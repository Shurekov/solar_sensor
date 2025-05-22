import numpy as np
from astropy.time import Time


def solar_sensor_model(r_sat, r_sun):
    """
    Моделирует выходные токи солнечного датчика на основе положения КА и Солнца.

    Вход:
        r_sat - вектор положения КА в ИСК (километры)
        r_sun - вектор положения Солнца в ИСК (километры)

    Выход:
        i1, i2, i3, i4 - выходные токи с граней датчика (нормированные)
    """
    # Единичный вектор направления на Солнце в инерциальной СК
    sun_dir = r_sun - r_sat
    sun_dir_norm = sun_dir / np.linalg.norm(sun_dir)

    # Предположим, что ПСК совпадает с инерциальной системой координат
    X_CПСК, Y_CПСК, Z_CПСК = sun_dir_norm

    # Угол визирования Солнца относительно оси X_ПСК
    alpha_C = np.arccos(X_CПСК)

    # Переводим радианы в градусы для удобства
    alpha_deg = np.degrees(alpha_C)

    # Коэффициент засветки K_C
    if alpha_deg >= 90:
        K_C = 0
    elif 74 <= alpha_deg < 90:
        alpha_rad = np.radians(alpha_deg)
        K_C = (np.sin(np.radians(96)) * np.cos(alpha_rad)) / \
              (np.sin(np.radians(22) + alpha_rad) * np.sin(np.radians(16)))
    else:
        K_C = 1

    # Нормали к граням датчика
    normals = [
        [np.sin(np.radians(22)), 0, np.cos(np.radians(22))],  # Грань 1
        [np.sin(np.radians(22)), 0, -np.cos(np.radians(22))],  # Грань 2
        [np.sin(np.radians(22)), np.cos(np.radians(22)), 0],  # Грань 3
        [np.sin(np.radians(22)), -np.cos(np.radians(22)), 0]  # Грань 4
    ]

    currents = []
    for normal in normals:
        cos_eps_n = np.dot(sun_dir_norm, normal)
        current = K_C * cos_eps_n
        # Эффект полного отражения при углах падения > 83°
        angle_of_incidence = np.degrees(np.arccos(cos_eps_n))
        if angle_of_incidence >= 83:
            current = 0
        currents.append(current)

    i1, i2, i3, i4 = currents
    return i1, i2, i3, i4


def reconstruct_sun_direction(i1, i2, i3, i4):
    """
    Восстанавливает единичный вектор направления на Солнце в ПСК
    по выходным токам солнечного датчика.
    """

    if all(i == 0 for i in [i1, i2, i3, i4]):
        return None  # Солнце вне поля зрения

    non_zero = [(i, idx) for idx, i in enumerate([i1, i2, i3, i4]) if i != 0]
    count = len(non_zero)

    if count == 4:
        # Все токи ненулевые — точное восстановление
        sin22 = np.sin(np.radians(22))
        cos22 = np.cos(np.radians(22))

        X = (i1 + i2) / (2 * sin22)
        Z = (i1 - i2) / (2 * cos22)
        Y = (i3 - i4) / (2 * cos22)
        vec = np.array([X, Y, Z])
        return vec / np.linalg.norm(vec)

    elif count == 3 or count == 2:
        try:
            # Пример решения для двух ненулевых токов
            A = np.sin(np.radians(22))
            B = np.cos(np.radians(22))

            X = (i1 + i3) / (2 * A)
            Y = (i3 - A * X) / B
            Z = (i1 - A * X) / B

            vec = np.array([X, Y, Z])
            return vec / np.linalg.norm(vec)
        except:
            return None

    else:
        return None