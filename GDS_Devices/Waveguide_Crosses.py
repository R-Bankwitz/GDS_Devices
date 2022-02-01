from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.port import Port
import numpy as np

class Straight_Waveguide_Cross:
    def __init__(self, wg_width, center_coordinates):
        self.wg_width = wg_width
        self.center_coordinates = center_coordinates
        self.dimensions = (100,100)
        self.ports = dict()

    def create(self):
        left_port = Port((self.center_coordinates[0]-self.dimensions[0]/2, self.center_coordinates[1]), 0, self.wg_width)
        left_waveguide = Waveguide.make_at_port(left_port)
        left_waveguide.add_straight_segment(self.dimensions[0])

        upper_port = Port((self.center_coordinates[0], self.center_coordinates[1]+self.dimensions[1]/2), -np.pi/2,
                         self.wg_width)
        upper_waveguide = Waveguide.make_at_port(upper_port)
        upper_waveguide.add_straight_segment(self.dimensions[0])

        Waveguides = geometric_union([left_waveguide, upper_waveguide])

        #lower_port = upper_waveguide.current_port()
        #right_port = left_waveguide.current_port()

        self.ports["left_port"] = left_port
        self.ports["right_port"] = left_waveguide.current_port
        self.ports["upper_port"] = upper_port
        self.ports["lower_port"] = upper_waveguide.current_port

        print(self.ports)

        return Waveguides


    def left_port(self):
        print("i", self.ports['upper_port'])
        return self.ports['left_port']


    def right_port(self):
        print("i", self.ports['upper_port'])
        return self.ports['right_port']


    def upper_port(self):
        print(self.ports)
        print("i", self.ports['upper_port'])
        return self.ports['upper_port']


    def lower_port(self):
        print("i", self.ports['upper_port'])
        return self.ports['lower_port']

