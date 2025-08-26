import math
from pytypes.type_beam import beam_t
from pytypes.unit import unit_disc_coord_t, map[unit_disc_coord_t], unit_disc_coord_generator
from pytypes.unit import unit_hemisphere_coord_t, map[unit_hemisphere_coord_t]
from pytypes.unit import PI, PI_D

# This function is deprecated and will be removed
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

def __linspace_on_unitdisc(
    start:unit_disc_coord_t,
    stop:unit_disc_coord_t,
    num:int,
    include_end:bool=True
) -> unit_disc_coord_generator:
    """
    numpy.linspaceと同等の機能を持つジェネレーター関数
    
    Parameters:
    -----------
    start : float
        開始値
    stop : float
        終了値
    num : int, optional
        生成する値の数 (デフォルト: 50)
    endpoint : bool, optional
        終了値を含むかどうか (デフォルト: True)
    
    Yields:
    -------
    float
        等間隔に配置された値
    """
    if num <= 0:
        return
    
    if num == 1:
        yield start
        return
    
    start_x = start["r"] * math.cos(start["theta"])
    start_y = start["r"] * math.sin(start["theta"])
    stop_x = stop["r"] * math.cos(stop["theta"])
    stop_y = stop["r"] * math.sin(stop["theta"])
    if include_end:
        # 終了値を含む場合
        step_x = (stop_x - start_x) / (num - 1)
        step_y = (stop_y - start_y) / (num - 1)
        for i in range(num):
            x_i = start_x + i * step_x
            y_i = start_y + i * step_y
            yield {"r": math.hypot(x_i, y_i), "theta": math.atan2(y_i, x_i)}
    else:
        # 終了値を含まない場合
        step_x = (stop_x - start_x) / num
        step_y = (stop_y - start_y) / num
        for i in range(num):
            x_i = start_x + i * step_x
            y_i = start_y + i * step_y
            yield {"r": math.hypot(x_i, y_i), "theta": math.atan2(y_i, x_i)}

def __snap_integer_angle(float_angle:float) -> int:
    return int(round(float_angle * PI_D / PI, 0) * PI / PI_D)

def __golden_angle():
    phi = (1 + math.sqrt(5)) / 2
    return 2 * PI / (phi**2)

def __phyllotaxis_points(N:int, delta:float) -> map[unit_disc_coord_t]:
    """
    平面上のphyllotaxis点を (r, theta) で返す。
    半径は単位円内に正規化。
    delta \\in [0,1)
    """
    n = range(N)
    ga = __golden_angle()
    return map(lambda n: {"r": math.sqrt((n + delta) / N), "theta": n * ga}, n)

def __map_to_hemisphere_coords(unitdisc_coords:map[unit_disc_coord_t]) -> map[unit_hemisphere_coord_t]:
    unit_hemisphere_coords:map[unit_hemisphere_coord_t] = map(lambda udc: {
        "theta": math.acos(1 - udc["r"]**2),
        "phi": udc["theta"]
    }, unitdisc_coords)
    return unit_hemisphere_coords

def __mod_theta_phi(
        unit_hemisphere_coords:map[unit_hemisphere_coord_t],
        theta_max:float|None=None,
        pattern_rotation:float|None=None,
        center_theta:float|None=None,
        center_phi:float|None=None,
        is_int_val:bool|None=False,
    ) -> map[unit_hemisphere_coord_t]:
    if pattern_rotation:
        unit_hemisphere_coords = map(lambda uhc: {
            "theta": uhc["theta"],
            "phi": uhc["phi"] + pattern_rotation
        }, unit_hemisphere_coords)
    if center_theta: # FIXME: implement center_theta adjustment
        """
        if {theta}-center_theta in pi/2
            theta = map(lambda t: t + center_theta, theta)
        else:
            NOT IMPLEMENTED
              ideas
                - Set them to pi/2
                - Ignore such points
        """
        print("Warning: center_theta is not implemented in __mod_theta_phi")
    if center_phi:
        unit_hemisphere_coords = map(lambda uhc: {
            "theta": uhc["theta"],
            "phi": uhc["phi"] + center_phi
        }, unit_hemisphere_coords)

    # Normalize angles to [0, 2π)
    unit_hemisphere_coords = map(lambda uhc: {
        "theta": uhc["theta"] % (2 * math.pi),
        "phi": uhc["phi"] % (2 * math.pi)
    }, unit_hemisphere_coords)

    if theta_max:
        unit_hemisphere_coords = map(lambda uhc: {
            "theta": uhc["theta"] * theta_max * 2 / PI,
            "phi": uhc["phi"]
        }, unit_hemisphere_coords)
    
    if is_int_val is not None and is_int_val==True:
        unit_hemisphere_coords = map(lambda uhc: {
            "theta": float(__snap_integer_angle(uhc["theta"])),
            "phi": float(__snap_integer_angle(uhc["phi"]))
        }, unit_hemisphere_coords)
        # Remove duplicates from an iterator
        # not implemented yet
    return unit_hemisphere_coords

def __linear_point_on_unitdisc(
        start_point: unit_disc_coord_t,
        end_point: unit_disc_coord_t,
        N: int,
        include_end: bool
) -> map[unit_disc_coord_t]:
    udc = __linspace_on_unitdisc(start_point, end_point, num=N, include_end=include_end)
    return map(lambda lc: {
        "r": lc["r"],
        "theta": lc["theta"]
    }, udc)


def __linear_point_on_hemisphere(
        N:int,
        start_point:unit_disc_coord_t,
        end_point:unit_disc_coord_t,
        theta_max:float,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool
    ) -> map[unit_hemisphere_coord_t]:
    udc = __linear_point_on_unitdisc(
        start_point=start_point,
        end_point=end_point,
        N=N,
        include_end=True
    )
    uhc = __map_to_hemisphere_coords(udc)
    uhc = __mod_theta_phi(
        uhc,
        theta_max=theta_max,
        pattern_rotation=pattern_rotation,
        center_theta=center_angle_theta,
        center_phi=center_angle_phi,
        is_int_val=is_int_val
    )

    return uhc


def __phyllotaxis_point_on_hemisphere(
        N:int, 
        delta:float, 
        theta_max:float, 
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool) -> map[unit_hemisphere_coord_t]:
    """
    1. phyllotaxis点を単位円盤に生成する ... __phyllotaxis_points
    2. それを当面積写像で半球にマッピングする
    3. 最後に天頂角を制限して返す -- 2., 3. ... __map_to_zenith_angle
    """
    # 極座標系でphyllotaxis点を生成
    udc = __phyllotaxis_points(N, delta)
    # 天頂角にマッピング
    uhc = __map_to_hemisphere_coords(udc)
    # 天頂角を制限して返す
    uhc = __mod_theta_phi(
        uhc,
        theta_max=theta_max,
        pattern_rotation=pattern_rotation,
        center_theta=center_angle_theta,
        center_phi=center_angle_phi,
        is_int_val=is_int_val)
    return uhc

def def_const_linear_beams(
        N: int,
        start_point:unit_disc_coord_t,
        end_point:unit_disc_coord_t,
        constant_dB:int,
        theta_max:float,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool
    ) -> list[beam_t]:
    # 単位変球面上にN点の線形点を生成
    uhc =  __linear_point_on_hemisphere(
        N=N,
        start_point=start_point,
        end_point=end_point,
        theta_max=theta_max,
        pattern_rotation=pattern_rotation,
        center_angle_theta=center_angle_theta,
        center_angle_phi=center_angle_phi,
        is_int_val=is_int_val
    )
    return [
        {
            "id": i,
            "dB": constant_dB,
            "theta": int(item["theta"] * PI_D / PI),
            "phi": int(item["phi"] * PI_D / PI)
        } for i, item in enumerate(uhc)]

def def_const_fibonacci_beams(
        N:int,
        start_point:unit_disc_coord_t,
        _end_point:unit_disc_coord_t,
        constant_dB:int,
        theta_max:float,
        pattern_rotation:float,
        center_angle_theta:float,
        center_angle_phi:float,
        is_int_val:bool
    ) -> list[beam_t]:
    # 度数法 -> 弧度法
    delta = start_point["r"]
    center_angle_phi += start_point["theta"]
    # 単位変球面上にN点のphyllotaxis点を生成
    uhc = __phyllotaxis_point_on_hemisphere(
        N,
        delta,
        theta_max,
        pattern_rotation=pattern_rotation,
        center_angle_theta=center_angle_theta,
        center_angle_phi=center_angle_phi,
        is_int_val=is_int_val
    )
    return [
        {
            "id": i,
            "dB": constant_dB,
            "theta": int(item["theta"] * PI_D / PI),
            "phi": int(item["phi"] * PI_D / PI)
        } for i, item in enumerate(uhc)]