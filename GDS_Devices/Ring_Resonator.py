from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.resonator import RingResonator

class Ring_Resonator:

    def __init__(self, name, wg_width, pitch=127, bending_radius = 100):
        self.pitch = pitch
        self.name = name
        self.bendin_radius = bending_radius
        self.wg_width = wg_width

    def create(self,x,y,coupler_params, gap ,  radius, angle = 0,):

        coupler_params["width"] = self.wg_width
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)

        wg1 = Waveguide.make_at_port(outcoupler.port)
        wg1.add_left_bend(self.bendin_radius)
        wg1.add_route_single_circle_to_port(incoupler.port,self.bendin_radius)

        RR = RingResonator((x+self.pitch/2, y+self.bendin_radius), angle = angle, gap = gap, radius = radius, width = self.wg_width)

        devices = geometric_union([incoupler, outcoupler, wg1, RR])
        cell = Cell("Resonator_%s" % (self.name))
        cell.add_to_layer(1, devices)

        return cell

