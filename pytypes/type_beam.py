from typing import TypedDict

dB_t = int

class beam_t(TypedDict):
    id: int
    dB: dB_t
    theta: int
    phi: int

class beam_control_program_t(TypedDict):
    start_id: int
    end_id: int
    step: int
    method: int
    iters: int
    reduction: int
    duration: int

class beam_sweeping_t(TypedDict):
    id: int
    dB: dB_t
    theta: int
    phi: int
    duration: int

class beam_str_t(TypedDict):
    TX: str
    RX: str

class args_t(TypedDict):
    config_file: str

class config_t(TypedDict):
    home_dir: str
    oai_dir: str
    exec_dir: str
    softmodem_bin: str
    flexric_dir: str
    flexric_build_dir: str
    xapp_beam_management_bin: str
    local_beam_table_csv_location: str
    du_beam_table_csv_location: str
    beam_control_program_json: str # beam_control_program_t
    beam_pattern: str
    theta_min: int
    theta_max: int
    pattern_rotation: int