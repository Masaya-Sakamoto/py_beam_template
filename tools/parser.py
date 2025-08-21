import argparse
from os import getenv
from typing import Any
from pytypes.type_beam import config_file_t, config_t, beam_control_program_t, BeamPattern
from math import pi as PI
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
        'beam_control_program_json': config_f['beam_control_program_json'],
        'beam_pattern': BeamPattern.UNDEFINED,
        'theta_min_d': config_f['theta_min_d'],
        'theta_max_d': config_f['theta_max_d'],
        'theta_min': config_f['theta_min_d']*PI/180,
        'theta_max': config_f['theta_max_d']*PI/180,
        'pattern_rotation': config_f['pattern_rotation']*PI/180,
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
    if config_f["beam_pattern"] == 'linear':
        config["beam_pattern"] = BeamPattern.LINEAR
    elif config_f["beam_pattern"] == 'fibonacci':
        config["beam_pattern"] = BeamPattern.FIBONACCI
    elif config_f["beam_pattern"] == 'circular':
        config["beam_pattern"] = BeamPattern.CIRCULAR
    # verification logic is not implemented
    return config
        
def parse_beam_control_program_json(json_file: Path) -> list[beam_control_program_t]:
    try:
        with json_file.open('r') as f:
            loaded = []
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

def arg_parser() -> config_t:
    """
    Parse command line arguments and return them as a dictionary.
    """
    args = parse_args()
    conf_f = parse_conf(Path(args.conf))
    return verify_conf(conf_f)

def get_beam_control_program_json(config: config_t) -> list[beam_control_program_t]:
    json_file = Path(config['beam_control_program_json'])
    return parse_beam_control_program_json(json_file)