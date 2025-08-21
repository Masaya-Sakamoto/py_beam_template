import math
from pytypes.type_beam import beam_t


def def_lin_beams(id_start:int, theta_start_d:int, theta_end_d:int, pattern_rotation_d:int, include_end:bool, step:int=1) -> list[beam_t]:
    """
    Generate a list of beam IDs based on a linear sequence.

    """
    last_theta = theta_end_d+step if include_end else theta_end_d
    return [{
        "id": id_start + i,
        "dB": 0,  # Default dB value, can be modified later 
        "theta": theta_d,
        "phi": pattern_rotation_d
    } for i, theta_d in enumerate(range(theta_start_d, last_theta, step))]

def __snap_integer_angle(float_angle:float) -> int:
    return int(round(float_angle * 180 / math.pi, 0) * math.pi / 180)

def __golden_angle():
    phi = (1 + math.sqrt(5)) / 2
    return 2 * math.pi / (phi**2)

def __phyllotaxis_points(N:int, delta:float) -> tuple[map[float], map[float]]:
    """
    平面上のphyllotaxis点列を (r, theta) で返す。
    半径は単位円内に正規化。
    delta \\in [0,1)
    """
    n = range(N)
    ga = __golden_angle()
    r = map(lambda n: math.sqrt((n + delta) / N), n)
    phi = map(lambda n: n * ga, n)
    return r, phi

def __map_to_zenith_angle(r:map[float], phi:map[float]) -> map[float]:
    theta = map(lambda r: math.acos(1 - r**2), r)
    return theta

def __mod_theta_phi(
        theta:map[float],
        phi:map[float],
        theta_max:float|None=None,
        pattern_rotation:float|None=None,
        center_theta:float|None=None,
        center_phi:float|None=None,
        is_int_val:bool|None=False,
    ) -> tuple[map[float|int], map[float|int]]:
    if pattern_rotation:
        phi = map(lambda p: p + pattern_rotation, phi)
    if theta_max:
        theta = map(lambda t: t * theta_max * 2 / math.pi, theta)
    if center_theta:
        print("Warning: center_theta is not implemented in __mod_theta_phi")
    if center_phi:
        print("Warning: center_phi is not implemented in __mod_theta_phi")
    # Normalize angles to [0, 2π)
    theta = map(lambda t: t % (2 * math.pi), theta)
    phi = map(lambda p: p % (2 * math.pi), phi)
    if is_int_val is not None and is_int_val==True:
        theta = map(__snap_integer_angle, theta)
        phi = map(__snap_integer_angle, phi)
        # Remove duplicates from an iterator
        # not implemented yet
    return (theta, phi)

# FIXME: まだ単位円盤から変換する実装はしていない
def __linear_point_on_hemisphere(
        theta_start_d:int,
        theta_end_d:int,
        theta_step_d:int,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool
    ) -> tuple[map[float|int], map[float|int]]:
    step_vector = (theta_end_d - theta_start_d) // abs(theta_end_d - theta_start_d) * theta_step_d
    theta = map(lambda t: t * math.pi / 180, range(theta_start_d, theta_end_d+step_vector, step_vector))
    phi = map(lambda p: p, (pattern_rotation for _ in range(theta_start_d, theta_end_d+step_vector, step_vector)))
    theta, phi = __mod_theta_phi(theta, phi, is_int_val=is_int_val)
    return (theta, phi)

def __phyllotaxis_point_on_hemisphere(
        N:int, 
        delta:float, 
        theta_max:float, 
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool) -> tuple[map[float|int], map[float|int]]:
    """
    1. phyllotaxis点を単位円盤に生成する ... __phyllotaxis_points
    2. それを当面積写像で半球にマッピングする
    3. 最後に天頂角を制限して返す -- 2., 3. ... __map_to_zenith_angle
    """
    # 極座標系でphyllotaxis点列を生成
    r, phi = __phyllotaxis_points(N, delta)
    # 天頂角にマッピング
    theta = __map_to_zenith_angle(r, phi)
    # 天頂角を制限して返す
    theta, phi = __mod_theta_phi(theta, phi, theta_max=theta_max, pattern_rotation=pattern_rotation, is_int_val=is_int_val)
    return (theta, phi)

def def_basic_linear_beams(
        theta_start_d:int,
        theta_end_d:int,
        theta_step_d:int,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool
    ) -> list[dict[str, int]]:
    theta, phi =  __linear_point_on_hemisphere(theta_start_d, theta_end_d, theta_step_d, pattern_rotation, center_angle_theta, center_angle_phi, is_int_val)
    return [{"id": i, "theta": int(t), "phi": int(p)} for i, (t, p) in enumerate(zip(theta, phi))]

def def_basic_fibonacci_beams(
        N:int,
        delta:float,
        theta_max:float,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float
    ) -> list[dict[str, int]]:
    theta, phi = __phyllotaxis_point_on_hemisphere(N, delta, theta_max, pattern_rotation=pattern_rotation, center_angle_theta=center_angle_theta, center_angle_phi=center_angle_phi, is_int_val=True)
    # 型ヒント用: float(int) -> int -- int(t), int(p)
    return [{"id": i, "theta": int(t), "phi": int(p)} for i, (t, p) in enumerate(zip(theta, phi))]