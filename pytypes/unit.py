    
from typing import TypedDict, Generator
from math import pi as PI
PI_D = 180


dB_t = int

class unit_disc_coord_t(TypedDict):
    r: float
    theta: float

map_unit_disc_coord_t = map[unit_disc_coord_t]

unit_disc_coord_generator = Generator[unit_disc_coord_t, None, None]

class unit_hemisphere_coord_t(TypedDict):
    phi: float
    theta: float

map_unit_hemisphere_coord_t = map[unit_hemisphere_coord_t]