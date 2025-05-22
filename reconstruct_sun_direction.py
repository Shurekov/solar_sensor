def reconstruct_sun_direction(i1, i2, i3, i4):
    """
    Восстанавливает единичный вектор направления на Солнце в ПСК
    по выходным токам солнечного датчика.
    """

    # Если все нулевые — Солнце вне поля зрения
    if all(i == 0 for i in [i1, i2, i3, i4]):
        return np.array([0, 0, 0])

    # Случай: все 4 тока ненулевые (точное восстановление)
    if all(i != 0 for i in [i1, i2, i3, i4]):
        X = (i1 + i2) / (2 * np.sin(np.radians(22)))
        Z = (i1 - i2) / (2 * np.cos(np.radians(22)))
        Y = (i3 - i4) / (2 * np.cos(np.radians(22)))
        vec = np.array([X, Y, Z])
        return vec / np.linalg.norm(vec)

    # Общий случай: не все токи ненулевые
    non_zero = [(i, idx) for idx, i in enumerate([i1, i2, i3, i4]) if i != 0]
    count = len(non_zero)

    if count == 3 or count == 2:
        # Пример для двух ненулевых токов: i1 и i3
        try:
            A = np.sin(np.radians(22))
            B = np.cos(np.radians(22))

            # Решаем систему:
            # i1 = A * X + B * Z
            # i3 = A * X + B * Y
            # Запишем в виде матрицы и решим через подстановку

            # Получаем выражения:
            X = (i1 + i3) / (2 * A)
            Y = (i3 - A * X) / B
            Z = (i1 - A * X) / B

            vec = np.array([X, Y, Z])
            return vec / np.linalg.norm(vec)
        except:
            return None
    else:
        return None