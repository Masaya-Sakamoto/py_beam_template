from pytypes.type_beam import beam_t, beam_str_t

def create_beam_str(beam_entry: beam_t, beam_mode:str) -> str:
    if not (beam_mode == 'TX' or beam_mode == 'RX'):
        raise ValueError("beam_type must be either 'TX' or 'RX'")
    return f"{beam_mode},{beam_entry['id']},0,0,{beam_entry['theta']},{beam_entry['phi']},,,,"

def create_beam_table_csv_data(beams:list[beam_t]) -> list[beam_str_t]:
    """
    [
      {
        'TX': '1,...'
        'RX': '1,...'
      }
        ,...,
      {
        'TX': '1,...'
        'RX': '1,...'
      }
    ]
    """
    beam_table = []
    for beam in beams:
        beam_table.append({
            'TX': create_beam_str(beam, 'TX'),
            'RX': create_beam_str(beam, 'RX')
        })
    return beam_table

def create_beam_table_csv(beam_table_str_lists:list[beam_str_t], filename:str):
    """
    Create a CSV file from the beam table string lists.
    """
    with open(filename, 'w') as f:
        # Write header
        f.write("Mode,BeamID,BeamType,beam_db,beam_theta,beam_phi,ch,ch_sw,ch_db,ch_deg\n")
        # Write each beam entry
        for beam_entry in beam_table_str_lists:
            f.write(beam_entry['TX'] + '\n')
            f.write(beam_entry['RX'] + '\n')