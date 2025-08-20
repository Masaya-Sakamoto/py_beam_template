def create_beam_str(beam_entry: dict[str, int], beam_mode:str):
    if not (beam_mode == 'TX' or beam_mode == 'RX'):
        raise ValueError("beam_type must be either 'TX' or 'RX'")
    return f"{beam_mode},{beam_entry['id']},0,0,{beam_entry['theta']},{beam_entry['phi']},,,,"

def create_beam_table(beams:list[dict[str, int]]) -> list[dict[str,str]]:
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
    for be in beams:
        beam_table.append({
            'TX': create_beam_str(be, 'TX'),
            'RX': create_beam_str(be, 'RX')
        })
    return beam_table

def create_beam_table_csv(beam_table_str_lists:list[dict[str,str]], filename:str):
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