from lib.defs_beams import def_lin_beams
from lib.make_beam_csvfile import create_beam_table, create_beam_table_csv

def test_create_beam_table():
    """
    Test the create_beam_table function.
    Tests:
      - Verify that the size of the output list is the 
        same as the size of the beam list input to the 
        function.
      - Check that the TX and RX entries in each beam l-
        ist have the save value.
    """
    origin = {'id':1, 'theta': 0, 'phi': 0}
    beams1 = def_lin_beams(
        id_start=2,
        theta_start=1,
        theta_end=25,
        phi_const=0,
        include_end=True,
        step=1
    )
    beams2 = def_lin_beams(
        id_start=27,
        theta_start=1,
        theta_end=25,
        phi_const=180,
        include_end=True,
        step=1
    )
    beams = [origin,] + beams1 + beams2
    beam_table_str_lists = create_beam_table(beams)
    assert len(beam_table_str_lists) == len(beams)
    for i, beam_table_str_dict in enumerate(beam_table_str_lists):
        TX_row_str_list = beam_table_str_dict['TX'].split(',')
        RX_row_str_list = beam_table_str_dict['RX'].split(',')
        assert TX_row_str_list[0] == "TX"
        assert RX_row_str_list[0] == "RX"
        assert TX_row_str_list[1] == str(beams[i]['id'])
        assert RX_row_str_list[1] == str(beams[i]['id'])
        assert TX_row_str_list[4] == str(beams[i]['theta'])
        assert RX_row_str_list[4] == str(beams[i]['theta'])
        assert TX_row_str_list[5] == str(beams[i]['phi'])
        assert RX_row_str_list[5] == str(beams[i]['phi'])
          

def test_create_beam_table_csv():
    """
    Test the create_beam_table_csv function.
    Test:
      - Verify that the function is creating a csv file
      - Check that the header row of the CSV file creat-
        ed by the function is correct
      - Verify that each row in the CSV file created by 
        the function matches the content created by the 
        create_beam_table() function.
    """
    pass