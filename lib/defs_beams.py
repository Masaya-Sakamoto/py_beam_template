def def_lin_beams(id_start:int, theta_start:int, theta_end:int, phi_const:int, step:int=1) -> list[dict[int, int, int]]:
    """
    Generate a list of beam IDs based on a linear sequence.

    """
    return [{"id": id_start + i, "theta": theta, "phi": phi_const} for i, theta in enumerate(range(theta_start, theta_end + 1, step))]


def def_basic_lin_beams(theta_max:int=25, phi_0:int=0, step:int=1) -> list[dict[int, int, int]]:
    """
    Generate a list of basic linear beams.

    """
    origin = {"id": 1, "theta": 0, "phi": phi_0}
    beams1 = def_lin_beams(id_start=2, theta_start=1, theta_end=theta_max, phi_const=phi_0, step=step)
    beams2 = def_lin_beams(id_start=len(beams1) + 2, theta_start=1, theta_end=theta_max, phi_const=phi_0 + 180, step=step)
    return [origin,] + beams1 + beams2