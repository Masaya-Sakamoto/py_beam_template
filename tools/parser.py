import argparse
from os import getenv
from typing import Any
from pytypes.type_beam import beam_control_preload_t, config_file_t, config_t
from pytypes.type_beam import beam_control_program_t, beam_template_t, beam_template_file_t
from pytypes.type_beam import BeamPattern, BeamControlMethod
from pytypes.unit import PI, PI_D, unit_disc_coord_file_t, unit_disc_coord_t
import json
from pathlib import Path

DEFAULT_CONFIG_FILE = 'tools/default_val/ctrl_config.default.json'

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Beam control script")
    parser.add_argument('--conf', type=Path, default=DEFAULT_CONFIG_FILE, help='Path to the configuration file')
    return parser.parse_args()

def parse_default_conf() -> config_file_t:
    with open(DEFAULT_CONFIG_FILE, 'r') as f:
        config_f = json.load(f)
    return config_f

def parse_conf(conf_file: Path) -> config_file_t:
    config_f = parse_default_conf()
    with conf_file.open('r') as f:
        update_config_f = json.load(f)
        for key, value in update_config_f.items():
            config_f[key] = value
    return config_f

def verify_conf(config_f: config_file_t) -> config_t:
    config: config_t = {
        'home_dir': config_f['home_dir'],
        'oai_dir': config_f['oai_dir'],
        'exec_dir': config_f['exec_dir'],
        'softmodem_bin': config_f['softmodem_bin'],
        'flexric_dir': config_f['flexric_dir'],
        'flexric_build_dir': config_f['flexric_build_dir'],
        'xapp_beam_management_bin': config_f['xapp_beam_management_bin'],
        'xapp_beam_management_bin_path': '',
        'local_beam_table_csv_location': config_f['local_beam_table_csv_location'],
        'du_beam_table_csv_location': config_f['du_beam_table_csv_location'],
        'beam_template_file_jsonl':config_f['beam_template_file_jsonl'],
        'beam_control_program_jsonl': config_f['beam_control_program_jsonl'],
        'theta_min_d': config_f['theta_min_d'],
        'theta_max_d': config_f['theta_max_d'],
        'theta_min': config_f['theta_min_d']*PI/PI_D,
        'theta_max': config_f['theta_max_d']*PI/PI_D,
        'pattern_rotation_angle': config_f['pattern_rotation_angle_d']*PI/PI_D,
        'center_angle_theta': config_f['center_angle_theta_d']*PI/PI_D,
        'center_angle_phi': config_f['center_angle_phi_d']*PI/PI_D,
        'random_seed': config_f['random_seed']
    }
    # xapp_beam_management_bin_path
    config["xapp_beam_management_bin_path"] = f"\
    {config['home_dir']}/\
    {config['oai_dir']}/\
    {config['flexric_dir']}/\
    {config['flexric_build_dir']}/\
    examples/xApp/oaibox/\
    {config['xapp_beam_management_bin']}\
    "
    # verification logic is not implemented
    return config
        
def parse_beam_control_program_json(json_file: Path) -> list[beam_control_preload_t]:
    try:
        with json_file.open('r') as f:
            loaded:list[beam_control_preload_t] = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                try:
                    loaded.append(json.loads(line))
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON format in line: {line}")
            return loaded
    except FileNotFoundError:
        raise FileNotFoundError(f"File {json_file} not found.")
    
def parse_beam_template_json(json_file:Path) -> list[beam_template_file_t]:
    try:
        with json_file.open('r') as f:
            loaded:list[beam_template_file_t] = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                try:
                    loaded.append(json.loads(line))
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON format in line: {line}")
            return loaded
    except FileNotFoundError:
        raise FileNotFoundError(f"File {json_file} not found.")

def arg_parser(set_config_file_path:str|None=None) -> config_t:
    """
    Parse command line arguments and return them as a dictionary.
    """
    conf_path = None
    if set_config_file_path:
        conf_path = Path(set_config_file_path)
    else:
        args = parse_args()
        conf_path = Path(args.conf)
    if not conf_path:
        raise ValueError("conf_pathが設定されませんでした。")
    conf_f = parse_conf(conf_path)
    return verify_conf(conf_f)

def get_beam_control_program_from_json(config: config_t) -> list[beam_control_program_t]:
    json_file = Path(config['beam_control_program_jsonl'])
    preload = parse_beam_control_program_json(json_file)
    bcp_lst = []
    for item in preload:
        bcp: beam_control_program_t = {
            'start_id': item['start_id'],
            'end_id': item['end_id'],
            'step': item['step'],
            'method': BeamControlMethod.from_string(item['method']),
            'iters': item['iters'],
            'reduction': bool(item['reduction']),
            'duration': item['duration']
        }
        bcp_lst.append(bcp)
    return bcp_lst

def data_converter_for_file_unitdisc(point: unit_disc_coord_file_t) -> unit_disc_coord_t:
    return {
        'r': point['r'],
        'theta': point['theta_d'] * PI / PI_D
    }

def get_beam_template_from_json(config: config_t) -> list[beam_template_t]:
    json_file = Path(config['beam_template_file_jsonl'])
    preload = parse_beam_template_json(json_file)
    btp_lst = []
    for item in preload:
        btp: beam_template_t = {
            'type': BeamPattern.from_string(item['type']),
            'start_point': data_converter_for_file_unitdisc(item['start_point']),
            'end_point': data_converter_for_file_unitdisc(item['end_point']),
            'steps': item['steps']
        }
        btp_lst.append(btp)
    return btp_lst