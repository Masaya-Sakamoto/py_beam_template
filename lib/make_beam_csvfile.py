from lib.defs_beams import def_lin_beams

def create_beam_str(beam_entry: dict[str, int], beam_type:str):
    if not (beam_type == 'TX' or beam_type == 'RX'):
        raise ValueError("beam_type must be either 'TX' or 'RX'")
    return f"{beam_type},{beam_entry['id']},0,0,{beam_entry['theta']},{beam_entry['phi']},,,,"

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
        entry_list = []
        entry_list.append(create_beam_str(be, 'TX'))
        entry_list.append(create_beam_str(be, 'RX'))
        beam_table.append({
            'TX': entry_list[0],
            'RX': entry_list[1]
        })
    return beam_table

def create_beam_table_csv(beam_table_str_lists:list[dict[str,str]], filename:str):
    pass