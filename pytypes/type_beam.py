from typing import TypedDict

dB_t = int

class beam_t(TypedDict):
    id: int
    dB: dB_t
    theta: int
    phi: int

class sweep_program_t(TypedDict):
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