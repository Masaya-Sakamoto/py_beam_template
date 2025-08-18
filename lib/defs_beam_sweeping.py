def def_lin_beam_sweeping(origin: dict[str, int], beams: list[dict[str, int]]) -> list[dict[str, int]]:
    """
    Generate a list of basic linear beams with sweeping angles.

    """
    print(f"type(origin)={type(origin)}, type(beams)={type(beams)}")
    return [origin,] + beams + beams[-1::-1]  # Reverse the last beam to create a sweeping effect

def def_basic_lin_beam_sweeping(origin: dict[str, int], beams_list: list[list[dict[str, int]]]) -> list[dict[str, int]]:
    result:list[dict[str, int]] = []
    for beams in beams_list:
        result.extend(def_lin_beam_sweeping(origin, beams))
    return result