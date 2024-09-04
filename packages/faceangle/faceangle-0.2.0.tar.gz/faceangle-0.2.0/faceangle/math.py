""" Функции математических преобразований """

import math as m

def toSpheric(x: float, y: float, z: float):
    """
    Преобразование декартовых координат в сферические.

    Аргументы
    ---------
    x - абсцисса\n
    y - ордината\n
    z - апликата

    Результат
    ---------
    r - радиус\n
    phi - азимутальный угол\n
    th - зенитный угол
    """
    r = m.sqrt(x**2 + y**2)
    phi = round(90 - m.atan2(m.sqrt(x**2 + y ** 2), z) * 180 / m.pi, 2)
    th = round(m.atan2(y, x) * 180 / m.pi, 2)

    return r, phi, th

def toCartesian(r: float, phi: float, th: float):
    """
    Преобразование сферических координат в декартовы.

    Аргументы
    ---------
    r - радиус\n
    phi - азимутальный угол\n
    th - зенитный угол

    Результат
    ---------
    x - абсцисса\n
    y - ордината\n
    z - апликата
    """
    x = r * m.cos(th) * m.sin(th)
    y = r * m.sin(th) * m.sin(phi)
    z = r * m.cos(phi)

    return x, y, z