def def_lin_beamsweeping(origin: dict[int, int, int], beams: list[dict[int, int, int]]) -> list[dict[int, int, int]]:
    """
    Generate a list of basic linear beams with sweeping angles.

    """
    print(f"type(origin)={type(origin)}, type(beams)={type(beams)}")
    return [origin,] + beams + beams[-1::-1]  # Reverse the last beam to create a sweeping effect

def def_basic_lin_beamsweeping(origin: dict[int, int, int], beams_list: list[list[dict[int, int, int]]]) -> list[dict[int, int, int]]:
    result:dict[int, int, int] = []
    for beams in beams_list:
        result.extend(def_lin_beamsweeping(origin, beams))
    return result