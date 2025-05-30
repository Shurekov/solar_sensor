# sensor_model.py
import numpy as np

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

def quat_to_rotmat(q):
    """Преобразует кватернион [w, x, y, z] в матрицу поворота 3x3."""
    w, x, y, z = q
    return np.array([
        [1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w],
        [2 * x * y + 2 * z * w, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * x * w],
        [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x ** 2 - 2 * y ** 2]
    ])

def compute_Kc(alpha_C):
    if alpha_C >= np.radians(90):
        return 0.0
    elif alpha_C <= np.radians(74):
        return 1.0
    else:
        numerator = np.sin(np.radians(96)) * np.cos(alpha_C)
        denominator = np.sin(np.radians(22) + alpha_C) * np.sin(np.radians(16))
        return numerator / denominator

def compute_incidence_angle(sun_vec_psk, normal):
    dot = np.dot(sun_vec_psk, normal)
    dot = np.clip(dot, -1.0, 1.0)
    return np.arccos(dot)

def apply_total_reflection(angle_inc, current_i):
    return 0.0 if angle_inc >= np.radians(83) else current_i

def sun_detector_model(sun_ort_real_ssk, craft_orient_quat, inst_matrix=np.eye(3)):
    sin22 = np.sin(np.radians(22))
    cos22 = np.cos(np.radians(22))

    normals = {
        'face1': np.array([sin22, 0.0, cos22]),
        'face2': np.array([sin22, 0.0, -cos22]),
        'face3': np.array([sin22, cos22, 0.0]),
        'face4': np.array([sin22, -cos22, 0.0])
    }

    trans_matrix = quat_to_rotmat(craft_orient_quat)
    sun_ort_real_psk = np.dot(inst_matrix, np.dot(trans_matrix, sun_ort_real_ssk))
    sun_ort_real_psk = normalize(sun_ort_real_psk)

    alpha_C = np.arccos(sun_ort_real_psk[0])
    phi_s = np.arctan2(sun_ort_real_psk[2], sun_ort_real_psk[1])

    Kc = compute_Kc(alpha_C)

    currents = {}
    for name, n in normals.items():
        eps = compute_incidence_angle(sun_ort_real_psk, n)
        i = np.dot(sun_ort_real_psk, n) * Kc
        i = apply_total_reflection(eps, i)
        currents[name] = i

    return {
        "sun_ort_real_psk": sun_ort_real_psk,
        "currents": currents,
        "alpha_C_deg": np.degrees(alpha_C),
        "phi_s_deg": np.degrees(phi_s),
        "Kc": Kc
    }
