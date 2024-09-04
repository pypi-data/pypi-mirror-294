"""Функции для визуализации обработанных изображений"""

import cv2
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML, display

# Частота кадров в видео
FPS = 25

def writeVideo(frames: list[np.ndarray], filename: str):
    """
    Запись видео в файл.
    
    Аргументы
    ---------
    frames - последовательность кадров\n
    filename - путь сохранения .mp4 видеофайла
    """
    assert filename[-3:] == "mp4"

    w, h, ch = frames[0].shape
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))
    for frame in frames:
        out.write(frame)
    out.release()

def writeImage(image: np.ndarray, filename: str):
    """
    Запись видео в файл.
    
    Аргументы
    ---------
    image - изображение\n
    filename - путь сохранения изображения
    """
    cv2.imwrite(filename, image)

def drawBoundingBox(image: np.ndarray, box: list[int]) -> np.ndarray:
    """
    Отрисовка ограничивающей рамки лица.

    Аргументы
    ---------
    image - исходное изображение\n
    box - координаты ограничивающей рамки

    Результат
    ---------
    Изображение с ограничивающей рамкой лица
    """
    w, h, ch = image.shape
    box_color = (170, 150, 0)
    box_thickness = max(int(w / 640), 1)
    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), box_color, box_thickness)

    return image

def writeAngles(image: np.ndarray, box: list[int], phi: float, th: float) -> np.ndarray:
    """
    Отрисовка угла поворота головы.

    Аргументы
    ---------
    image - исходное изображение\n
    box - координаты ограничивающей рамки лица\n
    phi - азимутальный угол \n
    th - зенитный угол

    Результат
    ---------
    Изображение с указанием угла поворота головы
    """
    w, h, ch = image.shape
    text_thickness = max(int(w / 640), 1)
    box_thickness = max(int(w / 640), 1)
    font_scale = max(w / 1500, 0.3)
    gap = max(int(w / 200), 1)
    text_gap = max(int(w  / 150), 1)
    font_face = cv2.FONT_HERSHEY_DUPLEX
    text_color = (255, 255, 255)
    bg_color = (170, 150, 0)

    phi_label = str(phi)
    th_label = str(th)
    
    text_size_1, _ = cv2.getTextSize(
        phi_label, font_face, font_scale, text_thickness
    )
    text_w_1, text_h_1 = text_size_1

    text_size_2, _ = cv2.getTextSize(th_label, font_face, font_scale, text_thickness)
    text_w_2, text_h_2 = text_size_2

    rect_w = max(text_w_1, text_w_2) + 2 * gap
    rect_h = text_h_1 + text_h_2 + 2 * gap + text_gap

    rect_pos_1 = (box[0] - box_thickness + 1, box[3] )
    rect_pos_2 = (box[2], box[3] + rect_h)
    phi_pos = (int(rect_pos_1[0] + gap), int(gap + rect_pos_1[1] + text_h_1 + font_scale - 1))
    th_pos = (int(rect_pos_1[0] + gap), int(rect_pos_1[1] + rect_h + font_scale - 1 - gap))

    cv2.rectangle(image, rect_pos_1, rect_pos_2, bg_color, -1)
    cv2.putText(
        image, phi_label, phi_pos, font_face, font_scale, text_color, text_thickness
    )
    cv2.putText(
        image, th_label, th_pos, font_face, font_scale, text_color, text_thickness
    )

    return image


# def drawKeypoints(image: np.ndarray, keypoints: np.ndarray) -> np.ndarray:
#     w, h, ch = image.shape
#     pts_color = (255, 0, 0)
#     pts_scale = max(int(w / 640), 1)

#     for i in range(landmarks.shape[0]):
#         p = tuple(landmarks[i])
#         cv2.circle(image, p, pts_scale, pts_color, -1)
    
#     return image


def drawLandmarks(image: np.ndarray, landmarks: np.ndarray) -> np.ndarray:
    """
    Отрисовка ключевых точек.

    Аргументы
    ---------
    image     : numpy.ndarray
                Исходное изображение\n
    landmarks : numpy.ndarray
                Ключевые точки

    Результат
    ---------
    numpy.ndarray\n
    Изображение с размеченными ключевыми точками лица
    """
    w, h, ch = image.shape
    pts_color = (170, 150, 0)
    pts_scale = max(int(w / 640), 1)

    for i in range(landmarks.shape[0]):
        p = tuple(landmarks[i])
        cv2.circle(image, p, pts_scale, pts_color, -1)
    
    return image