from lib.defs_beams import def_lin_beams
from lib.defs_beam_sweeping import def_basic_lin_beamsweeping, def_lin_beamsweeping

def test_def_lin_beamsweeping():
    """
    Test the def_lin_beamsweeping function.
    Tests:
      - Check the length of the returned list.
      - Check the first and last elements to ensure they are the same.
    """
