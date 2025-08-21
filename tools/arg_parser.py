import argparse
from os import getenv
from typing import Any
from math import pi as PI

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Beam management script")
    parser.add_argument('--home-dir', type=str, default=getenv('HOME', '/home/user'), help='Home directory path')
    parser.add_argument('--oai-dir', type=str, default='openairinterface5g', help='OpenAirInterface directory')
    parser.add_argument('--executables-dir', type=str, default='cmake_targets/ran_build/build', help='Executables directory')
    parser.add_argument('--softmodem-bin', type=str, default='nr-softmodem', help='Softmodem binary name')
    parser.add_argument('--flexric-dir', type=str, default='openair2/E2AP/flexric', help='FlexRIC directory')
    parser.add_argument('--flexric-build-dir', type=str, default='build', help='FlexRIC build directory')
    parser.add_argument('--xapp-beam-management-bin', type=str, default='oaibox_xapp_beam_management', help='XApp Beam Management binary name')
    parser.add_argument('--local-beam-table-csv-location', type=str, default='./CustomBatchBeams.csv', help='Local Beam Table CSV location')
    parser.add_argument('--beam-switch-interval', type=int, default=20, help='Beam switch interval')
    parser.add_argument('--theta-min', type=int, default=1, help='Minimum theta value in degree')
    parser.add_argument('--theta-max', type=int, default=25, help='Maximum theta value in degree')
    parser.add_argument('--theta-step', type=int, default=1, help='Theta step value in degree')
    parser.add_argument('--pattern-rotation', type=int, default=0, help='Pattern rotation value in degree')
    parser.add_argument('--center-angle-theta', type=float, default=None, help='Center angle theta value in degree')
    parser.add_argument('--center-angle-phi', type=float, default=None, help='Center angle phi value in degree')
    parser.add_argument('--beam-pattern', type=str, choices=['linear', 'fibonacci', 'circular'], default='linear', help='Beam pattern type')
    return parser.parse_args()

def arg_verification(arg:argparse.Namespace) -> dict[str, Any]:
    """
    angle in degrees -> radians
    """
    ret_dict = dict()
    ret_dict['home_dir'] = arg.home_dir
    ret_dict['oai_dir'] = arg.oai_dir
    ret_dict['exec_dir'] = arg.executables_dir
    ret_dict['softmodem_bin'] = arg.softmodem_bin
    ret_dict['flexric_dir'] = arg.flexric_dir
    ret_dict['flexric_build_dir'] = arg.flexric_build_dir
    ret_dict['xapp_beam_management_bin'] = arg.xapp_beam_management_bin
    ret_dict['local_beam_table_csv_location'] = arg.local_beam_table_csv_location
    ret_dict['du_beam_csv_location'] = f"{arg.home_dir}/{arg.oai_dir}/radio/USRP/setup/"
    ret_dict['beam_switch_interval'] = arg.beam_switch_interval
    ret_dict['beam_pattern'] = arg.beam_pattern
    ret_dict['pattern_rotation'] = arg.pattern_rotation * PI / 180
    ret_dict['theta_min'] = arg.theta_min * PI / 180
    if arg.center_angle_theta:
        ret_dict['center_angle_theta'] = arg.center_angle_theta * PI / 180
    if arg.center_angle_phi:
        ret_dict['center_angle_phi'] = arg.center_angle_phi * PI / 180
    if ret_dict['beam_pattern']:
        ret_dict['theta_max'] = arg.theta_max * PI / 180
        ret_dict['theta_step'] = arg.theta_step * PI / 180
    return ret_dict

def arg_parser() -> dict[str, Any]:
    """
    Parse command line arguments and return them as a dictionary.
    """
    args = parse_args()
    return arg_verification(args)