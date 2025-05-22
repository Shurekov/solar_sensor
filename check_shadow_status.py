import numpy as np
import math
from astropy.time import Time

# Функция для проверки освещенности (тень или свет)
def CheckShadowStatus(dateTime, r0):

    earth_radius = 6378.137  # Средний радиус Земли в км
    eps = math.radians(23.43929111)  # Наклонение плоскости эклиптики
    om = math.radians(282.940)  # Долгота восходящего узла и аргумент перицентра
    R_orbE = 149600000  # Средний радиус орбиты Земли в км

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
    eps_e = math.asin(earth_radius / np.linalg.norm(-r0)) # Угол между вектором КА-Земля и вектором центр Земли-поверхность земли

    # Если угол между КА и Солнцем больше угла между вектором КА-Земля и вектором центр Земли-поверхность земли, то объект находится в тени, иначе — в зоне солнечного света.
    return 1 if phi >= eps_e else 0
