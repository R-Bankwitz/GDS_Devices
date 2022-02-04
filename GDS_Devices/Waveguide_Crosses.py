from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.text import Text
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

        #print(self.ports)

        return Waveguides


    def left_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['left_port']


    def right_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['right_port']


    def upper_port(self):
        #print(self.ports)
        #print("i", self.ports['upper_port'])
        return self.ports['upper_port']


    def lower_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['lower_port']

class Tapered_Waveguide_Cross:
    def __init__(self, wg_width, center_coordinates):
        self.wg_width = wg_width
        self.center_coordinates = center_coordinates
        self.ports = dict()

    def create(self, taper_length_x, taper_length_y, wg_width_x, wg_width_y, cross_length_x, cross_length_y, dimensions, text = True):
        left_port = Port((self.center_coordinates[0]-dimensions[0]/2, self.center_coordinates[1]), 0, self.wg_width)
        left_waveguide = Waveguide.make_at_port(left_port)
        left_waveguide.add_straight_segment(dimensions[0]/2-cross_length_x/2-taper_length_x)
        left_waveguide.add_straight_segment(taper_length_x, final_width=wg_width_x)
        left_waveguide.add_straight_segment(cross_length_x)
        left_waveguide.add_straight_segment(taper_length_x, final_width=self.wg_width)
        left_waveguide.add_straight_segment(dimensions[0] / 2 - cross_length_x / 2 - taper_length_x)


        upper_port = Port((self.center_coordinates[0], self.center_coordinates[1]+dimensions[1]/2), -np.pi/2,
                         self.wg_width)
        upper_waveguide = Waveguide.make_at_port(upper_port)
        #upper_waveguide.add_straight_segment(self.dimensions[0])

        upper_waveguide.add_straight_segment(dimensions[1] / 2 - cross_length_y / 2 - taper_length_y)
        upper_waveguide.add_straight_segment(taper_length_y, final_width=wg_width_y)
        upper_waveguide.add_straight_segment(cross_length_y)
        upper_waveguide.add_straight_segment(taper_length_y, final_width=self.wg_width)
        upper_waveguide.add_straight_segment(dimensions[1] / 2 - cross_length_y / 2 - taper_length_y)

        Waveguides = geometric_union([left_waveguide, upper_waveguide])

        #lower_port = upper_waveguide.current_port()
        #right_port = left_waveguide.current_port()

        self.ports["left_port"] = left_port
        self.ports["right_port"] = left_waveguide.current_port
        self.ports["upper_port"] = upper_port
        self.ports["lower_port"] = upper_waveguide.current_port

        #print(self.ports)

        tx_x = ('x direction:\n taper length: %s um\ncross wg width: %s um\narm length: %s um') \
               % (np.around(taper_length_x,2), np.around(wg_width_x,2), np.around(cross_length_x,2))
        tx_y = ('y direction:\n taper length: %s um\ncross wg width: %s um\narm length: %s um') \
               % (np.around(taper_length_y,2), np.around(wg_width_y,2), np.around(cross_length_y,2))

        if text:
            txt_x = Text((self.center_coordinates[0] + 50, self.center_coordinates[1] - 20), 20, tx_x, alignment="left-top")
            txt_y = Text((self.center_coordinates[0] - 50, self.center_coordinates[1] + 20), 20, tx_y,alignment="right-bottom")
        else:
            txt_x = None
            txt_y = None

        return Waveguides, txt_x, txt_y


    def left_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['left_port']


    def right_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['right_port']


    def upper_port(self):
        #print(self.ports)
        #print("i", self.ports['upper_port'])
        return self.ports['upper_port']


    def lower_port(self):
        #print("i", self.ports['upper_port'])
        return self.ports['lower_port']

