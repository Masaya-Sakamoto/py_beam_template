from typing import TypedDict
from enum import Enum, auto
from unit import dB_t

class beam_t(TypedDict):
    id: int
    dB: dB_t
    theta: int
    phi: int

class BeamControlMethod(Enum):
    UNDEFINED = auto()
    CONST = auto()
    SEQUENTIAL = auto()
    RANDOM = auto()

    @classmethod
    def from_string(cls, method_str: str) -> 'BeamControlMethod':
        """
        Convert a string to a BeamControlMethod enum member.

        Args:
            method_str (str): The name of the BeamControlMethod member as a string.

        Returns:
            BeamControlMethod: The corresponding enum member if found, otherwise BeamControlMethod.UNDEFINED.
        """
        try:
            return cls[method_str]
        except KeyError:
            return cls.UNDEFINED

class BeamPattern(Enum):
    UNDEFINED = auto()
    CONST = auto()
    LINEAR = auto()
    FIBONACCI = auto()
    CIRCULAR = auto()   # not implemented

    @classmethod
    def from_string(cls, pattern_str: str) -> 'BeamPattern':
        """
        Convert a string to a BeamPattern enum member.

        Args:
            pattern_str (str): The name of the BeamPattern member as a string.

        Returns:
            BeamPattern: The corresponding enum member if found, otherwise BeamPattern.UNDEFINED.
        """
        try:
            return cls[pattern_str]
        except KeyError:
            return cls.UNDEFINED

class beam_control_preload_t(TypedDict):
    start_id: int
    end_id: int
    step: int
    method: str
    iters: int
    reduction: int
    duration: int

class beam_control_program_t(TypedDict):
    start_id: int
    end_id: int
    step: int
    method: BeamControlMethod
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

class config_file_t(TypedDict):
    home_dir: str
    oai_dir: str
    exec_dir: str
    softmodem_bin: str
    flexric_dir: str
    flexric_build_dir: str
    xapp_beam_management_bin: str
    local_beam_table_csv_location: str
    du_beam_table_csv_location: str
    beam_control_program_json: str 
    beam_pattern: str
    theta_min_d: int
    theta_max_d: int
    pattern_rotation: int

class config_t(TypedDict):
    home_dir: str
    oai_dir: str
    exec_dir: str
    softmodem_bin: str
    flexric_dir: str
    flexric_build_dir: str
    xapp_beam_management_bin: str
    xapp_beam_management_bin_path: str
    local_beam_table_csv_location: str
    du_beam_table_csv_location: str
    beam_control_program_json: str # beam_control_program_t
    beam_pattern: BeamPattern
    theta_max_d: int
    theta_min_d: int
    theta_min: float
    theta_max: float
    pattern_rotation: float