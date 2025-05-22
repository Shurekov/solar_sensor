import numpy as np
from datetime import datetime, timedelta
from check_shadow_status import CheckShadowStatus
from j2_gravitational_acceleration import a_grav

# Начальные условия
t0 = datetime(2024, 10, 1, 11, 0, 0)
r0 = np.array([5666.282392, 3512.092276, -1780.014521])  # км
v0 = np.array([2.194685, 0.146478, 7.275306])            # км/с

# Параметры интегрирования
endTime = 86400  # 24 часа
dt = 1           # шаг интегрирования, 1 секунда

# Константы
mu = 398600.4415  # км³/с²

# Функция правой части уравнения движения
def derivatives(t, state, dateTime):
    r = state[:3]
    v = state[3:]

    rj2k = np.linalg.norm(r)
    grav_acc = -(mu / rj2k**3) * r + a_grav(dateTime, r)

    drdt = v
    dvdt = grav_acc

    return np.concatenate((drdt, dvdt))

# Метод Рунге–Кутты 4-го порядка
def rk4_step(t, state, dt, dateTime):
    k1 = dt * derivatives(t, state, dateTime)
    k2 = dt * derivatives(t + dt/2, state + k1/2, dateTime + timedelta(seconds=dt//2))
    k3 = dt * derivatives(t + dt/2, state + k2/2, dateTime + timedelta(seconds=dt//2))
    k4 = dt * derivatives(t + dt, state + k3, dateTime + timedelta(seconds=dt))

    return state + (k1 + 2*k2 + 2*k3 + k4) / 6

# Интегрирование
state = np.concatenate((r0, v0))  # объединяем состояние
lighting = CheckShadowStatus(t0, r0)

for i in range(int(endTime // dt)):
    current_time = t0 + timedelta(seconds=i * dt)

    # Интегрируем по RK4
    state = rk4_step(i * dt, state, dt, current_time)

    # Извлекаем новые значения r и v
    r = state[:3]
    v = state[3:]

    # Проверка освещённости
    currentLight = CheckShadowStatus(current_time, r)
    if lighting != currentLight:
        print(f"Переход {'в зону тени' if currentLight == 0 else 'в освещённую область'}. Время: {current_time}")
        lighting = currentLight