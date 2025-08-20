from lib.defs_beams import def_lin_beams


def test_def_lin_beams():
    """
    Test the def_lin_beams function.
    """
    beams = def_lin_beams(id_start=1, theta_start=0, theta_end=10, pattern_rotation=45, include_end=True,step=2)
    beams_size = len(beams)
    assert beams_size == 5 + 1  # {0 .. 10} = {0, 2, 4, 6, 8, 10} with step 2 = 6 beams
    assert beams[0] == {"id": 1, "theta": 0, "phi": 45}
    assert beams[1] == {"id": 2, "theta": 2, "phi": 45}
    assert beams[beams_size - 1] == {"id": 6, "theta": 10, "phi": 45}
    beams = def_lin_beams(id_start=1, theta_start=0, theta_end=10, pattern_rotation=45, include_end=False, step=2)
    beams_size = len(beams)
    assert beams_size == 5  # {0 .. 10} = {0, 2, 4, 6, 8} with step 2 = 5 beams
    assert beams[0] == {"id": 1, "theta": 0, "phi": 45}
    assert beams[1] == {"id": 2, "theta": 2, "phi": 45}
    assert beams[beams_size - 1] == {"id": 5, "theta": 8, "phi": 45}