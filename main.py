from lib.make_beam_file import create_beam_table_csv, create_beam_table_csv_data
from lib.defs_beams import def_const_linear_beams, def_const_fibonacci_beams
from lib.defs_beam_sweeping import create_beam_control_table
from lib.defs_beam_sweep_op import sequence_ops
from pytypes.type_beam import BeamPattern, beam_control_program_t, beam_t, config_t, beam_template_t
from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json
from tools.softmodem_management import run_softmodem, kill_softmodem
import shutil

# HOME_DIR = '/home/user'
# OAI_DIR = 'openairinterface5g'
# EXECUTABLES_DIR = 'cmake_targets/ran_build/build'
# SOFTMODEM_BIN = 'nr-softmodem'
# FLEXRIC_DIR = 'openair2/E2AP/flexric'
# FLEXRIC_BUILD_DIR = 'build'
# XAPP_BEAMMANAGEMENT_BIN = 'oaibox_xapp_beam_management'
# xapp_beam_management_bin_path = f'{HOME_DIR}/{OAI_DIR}/{FLEXRIC_DIR}/{FLEXRIC_BUILD_DIR}/examples/xApp/oaibox/{XAPP_BEAMMANAGEMENT_BIN}'
# local_beam_table_csv_location = './CustomBatchBeams.csv'
# du_beam_csv_location = f'{HOME_DIR}/{OAI_DIR}/radio/USRP/setup/'
# beam_switch_interval = 20


def main(
          config: config_t,
          beam_template_lst:list[beam_template_t],
          beam_control_program_lst: list[beam_control_program_t]
):
    """
    1. beam_listsを作成 list[list[dict[str, int]]]
    2. beam_listsからbs_seqを作成
    3. beam_listsからbeam_tableを作成 list[list[dict[str,str]]]
    4. beam_tableからcsvを作成
    5. csvを再配置
    6. softmodem起動
    7. beam-sweepingを実行
    """

    # beam_tableの作成
    beam_table: list[beam_t] = []
    for beam_template in beam_template_lst:
            if beam_template['type'] == BeamPattern.LINEAR:
                beam_table += def_const_linear_beams(
                    beam_template['steps'],
                    beam_template['start_point'],
                    beam_template['end_point'],
                    0,
                    config['theta_max'],
                    config['pattern_rotation'],
                    config['center_angle_theta'],
                    config['center_angle_phi'],
                    True
                )
            elif beam_template['type'] == BeamPattern.FIBONACCI:
                beam_table += def_const_fibonacci_beams(
                    beam_template['steps'],
                    beam_template['start_point'],
                    beam_template['end_point'],
                    0,
                    config['theta_max'],
                    config['pattern_rotation'],
                    config['center_angle_theta'],
                    config['center_angle_phi'],
                    True
                )
            elif beam_template['type'] == BeamPattern.CIRCULAR:
                pass
            else:
                raise ValueError(f"Unsupported beam pattern: {beam_template['type']}")
    
    # beam table csvファイルを作成
    csv_data = create_beam_table_csv_data(beam_table)
    create_beam_table_csv(csv_data, config['local_beam_table_csv_location'])
    
    # beam control tableを作成
    beam_control_table = create_beam_control_table(
        beam_table,
        beam_control_program_lst,
        seed=config['random_seed']
    )

    # softmodem起動

    # beam controlを実行
    sequence_ops(beam_control_table, config['xapp_beam_management_bin'])

    # 停止処理を書く

if __name__ == "__main__":
    config = arg_parser()
    beam_template_lst = get_beam_template_from_json(config)
    beam_control_program_lst = get_beam_control_program_from_json(config)
    main(config, beam_template_lst, beam_control_program_lst)
