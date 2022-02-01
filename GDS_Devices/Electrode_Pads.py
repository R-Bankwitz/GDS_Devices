from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.port import Port
from shapely.geometry import Polygon
import numpy as np


class GSG_configuration_probe_pads:
    def __init__(self, pad_width, pad_length, upper_right_left_pad_coordinate, pad_pitch=125):
        self.pad_width = pad_width
        self.upper_right_left_pad_coordinate = upper_right_left_pad_coordinate
        self.pad_length = pad_length
        self.pad_pitch = pad_pitch
        self.ports = dict()

    def create(self):
        left_Pad_port = Port(
            [self.upper_right_left_pad_coordinate[0] - self.pad_width / 2, self.upper_right_left_pad_coordinate[1]], -np.pi / 2,
            self.pad_width).inverted_direction
        left_Pad = Waveguide.make_at_port(left_Pad_port)
        left_Pad.add_straight_segment(self.pad_length + 40)

        center_pad_port = Port([self.upper_right_left_pad_coordinate[0] - self.pad_width / 2 + self.pad_pitch,
                                self.upper_right_left_pad_coordinate[1]], -np.pi / 2, self.pad_width).inverted_direction
        center_Pad = Waveguide.make_at_port(center_pad_port)
        center_Pad.add_straight_segment(self.pad_length)

        print(center_Pad.angle)

        right_pad_port = Port([self.upper_right_left_pad_coordinate[0] - self.pad_width / 2 + 2 * self.pad_pitch,
                               self.upper_right_left_pad_coordinate[1]], -np.pi / 2, self.pad_width).inverted_direction
        right_Pad = Waveguide.make_at_port(right_pad_port)
        right_Pad.add_straight_segment(self.pad_length + 40)
        self.ports["left_pad_port"] = left_Pad_port
        self.ports["center_pad_port"] = center_pad_port
        self.ports["right_pad_port"] = right_pad_port
        outer_corners = [(self.upper_right_left_pad_coordinate[0]-self.pad_width, self.upper_right_left_pad_coordinate[1]+self.pad_length+40),
                         (self.upper_right_left_pad_coordinate[0]-self.pad_width, self.upper_right_left_pad_coordinate[1]+self.pad_width+self.pad_length+40),
                         (self.upper_right_left_pad_coordinate[0] + 2*self.pad_pitch, self.upper_right_left_pad_coordinate[1]+self.pad_width+self.pad_length+40),
                         (self.upper_right_left_pad_coordinate[0] + 2*self.pad_pitch, self.upper_right_left_pad_coordinate[1]+self.pad_length+40)]
        polygon = Polygon(outer_corners)



        Pads = geometric_union([ polygon, left_Pad, center_Pad, right_Pad,])
        return Pads, self.ports
