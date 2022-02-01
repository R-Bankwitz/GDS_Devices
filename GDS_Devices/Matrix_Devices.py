from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.text import Text
from gdshelpers.parts.splitter import Splitter
import GDS_Devices.Waveguide_Crosses
from GDS_Devices.Electrode_Pads import GSG_configuration_probe_pads as GSG_pads
from gdshelpers.parts.splitter import DirectionalCoupler
from gdshelpers.parts.port import Port
from gdshelpers.parts.spiral import Spiral
import numpy as np

class Matix_cell_1x1:

    def __init__(self, name, wg_width, pitch=127, photonic_layer=1, info_layer=2, label_layer=3,region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer
        self.MZI_coordinates = []
        self.MZI_width = 40
        self.MZI_length = 1700
        self.electrode_ports = dict()

    def create_waveguides(self, x,y,coupler_params, Waveguide_Cross):

        #### initialize parameter -> to be variables soon
        MZI_length = self.MZI_length
        cross_size = 100
        coupler_sep = 0.5
        coupler_length = 60
        x_DC_length = 150
        x_DC_length_MZI = 85
        MZI_width = self.MZI_width
        y_DC_length = self.pitch / 2.0 - coupler_sep / 2.0 - self.wg_width / 2.0
        y_DC_length_MZI = MZI_width / 2.0 - coupler_sep / 2.0 - self.wg_width / 2.0

        #create couplers and taper for coupling
        coupler1 = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        wg_coupler1 = Waveguide.make_at_port(coupler1.port)
        wg_coupler1.add_straight_segment(50, final_width=self.wg_width)

        coupler2 = GratingCoupler.make_traditional_coupler((x + 2*self.pitch, y), **coupler_params)
        wg_coupler2 = Waveguide.make_at_port(coupler2.port)
        wg_coupler2.add_straight_segment(50, final_width=self.wg_width)

        coupler3 = GratingCoupler.make_traditional_coupler((x + 3*self.pitch, y), **coupler_params)
        wg_coupler3 = Waveguide.make_at_port(coupler3.port)
        wg_coupler3.add_straight_segment(50, final_width=self.wg_width)

        coupler4 = GratingCoupler.make_traditional_coupler((x + 4*self.pitch, y), **coupler_params)
        wg_coupler4 = Waveguide.make_at_port(coupler4.port)
        wg_coupler4.add_straight_segment(50, final_width=self.wg_width)

        coupler5 = GratingCoupler.make_traditional_coupler((x + 5*self.pitch, y), **coupler_params)
        wg_coupler5 = Waveguide.make_at_port(coupler5.port)
        wg_coupler5.add_straight_segment(50, final_width=self.wg_width)

        coupler6 = GratingCoupler.make_traditional_coupler((x + 7*self.pitch, y), **coupler_params)
        wg_coupler6 = Waveguide.make_at_port(coupler6.port)
        wg_coupler6.add_straight_segment(50, final_width=self.wg_width)

        coupler7 = GratingCoupler.make_traditional_coupler((x + 8*self.pitch, y), **coupler_params)
        wg_coupler7 = Waveguide.make_at_port(coupler7.port)
        wg_coupler7.add_straight_segment(50, final_width=self.wg_width)

        coupler8 = GratingCoupler.make_traditional_coupler((x + 9*self.pitch, y), **coupler_params)
        wg_coupler8 = Waveguide.make_at_port(coupler8.port)
        wg_coupler8.add_straight_segment(50, final_width=self.wg_width)

        coupler9 = GratingCoupler.make_traditional_coupler((x + 11*self.pitch, y), **coupler_params)
        wg_coupler9 = Waveguide.make_at_port(coupler9.port)
        wg_coupler9.add_straight_segment(50, final_width=self.wg_width)

        coupler10 = GratingCoupler.make_traditional_coupler((x + 13*self.pitch, y), **coupler_params)
        wg_coupler10 = Waveguide.make_at_port(coupler10.port)
        wg_coupler10.add_straight_segment(50, final_width=self.wg_width)

        coupler = geometric_union([coupler1, coupler2, coupler3, coupler4, coupler5, coupler6, coupler7, coupler8, coupler9, coupler10])
        coupler_waveguides = geometric_union([wg_coupler1, wg_coupler2, wg_coupler3, wg_coupler4, wg_coupler5, wg_coupler6, wg_coupler7, wg_coupler8, wg_coupler9, wg_coupler10])

        #create left splitter for calibration
        splitter_coupler_2 = Splitter.make_at_root_port(wg_coupler2.current_port, 80, 25)
        left_aligning_wg = Waveguide.make_at_port(splitter_coupler_2.left_branch_port)
        left_aligning_wg.add_left_bend(100)
        left_aligning_wg.add_route_single_circle_to_port(wg_coupler1.current_port, max_bend_strength=100)

        #Waveguide routing
        upper_cross_wg = Waveguide.make_at_port(splitter_coupler_2.right_branch_port)

        #Directional coupler to fed fraction of light into MZI
        left_cross_wg = Waveguide.make_at_port(wg_coupler3.current_port)

        left_cross_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
                                           path_derivative=lambda t: (
                                           x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))
        left_cross_wg.add_straight_segment(coupler_length)
        left_cross_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
                                           path_derivative=lambda t: (
                                           x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))

        # create MZI
        left_MZI_wg = Waveguide.make_at_port(wg_coupler4.current_port)
        left_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
                                  path_derivative=lambda t: (x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))
        left_MZI_wg.add_straight_segment(coupler_length)
        left_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
                                  path_derivative=lambda t: (x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))
        MZI_beginning_coordinates = left_MZI_wg.current_port.origin
        left_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
                                           path_derivative=lambda t: (
                                           x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))
        left_MZI_wg.add_straight_segment(coupler_length)
        left_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length_MZI, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length_MZI),
                                           path_derivative=lambda t: (
                                           x_DC_length_MZI, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length_MZI))


        left_MZI_wg.add_straight_segment(MZI_length)

        left_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length_MZI, .5 * (np.cos(np.pi * t) - 1) * y_DC_length_MZI),
                                           path_derivative=lambda t: (
                                               x_DC_length_MZI, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length_MZI))
        left_MZI_wg.add_straight_segment(coupler_length)
        left_MZI_wg.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))

        right_MZI_wg = Waveguide.make_at_port(wg_coupler5.current_port)
        right_MZI_wg.add_straight_segment(MZI_beginning_coordinates[1]-50)

        right_MZI_wg.add_parameterized_path(path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
                                           path_derivative=lambda t: (
                                               x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))
        right_MZI_wg.add_straight_segment(coupler_length)
        right_MZI_wg.add_parameterized_path(
            path=lambda t: (t * x_DC_length_MZI, .5 * (np.cos(np.pi * t) - 1) * y_DC_length_MZI),
            path_derivative=lambda t: (
                x_DC_length_MZI, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length_MZI))
        right_MZI_wg.add_straight_segment(MZI_length)
        MZI_center = right_MZI_wg.current_port.origin
        MZI_center[0] = MZI_center[0]-MZI_width/2
        print("iii", MZI_center)
        self.MZI_coordinates = MZI_center#(MZI_center[0], MZI_center[1])

        right_MZI_wg.add_parameterized_path(
            path=lambda t: (t * x_DC_length_MZI, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length_MZI),
            path_derivative=lambda t: (
                x_DC_length_MZI, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length_MZI))
        right_MZI_wg.add_straight_segment(coupler_length)
        right_MZI_wg.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))

        right_MZI_wg.add_right_bend(100)
        MZI_end_coordinates = right_MZI_wg.current_port.origin
        right_MZI_wg.add_route_single_circle_to_port(wg_coupler6.current_port,100)

        #Waveguide routing
        left_cross_wg.add_straight_segment(MZI_end_coordinates[1]-410)
        left_cross_wg.add_right_bend(100)

        upper_cross_wg.add_straight_segment(MZI_end_coordinates[1]-30+cross_size/2)
        upper_cross_wg.add_right_bend(100)

        wg_coupler7.add_straight_segment(MZI_length/2)
        wg_coupler8.add_straight_segment(MZI_length / 2)

        #Directional coupler for coupling out of MZI part
        wg_coupler7.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))
        wg_coupler7.add_straight_segment(coupler_length)
        wg_coupler7.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))

        wg_coupler8.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * -y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * -y_DC_length))
        wg_coupler8.add_straight_segment(coupler_length)
        wg_coupler8.add_parameterized_path(
            path=lambda t: (t * x_DC_length, .5 * (np.cos(np.pi * t) - 1) * y_DC_length),
            path_derivative=lambda t: (
                x_DC_length, -np.pi * .5 * np.sin(np.pi * t) * y_DC_length))

        #Waveguide routing
        left_MZI_wg.add_straight_segment(50)
        left_MZI_wg.add_right_bend(100)
        left_MZI_wg.add_route_single_circle_to_port(wg_coupler7.current_port, 100)

        #creation of Waveguide Cross
        Cross_coordinates = (wg_coupler8.current_port.origin[0], left_cross_wg.current_port.origin[1])
        Cross = Waveguide_Cross(self.wg_width, Cross_coordinates)
        C = Cross.create()

        #Waveguide routing
        wg_coupler8.add_route_straight_to_port(Cross.lower_port())
        left_cross_wg.add_route_straight_to_port(Cross.left_port().inverted_direction)
        upper_cross_wg.add_route_single_circle_to_port(Cross.upper_port().inverted_direction)

        #Right Splitter for calibration
        splitter_coupler_9 = Splitter.make_at_root_port(wg_coupler9.current_port, 80, 25)

        #Waveguide routing
        right_aligning_wg = Waveguide.make_at_port(splitter_coupler_9.right_branch_port)
        right_aligning_wg.add_right_bend(100)
        right_aligning_wg.add_route_single_circle_to_port(wg_coupler10.current_port, max_bend_strength=100)
        right_Cross_wg = Waveguide.make_at_port(Cross.right_port())
        right_Cross_wg.add_route_single_circle_to_port(splitter_coupler_9.left_branch_port, 100)


        txt = ('test')
        device_info = Text(origin=(x + 2.5 * self.pitch, y + 50), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 80), height=20, text=self.name, alignment='center-bottom')
        devices = geometric_union([right_Cross_wg, splitter_coupler_9, coupler,coupler_waveguides,splitter_coupler_2, left_aligning_wg, upper_cross_wg, left_cross_wg, left_MZI_wg, right_MZI_wg, wg_coupler7, wg_coupler8, C, right_aligning_wg])
        cell = Cell("1x1_Matrix_%s" % (self.name))
        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)

        return cell

    def get_MZI_coordinates(self):
        return self.MZI_coordinates

    def create_electrodes_and_pads(self):
        signal_pad_width = 38
        ground_pad_width = 100
        electrodes_gap = 2
        cell = Cell("Electrodes")

        MZI_signal_port = Port(self.MZI_coordinates, -np.pi/2, signal_pad_width)
        MZI_signal = Waveguide.make_at_port(MZI_signal_port)
        MZI_signal.add_straight_segment(self.MZI_length)

        self.MZI_coordinates[0] = self.MZI_coordinates[0]+signal_pad_width/2 + electrodes_gap + ground_pad_width/2
        MZI_right_ground_port = Port(self.MZI_coordinates, -np.pi / 2, ground_pad_width)
        MZI_right_ground = Waveguide.make_at_port(MZI_right_ground_port)
        MZI_right_ground.add_straight_segment(self.MZI_length)

        self.MZI_coordinates[0] = self.MZI_coordinates[0] - signal_pad_width  - 2*electrodes_gap - ground_pad_width
        MZI_left_ground_port = Port(self.MZI_coordinates, -np.pi / 2, ground_pad_width)
        MZI_left_ground = Waveguide.make_at_port(MZI_left_ground_port)
        MZI_left_ground.add_straight_segment(self.MZI_length)

        MZI_left_connection_adapter = Waveguide.make_at_port(MZI_left_ground_port.inverted_direction)
        MZI_left_connection_adapter.add_straight_segment(50, final_width=10)
        MZI_left_connection_adapter.add_straight_segment(600, final_width=10)

        MZI_right_connection_adapter = Waveguide.make_at_port(MZI_right_ground_port.inverted_direction)
        MZI_right_connection_adapter.add_straight_segment(50, final_width=10)
        MZI_right_connection_adapter.add_straight_segment(600, final_width=10)

        MZI_center_connection_adapter = Waveguide.make_at_port(MZI_signal_port.inverted_direction)
        MZI_center_connection_adapter.add_straight_segment(50, final_width=10)
        MZI_center_connection_adapter.add_straight_segment(600, final_width=10)

        left_ground_pad = GSG_pads(80,690,[481.5,3500])
        left_pad, contact_pad_ports = left_ground_pad.create()

        self.electrode_ports["MZI_signal_port"] = MZI_signal_port
        self.electrode_ports["MZI_right_ground_port"] = MZI_right_ground_port
        self.electrode_ports["MZI_left_ground_port"] = MZI_left_ground_port

        conection1 = Waveguide.make_at_port(contact_pad_ports["left_pad_port"].inverted_direction)
        conection1.add_route_straight_to_port(MZI_left_connection_adapter.current_port)
#
        conection2 = Waveguide.make_at_port(contact_pad_ports["center_pad_port"].inverted_direction)
        conection2.add_route_straight_to_port(MZI_center_connection_adapter.current_port)
#
        conection3 = Waveguide.make_at_port(contact_pad_ports["right_pad_port"].inverted_direction)
        conection3.add_route_straight_to_port(MZI_right_connection_adapter.current_port)

        devices = geometric_union([MZI_left_ground, MZI_signal,MZI_right_ground, left_pad, conection2, conection1, conection3, MZI_left_connection_adapter,MZI_right_connection_adapter, MZI_center_connection_adapter])#,conection1,conection2, conection3])

        cell.add_to_layer(10,devices)
        return cell