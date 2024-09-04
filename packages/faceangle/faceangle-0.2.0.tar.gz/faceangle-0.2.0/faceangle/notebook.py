"""Функции для визуализации в iPython блокнотах"""

import cv2
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import warnings

from numpy.typing import ArrayLike
from IPython.display import HTML, display


def visualizeAnimation(images: list[np.ndarray]):
    """
    Анимированная визуализация последовательности кадров.

    Аргументы
    ---------
    images - последовательность изображений
    """
    warnings.filterwarnings("ignore")

    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.grid(False)
    ax.set_axis_off()
    
    frames = []
    for image in images:
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = ax.imshow(rgbImage, animated=True)
        frames.append([frame])
        plt.close()

    ani = animation.ArtistAnimation(fig, frames, interval=60, blit=True)
    display(HTML(ani.to_jshtml()))


def animateLandmarks(landmarks: list[np.ndarray]):
    """
    Анимированная визуализация изменения ключевых точек

    Аргументы
    ---------
    landmarks - последовательность наборов ключевых точек
    """
    if len(landmarks[0].shape) != 3:
        raise AttributeError("Input argument must be list of landmarks.")
    
    warnings.filterwarnings("ignore")

    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.grid(False)
    ax.set_axis_off()
    
    frames = []
    for sample in landmarks:
        frame = plotLandmarks(sample)
        frames.append(frame)
        plt.close()

    ani = animation.ArtistAnimation(fig, frames, interval=60, blit=True)
    display(HTML(ani.to_jshtml()))


def plotLandmarks(landmarks: ArrayLike, image: np.ndarray = None):
    """
    Построение ключевых точек на графике. Функция принимает как двумерные,
    так и трёхмерные ключевые точки. Если в функцию передаётся несколько
    экземпляров ключевых точек, то графики отображаются в анимированном виде.

    Аргументы
    ---------
    landmarks - ключевые точки\n
    image - изображение, поверх которого строятся ключевые точки
            (только для двумерного случая и одного набора ключевых точек)
    """
    if type(landmarks) == np.ndarray:
        n_points, dim = landmarks.shape
        color_pts = (0/255., 150/255., 170/255.)
        fig = plt.figure(figsize=(5, 5))

        if dim == 2:
            ax = fig.add_subplot()

            x = landmarks[:, 0]
            y = landmarks[:, 1]

            if image is not None:
                rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                ax.imshow(rgbImage, animated=True)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            
            ax.scatter(x, y, c=[color_pts], s=0.5)

        elif dim == 3:
            ax = fig.add_subplot(projection='3d')

            x = landmarks[:, 0]
            y = landmarks[:, 1]
            z = landmarks[:, 2]

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            ax.scatter(x, y, z, c=[color_pts])

    elif type(landmarks) == list:
        color_pts = (0/255., 150/255., 170/255.)
        fig = plt.figure(figsize=(5, 5))

        ims = []

        for frame in landmarks:
            n_points, dim = frame.shape

            if dim == 2:
                ax = fig.add_subplot()

                x = frame[:, 0]
                y = frame[:, 1]

                if image is not None:
                    rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    ax.imshow(rgbImage, animated=True)
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                
                im = ax.scatter(x, y, c=[color_pts], s=0.5)
                plt.close()

                ims.append([im])

            elif dim == 3:
                ax = fig.add_subplot(projection='3d')

                x = frame[:, 0]
                y = frame[:, 1]
                z = frame[:, 2]

                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')

                im = ax.scatter(x, y, z, c=[color_pts])
                plt.close()
                
                ims.append([im])
        
        ani = animation.ArtistAnimation(fig, ims, interval=60, blit=True)
        display(HTML(ani.to_jshtml()))

