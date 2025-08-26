    
from typing import TypedDict, Generator
from math import pi as PI
PI_D = 180


dB_t = int

class unit_disc_coord_t(TypedDict):
    r: float
    theta: float

unit_disc_coord_generator = Generator[unit_disc_coord_t, None, None]

class unit_hemisphere_coord_t(TypedDict):
    phi: float
    theta: float