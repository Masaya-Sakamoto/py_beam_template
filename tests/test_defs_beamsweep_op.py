from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json
from lib.defs_beams import def_const_fibonacci_beams, reset_beam_table_id
from lib.defs_beam_sweeping import create_beam_control_table
from pytypes.type_beam import BeamPattern
from lib.defs_beam_sweep_op import sequence_ops
from pytypes.type_beam import beam_sweeping_t

ret_code = 0
def init_testcase(testcase_returncode:int):
    global ret_code
    ret_code = testcase_returncode

def mock_oaibox_xapp_beam_management_handler(txBeamId:int, rxBeamId:int, program_path:str) -> bool:
    return ret_code == 0

def test_sequence_ops(mocker):
    program_path = "/path/to/oai_xapp_beam_management" # dummy

    # beam control table作成
    config = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    beam_template_lst = get_beam_template_from_json(config)
    beam_control_program_lst = get_beam_control_program_from_json(config)
    # beam table作成
    beam_table = []
    for beam_template in beam_template_lst:
        assert beam_template['type'] == BeamPattern.FIBONACCI
        tmp_bt = def_const_fibonacci_beams(
                beam_template['steps'],
                beam_template['start_point'],
                beam_template['end_point'],
                0,
                config['theta_max'],
                config['pattern_rotation_angle'],
                config['center_angle_theta'],
                config['center_angle_phi'],
                True
            )
        beam_table += tmp_bt
    beam_table = reset_beam_table_id(beam_table)

    # control table作成
    beam_control_table = create_beam_control_table(
        beam_table,
        beam_control_program_lst,
        seed=config['random_seed']
    )

    # mock initialize: subprocess.run, sleep
    mocker.patch('time.sleep')
    mocker.patch('lib.defs_beam_sweep_op.oai_xapp_beam_management_handler', new=mock_oaibox_xapp_beam_management_handler)

    init_testcase(0) # Mock successful execution
    assert sequence_ops(beam_control_table, program_path) == True
    init_testcase(1) # Mock failed execution
    assert sequence_ops(beam_control_table, program_path) == False