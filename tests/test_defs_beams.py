from lib.defs_beams import def_lin_beams, def_basic_lin_beams


def test_def_lin_beams():
    """
    Test the def_lin_beams function.
    """
    beams = def_lin_beams(id_start=100, theta_start=0, theta_end=10, phi_const=45, step=2)
    assert len(beams) == 5 + 1  # {0 .. 10} = {0, 2, 4, 6, 8, 10} with step 2 = 6 beams
    assert beams[0] == {"id": 100, "theta": 0, "phi": 45}
    assert beams[1] == {"id": 101, "theta": 2, "phi": 45}
    assert beams[4] == {"id": 104, "theta": 8, "phi": 45}

def test_def_basic_lin_beams():
    """
    Test the def_basic_lin_beams function.
    """
    beams = def_basic_lin_beams(theta_max=10, phi_0=90, step=1)
    assert len(beams) == 21  # 1 origin + 10 + 10 beams
    assert beams[0] == {"id": 1, "theta": 0, "phi": 90}
    # Check first set of beams
    assert beams[1] == {"id": 2, "theta": 1, "phi": 90}
    assert beams[10] == {"id": 11, "theta": 10, "phi": 90}
    # Check second set of beams
    assert beams[11] == {"id": 12, "theta": 1, "phi": 270}  # Second set of beams
    assert beams[20] == {"id": 21, "theta": 10, "phi": 270}