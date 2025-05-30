import numpy as np
from datetime import datetime, timedelta
from j2_gravitational_acceleration import a_grav

t0 = datetime(2024, 10, 1, 11, 0, 0)
r0 = np.array([5666.282392, 3512.092276, -1780.014521])  # км
v0 = np.array([2.194685, 0.146478, 7.275306])  # км/с

endTime = 86400  # 24 часа в секундах
dt = 1  # Шаг интегрирования

# Вектор состояния: [rx, ry, rz, vx, vy, vz]
y0 = np.concatenate((r0, v0))

def dydt(t, y):
    r = y[:3]
    v = y[3:]

    mu = 398600.4415  # км^3/с^2 (гравитационная постоянная Земли)
    dateTime = t0 + timedelta(seconds=float(t))

    # Центральное гравитационное ускорение
    r_norm = np.linalg.norm(r)
    a_central = -mu / r_norm ** 3 * r

    # Возмущение от J2
    a_perturb = a_grav(dateTime, r)

    a_total = a_central + a_perturb

    return np.concatenate((v, a_total))  # [dr/dt, dv/dt]


def rk4_step(y, t, dt, dydt_func):
    k1 = dydt_func(t, y)
    k2 = dydt_func(t + dt / 2, y + dt / 2 * k1)
    k3 = dydt_func(t + dt / 2, y + dt / 2 * k2)
    k4 = dydt_func(t + dt, y + dt * k3)

    y_new = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y_new


if __name__ == "__main__":
    np.set_printoptions(suppress=True, formatter={'float_kind': '{:.6f}'.format})
    print(f"Старт моделирования: {t0}")
    current_y = y0.copy()

    steps = int(endTime // dt) + 1
    trajectory = []
    times = []

    for i in range(1, steps):
        t = (i - 1) * dt  # текущее время в секундах от начала
        current_time = t0 + timedelta(seconds=t + dt)

        # Интегрируем на один шаг
        current_y = rk4_step(current_y, t, dt, dydt)

        # Сохраняем результаты
        trajectory.append(current_y.copy())
        times.append(current_time)

        # Выводим вектор состояния
        print(f"[{current_time}] Вектор состояния y = {current_y}")

    print("Моделирование завершено.")