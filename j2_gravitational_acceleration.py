import numpy as np
import math
from astropy.time import Time

# Функция для расчета ускорения с учетом возмущений J2
def a_grav(dateTime, r0):
    A = -19089.451590
    B = 8640184.812866
    C = 0.093104
    D = -6.2e-6
    JD0 = 2451545
    JDD = 36525
    DS2R = 7.272205216643039903848712e-5
    J2 = 1.08262668355e-3  # Коэффициент второй зональной гармоники
    earth_radius = 6.378137e6  # Средний радиус Земли в метрах
    mu = 3.986004418e14  # Гравитационная постоянная Земли м^3/с^2

    # Расчёт юлианской даты с использованием astropy
    JD = Time(dateTime).jd  # Преобразование datetime в юлианскую дату
    t = (JD - JD0) / JDD
    f = 86400 * (JD % 1.0)
    alfa = DS2R * ((A + (B + (C + D * t) * t) * t) + f)
    alfa = alfa % (2 * math.pi)
    if alfa < 0:
        alfa += 2 * math.pi

    # Матрица перехода от J200 в ГСК
    Mj2kGr = np.array([[math.cos(alfa), -math.sin(alfa), 0],
                       [math.sin(alfa),  math.cos(alfa), 0],
                       [0             , 0              , 1]])

    # Радиус-вектор в ГСК
    rGsk = np.dot(Mj2kGr, r0 * 1000)

    # Расчёт возмущающего ускорения
    rMod = np.sqrt(np.dot(rGsk, rGsk))
    a_J2 = (-1.5 * J2 * (mu / rMod ** 2) * ((earth_radius / rMod) ** 2) *
            np.array([(1 - 5 * (rGsk[2] / rMod) ** 2) * rGsk[0] / rMod,
                      (1 - 5 * (rGsk[2] / rMod) ** 2) * rGsk[1] / rMod,
                      (3 - 5 * (rGsk[2] / rMod) ** 2) * rGsk[2] / rMod]))

    # Ускорение от несфееричности в ИСК
    a_grav = np.dot(Mj2kGr.T, a_J2) / 1000
    return a_grav

    # Расчёт координат Солнца
    JD = Time(dateTime).jd  # Преобразование datetime в юлианскую дату
    T = (JD - 2451545.0) / 36525.0 # Модифицированная Юлианская дата
    M = math.radians(357.5226 + 35999.049 * T)  # Средняя аномалия
    lm = om + M + math.radians(6892/3600)*math.sin(M) + math.radians(72/60)*math.sin(2*M)
    rs = np.array([        math.cos(lm),
                    math.sin(lm)*math.cos(eps),
                    math.sin(lm)*math.sin(eps)]) * R_orbE

    # Расчёт углов
    dif = rs - r0 # Угол между вектором КА-Солнце и вектором КА-Земля
    phi = math.acos(np.dot(-r0, dif) / (np.linalg.norm(r0) * np.linalg.norm(dif))) # Угол между КА и Солнцем