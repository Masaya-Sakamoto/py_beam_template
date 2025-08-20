from lib.defs_beams import def_lin_beams
from lib.defs_beam_sweeping import def_basic_lin_beamsweeping, def_lin_beamsweeping

def test_def_lin_beamsweeping():
    """
    Test the def_lin_beamsweeping function.
    Tests:
      - Check the length of the returned list.
      - Check the first, peak and last elements to ensure they are the same.
    """
    origin = {"id": 1, "theta": 0, "phi": 90}
    beams = def_lin_beams(id_start=2, theta_start=1, theta_end=25, pattern_rotation=90, include_end=True, step=1)
    beamsweeping = def_lin_beamsweeping(origin, beams)
    assert len(beamsweeping) == len(beams) * 2 + 1  # Original beams + reversed beams + origin
    assert beamsweeping[0] == origin
    assert beamsweeping[1] == beams[0]
    assert beamsweeping[len(beams)] == beams[-1]
    assert beamsweeping[-1] == beams[0]  # Last element should be the first beam in reverse order

def test_def_basic_lin_beamsweeping():
    """
    Test the def_basic_lin_beamsweeping function.
    Tests:
      - Check the length of the returned list.
      - Check the first, each peaks and each last elements of the entire of beams.
    """
    origin = {"id": 1, "theta": 0, "phi":45}
    beams_size = 25
    # origin: (1, 0, 0)
    # beam1: [(2,  1,  45), ..., (26, 25, 45)]
    # beam2: [(27, 1, 135), ..., (51, )]
    beams_list = [
        def_lin_beams(id_start=2, theta_start=1, theta_end=25, pattern_rotation=45, include_end=True, step=1),
        def_lin_beams(id_start=beams_size+2, theta_start=1, theta_end=25, pattern_rotation=45+90, include_end=True, step=1),
    ]
    beamsweeping = def_basic_lin_beamsweeping(origin, beams_list)
    assert len(beamsweeping) == (beams_size*2+1)*2
    # check: seq 1
    start_idx = 0
    seq_start = start_idx + 1
    seq_peak = seq_start + beams_size - 1
    seq_end = seq_start + 2*beams_size - 1
    assert beamsweeping[start_idx] == origin
    assert beamsweeping[seq_start] == beams_list[0][0]
    assert beamsweeping[seq_peak] == beams_list[0][-1]
    assert beamsweeping[seq_end] == beams_list[0][0]
    # check: seq 2
    start_idx = seq_end + 1
    seq_start = start_idx + 1
    seq_peak = seq_start + beams_size - 1
    seq_end = seq_start + 2*beams_size - 1
    assert beamsweeping[start_idx] == origin
    assert beamsweeping[seq_start] == beams_list[1][0]
    assert beamsweeping[seq_peak] == beams_list[1][-1]
    assert beamsweeping[seq_end] == beams_list[1][0]
