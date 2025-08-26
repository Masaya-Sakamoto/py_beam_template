from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json
from pytypes.type_beam import BeamPattern, BeamControlMethod
import math

def test_arg_parser():
    # arg_parser()自体の動作検証
    assert arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    assert arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    assert arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    config_fib_rnd = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    config_lin_rnd = arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    config_lin_seq = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    # 型チェック
    assert type(config_fib_rnd["home_dir"]) == str and config_fib_rnd["home_dir"] == "/home/user"
    assert type(config_fib_rnd["oai_dir"]) == str
    assert type(config_fib_rnd["exec_dir"]) == str
    assert type(config_fib_rnd["softmodem_bin"]) == str
    assert type(config_fib_rnd["flexric_dir"]) == str
    assert type(config_fib_rnd["flexric_build_dir"]) == str
    assert type(config_fib_rnd["xapp_beam_management_bin"]) == str
    assert type(config_fib_rnd["xapp_beam_management_bin_path"]) == str
    assert type(config_fib_rnd["local_beam_table_csv_location"]) == str
    assert type(config_fib_rnd["du_beam_table_csv_location"]) == str
    assert type(config_fib_rnd["beam_template_file_jsonl"]) == str
    assert type(config_fib_rnd["beam_control_program_jsonl"]) == str
    assert type(config_fib_rnd["theta_max_d"]) == int
    assert type(config_fib_rnd["theta_min_d"]) == int
    assert type(config_fib_rnd["theta_min"]) == float
    assert type(config_fib_rnd["theta_max"]) == float
    assert type(config_fib_rnd["pattern_rotation_angle"]) == float
    assert type(config_fib_rnd["center_angle_theta"]) == float
    assert type(config_fib_rnd["center_angle_phi"]) == float
    assert type(config_fib_rnd["random_seed"]) == int

    # 値の確認 - fib_rnd_conf.json
    assert config_fib_rnd["home_dir"] == "/home/user"
    assert config_fib_rnd["oai_dir"] == "openairinterface5g"
    assert config_fib_rnd["exec_dir"] == "cmake_targets/ran_build/build"
    assert config_fib_rnd["softmodem_bin"] == "nr-softmodem"
    assert config_fib_rnd["flexric_dir"] == "openair2/E2AP/flexric"
    assert config_fib_rnd["flexric_build_dir"] == "build"
    assert config_fib_rnd["xapp_beam_management_bin"] == "oaibox_xapp_beam_management"
    assert config_fib_rnd["local_beam_table_csv_location"] == "./CustomBatchBeams.csv"
    assert config_fib_rnd["du_beam_table_csv_location"] == "radio/USRP/setup/CustomBatchBeams.csv"
    assert config_fib_rnd["beam_template_file_jsonl"] == "tests/conf/fib_rnd/beam_pattern.fib64.jsonl"
    assert config_fib_rnd["beam_control_program_jsonl"] == "tests/conf/fib_rnd/beam_control_program.64.rnd.jsonl"
    assert config_fib_rnd["theta_min_d"] == 0
    assert config_fib_rnd["theta_max_d"] == 25
    assert config_fib_rnd["pattern_rotation_angle"] == 0
    assert config_fib_rnd["center_angle_theta"] == 0
    assert config_fib_rnd["center_angle_phi"] == 0
    assert config_fib_rnd["pattern_rotation_angle"] == 0
    assert config_fib_rnd["random_seed"] == 1234567890

    # 型チェック
    assert type(config_lin_rnd["home_dir"]) == str and config_lin_rnd["home_dir"] == "/home/user"
    assert type(config_lin_rnd["oai_dir"]) == str
    assert type(config_lin_rnd["exec_dir"]) == str
    assert type(config_lin_rnd["softmodem_bin"]) == str
    assert type(config_lin_rnd["flexric_dir"]) == str
    assert type(config_lin_rnd["flexric_build_dir"]) == str
    assert type(config_lin_rnd["xapp_beam_management_bin"]) == str
    assert type(config_lin_rnd["xapp_beam_management_bin_path"]) == str
    assert type(config_lin_rnd["local_beam_table_csv_location"]) == str
    assert type(config_lin_rnd["du_beam_table_csv_location"]) == str
    assert type(config_lin_rnd["beam_template_file_jsonl"]) == str
    assert type(config_lin_rnd["beam_control_program_jsonl"]) == str
    assert type(config_lin_rnd["theta_max_d"]) == int
    assert type(config_lin_rnd["theta_min_d"]) == int
    assert type(config_lin_rnd["theta_min"]) == float
    assert type(config_lin_rnd["theta_max"]) == float
    assert type(config_lin_rnd["pattern_rotation_angle"]) == float
    assert type(config_lin_rnd["center_angle_theta"]) == float
    assert type(config_lin_rnd["center_angle_phi"]) == float
    assert type(config_lin_rnd["random_seed"]) == int

    # 値の確認 - lin_rnd_conf.json
    assert config_lin_rnd["home_dir"] == "/home/user"
    assert config_lin_rnd["oai_dir"] == "openairinterface5g"
    assert config_lin_rnd["exec_dir"] == "cmake_targets/ran_build/build"
    assert config_lin_rnd["softmodem_bin"] == "nr-softmodem"
    assert config_lin_rnd["flexric_dir"] == "openair2/E2AP/flexric"
    assert config_lin_rnd["flexric_build_dir"] == "build"
    assert config_lin_rnd["xapp_beam_management_bin"] == "oaibox_xapp_beam_management"
    assert config_lin_rnd["local_beam_table_csv_location"] == "./CustomBatchBeams.csv"
    assert config_lin_rnd["du_beam_table_csv_location"] == "radio/USRP/setup/CustomBatchBeams.csv"
    assert config_lin_rnd["beam_template_file_jsonl"] == "tests/conf/lin_rnd/beam_pattern.lin51.jsonl"
    assert config_lin_rnd["beam_control_program_jsonl"] == "tests/conf/lin_rnd/beam_control_program.51.rnd.jsonl"
    assert config_lin_rnd["theta_min_d"] == 0
    assert config_lin_rnd["theta_max_d"] == 25
    assert config_lin_rnd["pattern_rotation_angle"] == 0
    assert config_lin_rnd["center_angle_theta"] == 0
    assert config_lin_rnd["center_angle_phi"] == 0
    assert config_lin_rnd["pattern_rotation_angle"] == 0
    assert config_lin_rnd["random_seed"] == 1234567890

    # 型チェック
    assert type(config_lin_seq["home_dir"]) == str and config_lin_seq["home_dir"] == "/home/user"
    assert type(config_lin_seq["oai_dir"]) == str
    assert type(config_lin_seq["exec_dir"]) == str
    assert type(config_lin_seq["softmodem_bin"]) == str
    assert type(config_lin_seq["flexric_dir"]) == str
    assert type(config_lin_seq["flexric_build_dir"]) == str
    assert type(config_lin_seq["xapp_beam_management_bin"]) == str
    assert type(config_lin_seq["xapp_beam_management_bin_path"]) == str
    assert type(config_lin_seq["local_beam_table_csv_location"]) == str
    assert type(config_lin_seq["du_beam_table_csv_location"]) == str
    assert type(config_lin_seq["beam_template_file_jsonl"]) == str
    assert type(config_lin_seq["beam_control_program_jsonl"]) == str
    assert type(config_lin_seq["theta_max_d"]) == int
    assert type(config_lin_seq["theta_min_d"]) == int
    assert type(config_lin_seq["theta_min"]) == float
    assert type(config_lin_seq["theta_max"]) == float
    assert type(config_lin_seq["pattern_rotation_angle"]) == float
    assert type(config_lin_seq["center_angle_theta"]) == float
    assert type(config_lin_seq["center_angle_phi"]) == float
    assert type(config_lin_seq["random_seed"]) == int

    # 値の確認 - lin_seq.conf.json
    assert config_lin_seq["home_dir"] == "/home/user"
    assert config_lin_seq["oai_dir"] == "openairinterface5g"
    assert config_lin_seq["exec_dir"] == "cmake_targets/ran_build/build"
    assert config_lin_seq["softmodem_bin"] == "nr-softmodem"
    assert config_lin_seq["flexric_dir"] == "openair2/E2AP/flexric"
    assert config_lin_seq["flexric_build_dir"] == "build"
    assert config_lin_seq["xapp_beam_management_bin"] == "oaibox_xapp_beam_management"
    assert config_lin_seq["local_beam_table_csv_location"] == "./CustomBatchBeams.csv"
    assert config_lin_seq["du_beam_table_csv_location"] == "radio/USRP/setup/CustomBatchBeams.csv"
    assert config_lin_seq["beam_template_file_jsonl"] == "tests/conf/lin_seq/beam_pattern.lin51.jsonl"
    assert config_lin_seq["beam_control_program_jsonl"] == "tests/conf/lin_seq/beam_control_program.bidirectional51.seq.jsonl"
    assert config_lin_seq["theta_min_d"] == 0
    assert config_lin_seq["theta_max_d"] == 25
    assert config_lin_seq["pattern_rotation_angle"] == 0
    assert config_lin_seq["center_angle_theta"] == 0
    assert config_lin_seq["center_angle_phi"] == 0
    assert config_lin_seq["pattern_rotation_angle"] == 0
    assert config_lin_seq["random_seed"] == 1234567890

def test_get_beam_template_from_json():
    config_fib_rnd = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    config_lin_rnd = arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    config_lin_seq = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    # get_beam_template_from_json()自体の動作検証
    assert get_beam_template_from_json(config_fib_rnd)
    assert get_beam_template_from_json(config_lin_rnd)
    assert get_beam_template_from_json(config_lin_seq)

    beam_fib_rnd_lst = get_beam_template_from_json(config_fib_rnd)
    beam_lin_rnd_lst = get_beam_template_from_json(config_lin_rnd)
    beam_lin_seq_lst = get_beam_template_from_json(config_lin_seq)

    # Test that the returned list: beam_fib_rnd_lst
    assert len(beam_fib_rnd_lst) == 1
    assert beam_fib_rnd_lst[0]['type'] == BeamPattern.FIBONACCI
    assert beam_fib_rnd_lst[0]['start_point']['r'] == 0.0
    assert beam_fib_rnd_lst[0]['start_point']['theta'] == 0.0
    assert beam_fib_rnd_lst[0]['steps'] == 64

    # Test that the returned list: beam_lin_rnd_lst
    assert len(beam_lin_rnd_lst) == 3
    # First template: CONST type
    assert beam_lin_rnd_lst[0]['type'] == BeamPattern.CONST
    assert beam_lin_rnd_lst[0]['start_point']['r'] == 0.0
    assert beam_lin_rnd_lst[0]['start_point']['theta'] == 0.0
    assert beam_lin_rnd_lst[0]['end_point']['r'] == 0.0
    assert beam_lin_rnd_lst[0]['end_point']['theta'] == 0.0
    assert beam_lin_rnd_lst[0]['steps'] == -1
    # Second template: LINEAR type
    assert beam_lin_rnd_lst[1]['type'] == BeamPattern.LINEAR
    assert beam_lin_rnd_lst[1]['start_point']['r'] == 0.04
    assert beam_lin_rnd_lst[1]['start_point']['theta'] == 0.0
    assert beam_lin_rnd_lst[1]['end_point']['r'] == 1.0
    assert beam_lin_rnd_lst[1]['end_point']['theta'] == 0.0
    assert beam_lin_rnd_lst[1]['steps'] == 25
    # Third template: LINEAR type (opposite direction)
    assert beam_lin_rnd_lst[2]['type'] == BeamPattern.LINEAR
    assert beam_lin_rnd_lst[2]['start_point']['r'] == 0.04
    assert beam_lin_rnd_lst[2]['start_point']['theta'] == math.pi
    assert beam_lin_rnd_lst[2]['end_point']['r'] == 1.0
    assert beam_lin_rnd_lst[2]['end_point']['theta'] == math.pi
    assert beam_lin_rnd_lst[2]['steps'] == 25

    # Test that the returned list: beam_lin_seq_lst
    assert len(beam_lin_seq_lst) == 3
    # First template: CONST type
    assert beam_lin_seq_lst[0]['type'] == BeamPattern.CONST
    assert beam_lin_seq_lst[0]['start_point']['r'] == 0.0
    assert beam_lin_seq_lst[0]['start_point']['theta'] == 0.0
    assert beam_lin_seq_lst[0]['end_point']['r'] == 0.0
    assert beam_lin_seq_lst[0]['end_point']['theta'] == 0.0
    assert beam_lin_seq_lst[0]['steps'] == -1
    # Second template: LINEAR type
    assert beam_lin_seq_lst[1]['type'] == BeamPattern.LINEAR
    assert beam_lin_seq_lst[1]['start_point']['r'] == 0.04
    assert beam_lin_seq_lst[1]['start_point']['theta'] == 0.0
    assert beam_lin_seq_lst[1]['end_point']['r'] == 1.0
    assert beam_lin_seq_lst[1]['end_point']['theta'] == 0.0
    assert beam_lin_seq_lst[1]['steps'] == 25
    # Third template: LINEAR type (opposite direction)
    assert beam_lin_seq_lst[2]['type'] == BeamPattern.LINEAR
    assert beam_lin_seq_lst[2]['start_point']['r'] == 0.04
    assert beam_lin_seq_lst[2]['start_point']['theta'] == math.pi
    assert beam_lin_seq_lst[2]['end_point']['r'] == 1.0
    assert beam_lin_seq_lst[2]['end_point']['theta'] == math.pi
    assert beam_lin_seq_lst[2]['steps'] == 25

def test_get_beam_control_program_from_json():
    config_fib_rnd = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    config_lin_rnd = arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    config_lin_seq = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    # get_beam_control_program_from_json()自体の動作検証
    assert get_beam_control_program_from_json(config_fib_rnd)
    assert get_beam_control_program_from_json(config_lin_rnd)
    assert get_beam_control_program_from_json(config_lin_seq)

    beam_control_program_fib_rnd_lst = get_beam_control_program_from_json(config_fib_rnd)
    beam_control_program_lin_rnd_lst = get_beam_control_program_from_json(config_lin_rnd)
    beam_control_program_lin_seq_lst = get_beam_control_program_from_json(config_lin_seq)

    # Verify return type is a list of beam_control_program_t
    assert isinstance(beam_control_program_fib_rnd_lst, list)
    for item in beam_control_program_fib_rnd_lst:
        assert isinstance(item, dict)
        assert 'start_id' in item
        assert 'end_id' in item
        assert 'step' in item
        assert 'method' in item
        assert 'iters' in item
        assert 'reduction' in item
        assert 'duration' in item
    
    # Verify the first item matches expected values
    expected_first = {
        'start_id': 1,
        'end_id': 1,
        'step': -1,
        'method': BeamControlMethod.CONST,
        'iters': -1,
        'reduction': False,
        'duration': 10
    }
    
    assert beam_control_program_fib_rnd_lst[0] == expected_first
    
    # Verify the third item (RANDOM method) matches expected values
    expected_third = {
        'start_id': 1,
        'end_id': 64,
        'step': -1,
        'method': BeamControlMethod.RANDOM,
        'iters': 3,
        'reduction': False,
        'duration': 5
    }
    
    assert beam_control_program_fib_rnd_lst[2] == expected_third
    
    # Verify total number of items
    assert len(beam_control_program_fib_rnd_lst) == 5

    # Verify return type is a list of beam_control_program_t
    assert isinstance(beam_control_program_lin_rnd_lst, list)
    for item in beam_control_program_lin_rnd_lst:
        assert isinstance(item, dict)
        assert 'start_id' in item
        assert 'end_id' in item
        assert 'step' in item
        assert 'method' in item
        assert 'iters' in item
        assert 'reduction' in item
        assert 'duration' in item
    
    # Verify the first item matches expected values
    expected_first = {
        'start_id': 1,
        'end_id': 1,
        'step': -1,
        'method': BeamControlMethod.CONST,
        'iters': -1,
        'reduction': False,
        'duration': 10
    }
    
    assert beam_control_program_lin_rnd_lst[0] == expected_first
    
    # Verify the third item (RANDOM method) matches expected values
    expected_third = {
        'start_id': 1,
        'end_id': 51,
        'step': -1,
        'method': BeamControlMethod.RANDOM,
        'iters': 3,
        'reduction': False,
        'duration': 5
    }
    
    assert beam_control_program_lin_rnd_lst[2] == expected_third
    
    # Verify total number of items
    assert len(beam_control_program_lin_rnd_lst) == 5

     # Verify return type is a list of beam_control_program_t
    assert isinstance(beam_control_program_lin_seq_lst, list)
    for item in beam_control_program_lin_seq_lst:
        assert isinstance(item, dict)
        assert 'start_id' in item
        assert 'end_id' in item
        assert 'step' in item
        assert 'method' in item
        assert 'iters' in item
        assert 'reduction' in item
        assert 'duration' in item
    
    # Verify the first item matches expected values
    expected_first = {
        'start_id': 1,
        'end_id': 1,
        'step': -1,
        'method': BeamControlMethod.CONST,
        'iters': -1,
        'reduction': False,
        'duration': 10
    }
    
    assert beam_control_program_lin_seq_lst[0] == expected_first
    
    # Verify the third item (SEQUENTIAL method) matches expected values
    expected_third = {
        'start_id': 2,
        'end_id': 26,
        'step': 1,
        'method': BeamControlMethod.SEQUENTIAL,
        'iters': 1,
        'reduction': False,
        'duration': 10
    }
    
    assert beam_control_program_lin_seq_lst[2] == expected_third
    
    # Verify the fourth item (reverse SEQUENTIAL method) matches expected values
    expected_fourth = {
        'start_id': 26,
        'end_id': 2,
        'step': 1,
        'method': BeamControlMethod.SEQUENTIAL,
        'iters': 1,
        'reduction': False,
        'duration': 10
    }
    
    assert beam_control_program_lin_seq_lst[3] == expected_fourth
    
    # Verify total number of items
    assert len(beam_control_program_lin_seq_lst) == 9