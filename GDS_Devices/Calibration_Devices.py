from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.resonator import RingResonator
from gdshelpers.parts.text import Text
from gdshelpers.parts.marker import SquareMarker
from gdshelpers.parts.splitter import DirectionalCoupler
from gdshelpers.parts.port import Port
from gdshelpers.parts.spiral import Spiral
import numpy as np

class ring_resonator:

    def __init__(self, name, wg_width, pitch=127, bending_radius = 100, photonic_layer = 1, info_layer = 2, label_layer = 3, region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.bendin_radius = bending_radius
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer

    def create(self,x,y,coupler_params, gap ,  radius, angle = 0,):

        coupler_params["width"] = self.wg_width
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)

        wg1 = Waveguide.make_at_port(outcoupler.port)
        wg1.add_left_bend(self.bendin_radius)
        wg1.add_route_single_circle_to_port(incoupler.port,self.bendin_radius)

        RR = RingResonator((x+self.pitch/2, y+self.bendin_radius), angle = angle, gap = gap, radius = radius, width = self.wg_width)

        devices = geometric_union([incoupler, outcoupler, wg1, RR])

        txt = ('gap: %s um\nradius: %s') \
              % (np.around(gap,3), radius)  #
        device_info = Text(origin=(x + self.pitch / 2, y), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 30), height=20, text=self.name, alignment='center-bottom')

        cell = Cell("Resonator_%s" % (self.name))
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_region_layer(self.region_layer)

        return cell

class global_markers:

    def __init__(self, name , marker_distance =200,  global_marker_layer = 5):
        self.marker_distance = marker_distance
        self.global_marker_layer = global_marker_layer
        self.name = name

    def create(self, dimension_x, dimension_y, size = 20):
        cell = Cell('global markers %s' % self.name)
        positions_LL = [(0, 0), (self.marker_distance, 0), (2*self.marker_distance, 0), (3*self.marker_distance, 0), (0, self.marker_distance), (0, 2*self.marker_distance), (0, 3*self.marker_distance)]
        positions_Ul = [(0, dimension_y), (self.marker_distance, dimension_y), (2*self.marker_distance, dimension_y), (3*self.marker_distance, dimension_y),
                        (0, dimension_y - self.marker_distance), (0, dimension_y - 2*self.marker_distance), (0, dimension_y - 3*self.marker_distance)]
        positions_UR = [(dimension_x, dimension_y), (dimension_x - self.marker_distance, dimension_y), (dimension_x - 2*self.marker_distance, dimension_y),
                        (dimension_x - 3*self.marker_distance, dimension_y), (dimension_x, dimension_y - self.marker_distance),
                        (dimension_x, dimension_y - 2*self.marker_distance), (dimension_x, dimension_y - 3*self.marker_distance)]
        positions_LR = [(dimension_x, 0), (dimension_x - self.marker_distance, 0), (dimension_x - 2*self.marker_distance, 0), (dimension_x - 3*self.marker_distance, 0),
                        (dimension_x, self.marker_distance), (dimension_x, 2*self.marker_distance), (dimension_x, 3*self.marker_distance)]

        markers_LL = [SquareMarker.make_marker(position, size) for position in positions_LL]
        markers_UL = [SquareMarker.make_marker(position, size) for position in positions_Ul]
        markers_UR = [SquareMarker.make_marker(position, size) for position in positions_UR]
        markers_LR = [SquareMarker.make_marker(position, size) for position in positions_LR]

        cell.add_to_layer(self.global_marker_layer, geometric_union(markers_LL), )
        cell.add_to_layer(self.global_marker_layer, geometric_union(markers_UL), )
        cell.add_to_layer(self.global_marker_layer, geometric_union(markers_UR), )
        cell.add_to_layer(self.global_marker_layer, geometric_union(markers_LR), )
        return cell

class conected_coupler:

    def __init__(self, name, wg_width, pitch=127, bending_radius = 100, photonic_layer = 1, info_layer = 2, label_layer = 3,region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.bendin_radius = bending_radius
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer

    def create(self, x, y,coupler_params, marker = False):

        #sweep_coupler_params = {
        #    'width':self.wg_width,
        #    'full_opening_angle': self.std_coupler_params['full_opening_angle'],
        #    'grating_period': self.std_coupler_params['grating_period'],
        #    'grating_ff': self.std_coupler_params['grating_ff'],
        #    'n_gratings': self.std_coupler_params['n_gratings'],
        #    'ap_max_ff': self.std_coupler_params['ap_max_ff'],
        #    'n_ap_gratings': self.std_coupler_params['n_ap_gratings'],
        #    'taper_length': self.std_coupler_params['taper_length']
        #}
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)

        wg1 = Waveguide.make_at_port(incoupler.port)
        wg1.add_straight_segment(20, final_width=self.wg_width)
        wg1.add_right_bend(125, np.pi/2)

        wg2 = Waveguide.make_at_port(outcoupler.port)
        wg2.add_straight_segment(20, final_width=self.wg_width)

        wg1.add_route_single_circle_to_port(wg2.current_port)

        txt = ('n_grat: %s um\nangle: %s') \
             % (coupler_params['n_ap_gratings'], np.around(coupler_params['full_opening_angle'],2))  #
        device_info = Text(origin=(x + self.pitch / 2, y), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 30), height=20, text=self.name, alignment='center-bottom')
        devices = geometric_union([incoupler, outcoupler, wg1, wg2])
        cell = Cell("Coupler_%s" % (self.name))

        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer , device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)

        if marker:
            if isinstance(marker, int):
                for number in range(marker):
                    coordinates = [(x+self.pitch/2, y-40), (x-25, y+130), (x+270, y+130)]
                    markers = []
                    for i in coordinates:
                        m = SquareMarker(i, 20+10*number)
                        markers.append(m)
                    cell.add_to_layer(11+number, markers)
            else:
                coordinates =[(x+self.pitch/2, y-40), (x-25, y+130), (x+270, y+130)]
                markers = []
                for i in coordinates:
                    m = SquareMarker(i, 20)
                    markers.append(m)
                cell.add_to_layer(11 , markers)


        return cell

class directional_coupler:

    def __init__(self, name, wg_width, pitch=127*2, photonic_layer=1, info_layer=2, label_layer=3,region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer

    def create(self, x,y,coupler_params, gap, length, width, bending_radius=100):
        incoupler1 = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        incoupler2 = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)
        outcoupler1 = GratingCoupler.make_traditional_coupler((x + 2 * self.pitch, y), **coupler_params)
        outcoupler2 = GratingCoupler.make_traditional_coupler((x + 3 * self.pitch, y), **coupler_params)

        # DC = DirectionalCoupler.make_at_port(port=wg1.current_port, length=30, gap=0.0, bend_radius=100, which=0)
        DC = DirectionalCoupler((x + 1.5 * self.pitch + 39.197 + gap / 2, y + 200), np.pi / 2, width, length, gap, 100,
                                bend_angle=0.6283185307179586)

        wg1 = Waveguide.make_at_port(outcoupler1.port)
        wg1.add_bezier_to_port(DC.left_ports[0], bending_radius)

        wg2 = Waveguide.make_at_port(incoupler2.port)
        wg2.add_bezier_to_port(DC.left_ports[1], bending_radius)

        wg3 = Waveguide.make_at_port(DC.right_ports[0])
        wg3.add_right_bend(bending_radius)
        wg3.add_route_single_circle_to_port(outcoupler2.port, bending_radius)

        wg4 = Waveguide.make_at_port(DC.right_ports[1])
        wg4.add_left_bend(bending_radius)
        wg4.add_route_single_circle_to_port(incoupler1.port, bending_radius)

        txt = ('length: %s um\ngap: %s um\nwidth: %s um') \
              % (length, gap, width)  #
        device_info = Text(origin=(x + 2.5 * self.pitch, y + 50), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 80), height=20, text=self.name, alignment='center-bottom')
        devices = geometric_union([incoupler1, outcoupler1, incoupler2, outcoupler2, wg1, wg2, wg3, wg4, DC])
        # print(spiral_2.length)
        cell = Cell("Spiral_%s" % (self.name))
        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)

        return cell

class Spiral_with_coupler:
    def __init__(self, name, wg_width, pitch=2*127, photonic_layer=1, info_layer=2, label_layer=3, region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer
        self.pitch = pitch

    def create(self, x, y, coupler_params, number_of_roundtrips=2, bending = 100, marker = False):
        inner_gap = bending
        gap = 3 *  self.wg_width
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        wg1 = Waveguide.make_at_port(incoupler.port)

        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)
        SpiralPort = Port((x + self.pitch / 2, y + 350), 0,  self.wg_width)
        spiral_2 = Spiral.make_at_port(SpiralPort, num=number_of_roundtrips, gap=gap, inner_gap=inner_gap)
        wg1.add_route_single_circle_to_port(spiral_2.in_port, 80)
        # spiral_1 = Spiral.make_at_port(wg1.port, num=number_of_roundtrips, gap=gap, inner_gap=inner_gap)
        wg2 = Waveguide.make_at_port(spiral_2.out_port)
        wg2.add_route_single_circle_to_port(outcoupler.port, 80)
        txt = ('length: %s um\nwidth: %s um\nbending_r: %s') \
              % (np.around(spiral_2.length + wg1.length + wg2.length, 0), np.around( self.wg_width, 2), np.around(bending, 2))  #
        device_info = Text(origin=(x + self.pitch / 2, y), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 30), height=20, text=self.name, alignment='center-bottom')
        devices = geometric_union([incoupler, outcoupler, wg1, wg2, spiral_2])

        cell = Cell("Spiral_%s" % (self.name))
        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)

        if marker:
            if isinstance(marker, int):
                for number in range(marker):
                    coordinates = [(x+self.pitch/2, y-40), (x-30, y+337), (x+280, y+337)]
                    markers = []
                    for i in coordinates:
                        m = SquareMarker(i, 20+10*number)
                        markers.append(m)
                    cell.add_to_layer(11+number, markers)
            else:
                coordinates = [(x+self.pitch/2, y-40), (x-30, y+337), (x+280, y+337)]
                markers = []
                for i in coordinates:
                    m = SquareMarker(i, 20)
                    markers.append(m)
                cell.add_to_layer(11 , markers)


        return cell

class rotated_directional_coupler:
    def __init__(self, name, wg_width, pitch=127, photonic_layer=1, info_layer=2, label_layer=3, region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer
        self.pitch = pitch

    def create(self, x, y, coupler_params, coupler_sep, coupler_length, marker = False):
        x_DC_length = 80
        y_DC_length = 100 / 2.0 - coupler_sep / 2.0 - self.wg_width / 2.0
        center_x = x + self.pitch*3
        center_y = y+170

        lower_DC_WG = Waveguide.make_at_port(Port((center_x - coupler_length/2- x_DC_length, center_y - 50),0, self.wg_width))
        upper_DC_WG = Waveguide.make_at_port(Port((center_x -  coupler_length/2 - x_DC_length, center_y + 50),0, self.wg_width))

        coupler1 = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        wg1 = Waveguide.make_at_port(coupler1.port)
        wg1.add_straight_segment(20, final_width=self.wg_width)

        coupler2 = GratingCoupler.make_traditional_coupler((x+self.pitch, y), **coupler_params)
        wg2 = Waveguide.make_at_port(coupler2.port)
        wg2.add_straight_segment(20, final_width=self.wg_width)

        coupler3 = GratingCoupler.make_traditional_coupler((x+5*self.pitch, y), **coupler_params)
        wg3 = Waveguide.make_at_port(coupler3.port)
        wg3.add_straight_segment(20, final_width=self.wg_width)

        coupler4 = GratingCoupler.make_traditional_coupler((x+6*self.pitch, y), **coupler_params)
        wg4 = Waveguide.make_at_port(coupler4.port)
        wg4.add_straight_segment(20, final_width=self.wg_width)

        upper_DC_WG.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * +y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * +y_DC_length))
        upper_DC_WG.add_straight_segment(coupler_length)
        upper_DC_WG.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))

        lower_DC_WG.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))
        lower_DC_WG.add_straight_segment(coupler_length)
        lower_DC_WG.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * +y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * +y_DC_length))

        wg1.add_route_single_circle_to_port(Port((center_x - coupler_length/2- x_DC_length, center_y + 50),0, self.wg_width).inverted_direction,100)
        wg2.add_route_single_circle_to_port(
            Port((center_x - coupler_length / 2 - x_DC_length, center_y - 50), 0, self.wg_width).inverted_direction,100)
        wg3.add_route_single_circle_to_port(lower_DC_WG.current_port,100)
        wg4.add_route_single_circle_to_port(upper_DC_WG.current_port,100)

        cell = Cell(self.name)

        txt = ('gap: %s um\nlength: %s um') \
              % (np.around(coupler_sep, 2), np.around(coupler_length, 2),)

        devices = geometric_union([coupler1, coupler2, coupler3, coupler4, lower_DC_WG, upper_DC_WG, wg1, wg2, wg3, wg4])
        device_info = Text(origin=(x + 3*self.pitch , y-30), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + 3*self.pitch , y + 30), height=20, text="rotated DC %s" %self.name, alignment='center-bottom')

        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)

        if marker:
            if isinstance(marker, int):
                for number in range(marker):
                    coordinates = [(x + self.pitch / 2+30, y +150), (x +230, y + 40), (x + 670, y + 150)]
                    markers = []
                    for i in coordinates:
                        m = SquareMarker(i, 20+10*number)
                        markers.append(m)
                    cell.add_to_layer(11+number, markers)
            else:
                coordinates = [(x + self.pitch / 2, y +100), (x +230, y + 40), (x + 580, y + 100)]
                markers = []
                for i in coordinates:
                    m = SquareMarker(i, 20)
                    markers.append(m)
                cell.add_to_layer(11 , markers)


        return cell


