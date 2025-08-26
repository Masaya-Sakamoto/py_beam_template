from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json
from pytypes.type_beam import BeamPattern
from pytypes.type_beam import beam_t
from lib.defs_beams import def_const_constant_beam, def_const_linear_beams, def_const_fibonacci_beams, reset_beam_table_id
from lib.defs_beams import __linspace_on_unitdisc, __linear_point_on_unitdisc
from lib.defs_beams import __golden_angle
from pytypes.unit import unit_disc_coord_t
import math

def test__linspace_on_unitdisc_1():
    one = __linspace_on_unitdisc({'r':0.04, 'theta':1}, {'r':0.04, 'theta':1}, 1)
    one_lst = list(one)
    assert len(one_lst) == 1
    assert one_lst[0]['r'] == 0.04
    assert one_lst[0]['theta'] == 1

def test__linspace_on_unitdisc_n():
    n = __linspace_on_unitdisc({'r':0.04, 'theta':math.pi}, {'r':1.0, 'theta':math.pi}, 25)
    n_lst = list(n)
    assert len(n_lst) == 25
    assert n_lst[0] == {'r': 0.04, 'theta': math.pi}
    assert n_lst[1] == {'r': 0.08, 'theta': math.pi}
    assert n_lst[-1] == {'r': 1.0, 'theta': math.pi}

def test__map_to_hemisphere_coords():
    
    udc = __linear_point_on_unitdisc(
        start_point={'r': 0.04, 'theta': math.pi},
        end_point={'r': 1, 'theta': math.pi},
        N=25,
        include_end=True
    )

def test_def_const_linear_beams():
    config = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")
    beam_template_lst = get_beam_template_from_json(config)
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

    assert len(beam_table) == 51
    
    # test constant beam
    assert beam_table[0]['id'] == 1
    assert beam_table[0]['dB'] == 0
    assert beam_table[0]['theta_d'] == 0
    assert beam_table[0]['phi_d'] == 0

    # test linear beams theta: 1 - 25, phi: 0
    assert beam_table[1]['id'] == 2
    assert beam_table[1]['dB'] == 0
    assert beam_table[1]['theta_d'] == 1
    assert beam_table[1]['phi_d'] == 0
    assert beam_table[25]['id'] == 26
    assert beam_table[25]['dB'] == 0
    assert beam_table[25]['theta_d'] == 25
    assert beam_table[25]['phi_d'] == 0

    # test linear beams theta: 1 - 25, phi: 0
    assert beam_table[26]['id'] == 27
    assert beam_table[26]['dB'] == 0
    assert beam_table[26]['theta_d'] == 1
    assert beam_table[26]['phi_d'] == 180
    assert beam_table[50]['id'] == 51
    assert beam_table[50]['dB'] == 0
    assert beam_table[50]['theta_d'] == 25
    assert beam_table[50]['phi_d'] == 180

def test_def_const_fibonacci_beams():
    config = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    beam_template_lst = get_beam_template_from_json(config)
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
    
    assert len(beam_table) == 64

    # test fibonacci beams
    assert beam_table[0]['id'] == 1
    assert beam_table[0]['dB'] == 0
    assert beam_table[0]['theta_d'] == 0
    assert beam_table[0]['phi_d'] == 0

    assert beam_table[63]['id'] == 64
    assert beam_table[63]['dB'] == 0
    assert beam_table[63]['theta_d'] == 25
    assert beam_table[63]['phi_d'] == round((__golden_angle() * 63) * 180/math.pi%360, 0)