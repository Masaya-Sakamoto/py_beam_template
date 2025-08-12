from lib.make_beam_csvfile import create_beam_table_csv, create_beam_table
from lib.defs_beams import def_lin_beams

def main():
    print("Hello from py-beam-template!")
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
    create_beam_table_csv(beam_table_str_lists, 'CustomBatchBeams.csv')


if __name__ == "__main__":
    main()
