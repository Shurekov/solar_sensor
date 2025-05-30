import numpy as np
from sun_sensor_model import sun_detector_model, normalize


def quat_from_axis_angle(axis, angle_deg):
    """Создаёт кватернион из оси и угла поворота."""
    angle_rad = np.radians(angle_deg)
    axis = normalize(np.array(axis))
    return np.array([
        np.cos(angle_rad / 2),
        axis[0] * np.sin(angle_rad / 2),
        axis[1] * np.sin(angle_rad / 2),
        axis[2] * np.sin(angle_rad / 2)
    ])

if __name__ == "__main__":
    # Направление на Солнце в связанной системе координат (ССК)
    sun_ort_real_ssk = np.array([0.7, 0.7, 0.0])

    # Кватернион ориентации КА: поворот вокруг оси Y на 50 градусов
    craft_orient_quat = quat_from_axis_angle([0, 1, 0], 50)

    # Вызов модели датчика
    result = sun_detector_model(sun_ort_real_ssk, craft_orient_quat)


    # Вывод результатов
    print("Направление на Солнце в ПСК:", result["sun_ort_real_psk"])
    print("Измеренные токи:", result["currents"])
    print("Угол визирования α_C (градусы):", result["alpha_C_deg"])
    print("Азимут φ_s (градусы):", result["phi_s_deg"])
    print("Коэффициент засветки Kc:", result["Kc"])