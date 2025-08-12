def def_lin_beams(id_start:int, theta_start:int, theta_end:int, phi_const:int, include_end:bool, step:int=1) -> list[dict[int, int, int]]:
    """
    Generate a list of beam IDs based on a linear sequence.

    """
    last_theta = theta_end+step if include_end else theta_end
    return [{"id": id_start + i, "theta": theta, "phi": phi_const} for i, theta in enumerate(range(theta_start, last_theta, step))]