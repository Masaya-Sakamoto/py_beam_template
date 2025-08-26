from tools.parser import arg_parser, get_beam_template_from_json, get_beam_control_program_from_json

def test_arg_parser():
    # arg_parser()自体の動作検証
    assert arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    assert arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    assert arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    config_fib_rnd = arg_parser("tests/conf/fib_rnd/fib_rnd_conf.json")
    config_lin_rnd = arg_parser("tests/conf/lin_rnd/lin_rnd_conf.json")
    config_lin_seq = arg_parser("tests/conf/lin_seq/lin_seq.conf.json")

    # 型チェック
    assert type(config_fib_rnd["home_dir"]) == str
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
    assert type(config_fib_rnd["pattern_rotation"]) == float
    assert type(config_fib_rnd["center_angle_theta"]) == float
    assert type(config_fib_rnd["center_angle_phi"]) == float
    assert type(config_fib_rnd["random_seed"]) == int

    assert type(config_lin_rnd["home_dir"]) == str
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
    assert type(config_lin_rnd["pattern_rotation"]) == float
    assert type(config_lin_rnd["center_angle_theta"]) == float
    assert type(config_lin_rnd["center_angle_phi"]) == float
    assert type(config_lin_rnd["random_seed"]) == int

    assert type(config_lin_seq["home_dir"]) == str
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
    assert type(config_lin_seq["pattern_rotation"]) == float
    assert type(config_lin_seq["center_angle_theta"]) == float
    assert type(config_lin_seq["center_angle_phi"]) == float
    assert type(config_lin_seq["random_seed"]) == int



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