"""Модели детектирования лиц, ключевых точек лица и оценки поворота головы"""

import cv2
from insightface.app import FaceAnalysis
import numpy as np
import onnxruntime as ort
from tqdm import tqdm
import warnings

from .math import toSpheric
from .preprocessing import estimateNorm
from .visualization import drawBoundingBox, drawLandmarks, writeAngles

NOSE_2D_POS        = 86  # Порядковый номер кончика носа в наборе двумерных ключевых точек
NOSE_3D_POS        = 34  # Порядковый номер кончика носа в наборе трёхмерных ключевых точек
LANDMARKS_2D_NUM   = 106 # Количество двумерных ключевых точек
LANDMARKS_3D_NUM   = 68  # Количество трёхмерных ключевых точек
SELECTED_2D_LANDMARKS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                         10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                         20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                         30, 31, 32, 72, 73, 74, 75, 76, 77, 78, 79,
                         80, 81, 82, 83, 84, 85]     # Индексы двумерных ключевых точек овала лица и носа
SELECTED_3D_LANDMARKS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                         27, 28, 29, 30, 31, 32, 33, 34] # Индексы трёхмерных ключевых точек овала лица и носа

class FaceDetector:
    """
    Объект для детектирования лица на изображении.

    Члены данных
    ------------
    providers : list[str] 
                Аппараты, на которых проводятся вычисления
                (CPUExecutionProvider, CUDAExecutionProvider)\n
    detector :  insightface.app.FaceAnalysis
                Модель детектирования лица на изображении\n
    det_size :  tuple[int]
                Входной размер изображения для модели детектирования
    """
    def __init__(self, det_size: tuple[int] = (448, 448), use_gpu: bool = True):
        """
        Аргументы
        ---------
        det_size : tuple[int]
                   Входной размер изображения для модели детектирования\n
        use_gpu  : bool
                   Указатель на использование GPU
        """
        warnings.filterwarnings("ignore")
        if use_gpu:
            self.providers = ["CUDAExecutionProvider"]
        else:
            self.providers = ["CPUExecutionProvider"]


        self.detector = FaceAnalysis(allowed_modules=['detection', 'landmark_2d_106', 'landmark_3d_68'],
                                     providers=self.providers)
        self.detector.prepare(ctx_id=0, det_size=det_size)
        self.det_size = det_size
    
    def process(self, image):
        faces = self.detector.get(image)
        for face in faces:
            face.landmarks2d = None
            face.landmarks3dProjection = None
            face.landmarks2dCentered = None
            face.landmarks3dCentered = None
            face.angle = None

            keypoints = face.kps.astype(int)
            matrix = estimateNorm(keypoints, min(self.det_size))
            inverseMatrix = cv2.invertAffineTransform(matrix)

            alignedImage = cv2.warpAffine(image, matrix, self.det_size, borderValue=0.0)
            alignedFaces = self.detector.get(alignedImage)

            if len(alignedFaces) > 0:
                lmks2d = alignedFaces[0].landmark_2d_106
                lmks3d = alignedFaces[0].landmark_3d_68

                lmks2dForTransform = np.hstack([lmks2d, np.ones((LANDMARKS_2D_NUM, 1))]).T
                lmks3dForTransform = np.hstack([lmks3d[:, :2], np.ones((LANDMARKS_3D_NUM, 1))]).T

                face.landmarks2d = (np.dot(inverseMatrix,
                                                    lmks2dForTransform).T)[:, :2].astype(int)
                face.landmarks3dProjection = (np.dot(inverseMatrix,
                                              lmks3dForTransform).T)[:, :2].astype(int)

                lmks2d /= min(self.det_size)
                lmks3d /= min(self.det_size)

                lmks2dExceptNose = np.vstack([lmks2d[:NOSE_2D_POS - 1, :], lmks2d[NOSE_2D_POS:, :]])
                nose2d = lmks2d[NOSE_2D_POS, :]
                lmks2dCentered = lmks2dExceptNose - nose2d

                lmks3dExceptNose = np.vstack([lmks3d[:NOSE_3D_POS - 1, :], lmks3d[NOSE_3D_POS:, :]])
                nose3d = lmks3d[NOSE_3D_POS, :]
                lmks3dCentered = lmks3dExceptNose - nose3d

                face.landmarks2dCentered = lmks2dCentered
                face.landmarks3dCentered = lmks3dCentered
        
        return faces
    
      
    def processImage(self, image, draw_bbox=True, draw_lmks='2d', write_angle=True):
        faces = self.process(image)
        processedImage = image.copy()
        if len(faces) > 0:
            for face in faces:
                if draw_bbox:
                    box = face.bbox.astype(int)
                    processedImage = drawBoundingBox(processedImage, box)

                if face.landmarks3dProjection is not None and draw_lmks == "3d":
                    processedImage = drawLandmarks(processedImage, face.landmarks3dProjection.astype(int))

                if face.landmarks2d is not None and draw_lmks == "2d":
                    processedImage = drawLandmarks(processedImage, face.landmarks2d.astype(int))

                if face.angle is not None and write_angle:
                    phi, th = face.angle
                    processedImage = writeAngles(processedImage, box, phi, th)

            return processedImage
            
        else:
            return None
    
    def processVideo(self, video, draw_bbox=True, draw_lmks="2d", write_angle=True):
        frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        clip = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype("uint8"))

        fc = 0
        ret = True

        while fc < frameCount and ret:
            ret, clip[fc] = video.read()
            fc += 1

        video.release()

        frames = []
        for frame in clip:
            frames.append(frame)

        processed_frames = []
        for frame in tqdm(frames):
            processed_image = self.processImage(frame, draw_bbox, draw_lmks, write_angle)
            if processed_image is None:
                processed_frames.append(frame)
            else:
                processed_frames.append(processed_image)
        
        return processed_frames


class AngleEstimator(FaceDetector):
    def __init__(self, angle_estimator_path, det_size = (448, 448), angle_size = (448, 448), use_gpu = True):
        super().__init__(det_size, use_gpu)
        self.angle_estimator = ort.InferenceSession(angle_estimator_path,
                                                    providers=self.providers)
        self.angle_size = angle_size

    def process(self, image):
        faces = super().process(image)
        for face in faces:
                if face.landmarks3dCentered is not None:
                    # lmksForAngle = face.landmarks3dCentered.take(SELECTED_3D_LANDMARKS, axis=0)
                    # k = len(SELECTED_3D_LANDMARKS)

                    k = LANDMARKS_3D_NUM - 1
                    lmksForAngle = face.landmarks3dCentered.reshape(1, k * 3)
                    x, y, z = self.angle_estimator.run(None, {"landmarks": lmksForAngle})[0][0]
                    r, phi, th = toSpheric(x, y, z)

                    face.angle = (phi, th)
        
        return faces