from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json
from pytypes.type_beam import BeamControlMethod, BeamPattern
from lib.defs_beams import def_const_constant_beam, def_const_linear_beams, def_const_fibonacci_beams, reset_beam_table_id
from lib.defs_beam_sweeping import create_beam_control_table

def test_create_lin_seq_beam_control_table():
    config = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")
    beam_template_lst = get_beam_template_from_json(config)
    beam_control_program_lst = get_beam_control_program_from_json(config)

    # beam table作成
    beam_table = []
    for beam_template in beam_template_lst:
        assert beam_template['type'] == BeamPattern.CONST or beam_template['type'] == BeamPattern.LINEAR
        if beam_template['type'] == BeamPattern.CONST:
            tmp_bt = def_const_constant_beam(
                1,
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
        elif beam_template['type'] == BeamPattern.LINEAR:
            tmp_bt = def_const_linear_beams(
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
        
        else:
            pass
    beam_table = reset_beam_table_id(beam_table)

    # control table作成
    beam_control_table = create_beam_control_table(
        beam_table,
        beam_control_program_lst,
        seed=config['random_seed']
    )

    # チェック
    # class beam_sweeping_t(TypedDict):
    # id: int
    # dB: dB_t
    # theta: int
    # phi: int
    # duration: int
    assert len(beam_control_table) == 1 + 1 + 25 + 25 + 1 + 25 + 25 + 1 + 1
    assert beam_control_table[0] == {
        'id': 1,
        'dB': 0,
        'theta_d': 0,
        'phi_d': 0,
        'duration': 10,
    }
    assert beam_control_table[2] == {
        'id': 2,
        'dB': 0,
        'theta_d': 1,
        'phi_d': 0,
        'duration': 10,
    }
    assert beam_control_table[2+25] == {
        'id': 26,
        'dB': 0,
        'theta_d': 25,
        'phi_d': 0,
        'duration': 10,
    }
    assert beam_control_table[2+25+24] == {
        'id': 2,
        'dB': 0,
        'theta_d': 1,
        'phi_d': 0,
        'duration': 10,
    }
    assert beam_control_table[2+25+25] == {
        'id': 1,
        'dB': 0,
        'theta_d': 0,
        'phi_d': 0,
        'duration': 10,
    }

    assert beam_control_table[2+25+25+1] == {
        'id': 27,
        'dB': 0,
        'theta_d': 1,
        'phi_d': 180,
        'duration': 10,
    }
    assert beam_control_table[2+25+25+25] == {
        'id': 51,
        'dB': 0,
        'theta_d': 25,
        'phi_d': 180,
        'duration': 10,
    }
    assert beam_control_table[2+25+25+25+25] == {
        'id': 27,
        'dB': 0,
        'theta_d': 1,
        'phi_d': 180,
        'duration': 10,
    }
    assert beam_control_table[2+25+25+25+25+1] == {
        'id': 1,
        'dB': 0,
        'theta_d': 0,
        'phi_d': 0,
        'duration': 10,
    }
    assert beam_control_table[2+25+25+25+25+1+1] == {
        'id': 1,
        'dB': 0,
        'theta_d': 0,
        'phi_d': 0,
        'duration': 5,
    }