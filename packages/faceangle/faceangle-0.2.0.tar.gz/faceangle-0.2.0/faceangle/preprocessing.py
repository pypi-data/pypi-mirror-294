"""Функции для предварительной обработки изображений"""

import numpy as np
from skimage import transform as trans

# Целевые точки лица, относительно которых выравнивается изображение
MY_DST = np.array(
    [[197, 194], [251, 194], [224, 223],
     [203, 253], [245, 253]],
    dtype=np.float32)

def estimateNorm(kps: np.ndarray, image_size: int = 448) -> np.ndarray:
    """
    Получение матрицы преобразований для выравнивания относительно ключевых точек

    Аргументы
    ---------
    kps - ключевые точки лица (центры глаз, кончик носа, уголки губ)\n
    image_size - размер стороны квадратного изображения

    Результат
    ---------
    M - матрица афинного преобразования
    """
    assert kps.shape == (5, 2)
    assert image_size%448==0 or image_size%448==0
    if image_size%448==0:
        ratio = float(image_size)/448.0
        diff_x = 0
    dst = MY_DST * ratio
    dst[:,0] += diff_x
    tform = trans.SimilarityTransform()
    tform.estimate(kps, dst)
    M = tform.params[0:2, :]
    
    return M