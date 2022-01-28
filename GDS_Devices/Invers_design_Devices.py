from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.text import Text
from gdshelpers.parts.port import Port
from gdshelpers.parts.splitter import Splitter

class waveguide_integrated_Filter:
    def __init__(self, name, wg_width, pitch=250, photonic_layer=1, info_layer=2, label_layer=3,region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer

    def create(self, x, y, coupler_params, device, device_width, device_length, number_of_filters, filling = 1):
        cell = Cell("Marco_filter_%s" % (self.name))
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + 2*self.pitch, y), **coupler_params)
        calibrationcoupler = GratingCoupler.make_traditional_coupler((x + 4*self.pitch, y), **coupler_params)

        wg1 = Waveguide.make_at_port(outcoupler.port)
        wg1.add_straight_segment(10, final_width=self.wg_width)
        splitter = Splitter.make_at_root_port(wg1.current_port, total_length=30, sep=10)

        wg_calibration = Waveguide.make_at_port(splitter.left_branch_port)
        wg_calibration.add_left_bend(100)
        wg_calibration.add_straight_segment(number_of_filters*device_length)
        wg_calibration.add_route_single_circle_to_port(incoupler.port,100)

        wg_filter = Waveguide.make_at_port(splitter.right_branch_port)
        wg_filter.add_right_bend(100)

        txt = ('number of filters: %s \n'
               'fill factor: %s') \
              % (number_of_filters, filling)  #
        device_info = Text(origin=(x + self.pitch / 2+50, y), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 30), height=20, text=self.name, alignment='center-bottom')

        taper_length = 0
        length_of_filter=4
        for i in range(number_of_filters):
            filter_cell = Cell("filter_%s_%s_%s_%s%s_%s" %(number_of_filters, True,i,x,y, filling))
            filter_cell.add_to_layer(10, device)
            cell.add_cell(filter_cell, origin = (wg_filter.current_port.get_parameters()["origin"][0]+i*device_length,wg_filter.current_port.get_parameters()["origin"][1]-device_width/2))
        Filter_port = Port(((wg_filter.current_port.get_parameters()["origin"][0]+number_of_filters*device_length,wg_filter.current_port.get_parameters()["origin"][1])),0,self.wg_width )
        wg_finish = Waveguide.make_at_port(Filter_port)
        wg_finish.add_route_single_circle_to_port(calibrationcoupler.port,100)
        devices = geometric_union(
            [incoupler, outcoupler, wg1, calibrationcoupler, splitter, wg_filter, wg_calibration, wg_finish])

        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)
        return cell

class waveguide_integrated_Splitter:
    def __init__(self, name, wg_width, pitch=250, photonic_layer=1, info_layer=2, label_layer=3,region_layer = 4):
        self.pitch = pitch
        self.name = name
        self.wg_width = wg_width
        self.photonic_layer = photonic_layer
        self.info_layer = info_layer
        self.label_layer = label_layer
        self.region_layer = region_layer

    def create(self, x, y, coupler_params, device, device_width, device_length, splitting_ratio, filling = 1):
        cell = Cell("Marco_filter_%s" % (self.name))
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)
        calibrationcoupler = GratingCoupler.make_traditional_coupler((x + 2*self.pitch, y), **coupler_params)
        calibrationcoupler_2 = GratingCoupler.make_traditional_coupler((x + 3 * self.pitch, y), **coupler_params)

        wg1 = Waveguide.make_at_port(outcoupler.port)
        wg1.add_straight_segment(10, final_width=self.wg_width)
        splitter = Splitter.make_at_root_port(wg1.current_port, total_length=30, sep=10)

        calibration_outcoupler_wg = Waveguide.make_at_port(incoupler.port)
        calibration_outcoupler_wg.add_straight_segment(10, final_width=self.wg_width)

        calibration_outcoupler_wg = Waveguide.make_at_port(incoupler.port)
        calibration_outcoupler_wg.add_straight_segment(10, final_width=self.wg_width)

        wg_calibration = Waveguide.make_at_port(splitter.left_branch_port)
        wg_calibration.add_left_bend(100)
        wg_calibration.add_route_single_circle_to_port(calibration_outcoupler_wg.current_port,100)

        wg_splitter = Waveguide.make_at_port(splitter.right_branch_port)
        wg_splitter.add_right_bend(100)
        wg_splitter.add_straight_segment(device_length)

        splitter_cell = Cell("splitter_%s%s_%s" % ( x, y, filling))
        splitter_cell.add_to_layer(10, device)
        cell.add_cell(splitter_cell, origin=(wg_splitter.current_port.get_parameters()["origin"][0],
                                           wg_splitter.current_port.get_parameters()["origin"][1] - device_width / 2))

        upper_splitter_port = Port(((wg_splitter.current_port.get_parameters()["origin"][0] + device_length,
                             wg_splitter.current_port.get_parameters()["origin"][1]+0.16+self.wg_width)), 0, self.wg_width)
        lower_splitter_port = Port(((wg_splitter.current_port.get_parameters()["origin"][0] +device_length,
                             wg_splitter.current_port.get_parameters()["origin"][1]-0.16-self.wg_width)), 0, self.wg_width)

        wg_finish = Waveguide.make_at_port(upper_splitter_port)
        wg_finish.add_route_single_circle_to_port(calibrationcoupler_2.port,100)

        wg_finish2 = Waveguide.make_at_port(lower_splitter_port)
        wg_finish2.add_route_single_circle_to_port(calibrationcoupler.port, 100)

        txt = ('fill factor: %s\n'
               'splitting_ratio: %s') \
              % ( filling, splitting_ratio)  #
        device_info = Text(origin=(x + self.pitch / 2, y), height=20, text=txt, alignment='center-bottom')
        device_name = Text(origin=(x + self.pitch / 2, y + 30), height=20, text=self.name, alignment='center-bottom')


        devices = geometric_union(
            [incoupler, outcoupler, wg1, calibrationcoupler, calibrationcoupler_2,wg_calibration,calibration_outcoupler_wg,  splitter, wg_splitter,wg_finish, wg_finish2])

        cell.add_to_layer(self.photonic_layer, devices)
        cell.add_to_layer(self.info_layer, device_info)
        cell.add_to_layer(self.label_layer, device_name)
        cell.add_region_layer(self.region_layer)
        return cell
