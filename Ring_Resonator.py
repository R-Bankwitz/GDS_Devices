from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.geometry.shapely_adapter import geometric_union
from gdshelpers.geometry.chip import Cell

class Ring_Resonator:

    def __init__(self, name, age, pitch):
        self.name = name
        self.age = age
        self.pitch = pitch

    def create(self,x,y,coupler_params):
        incoupler = GratingCoupler.make_traditional_coupler((x, y), **coupler_params)
        outcoupler = GratingCoupler.make_traditional_coupler((x + self.pitch, y), **coupler_params)

        devices = geometric_union([incoupler, outcoupler])
        cell = Cell("Coupler_%s" % (self.name))
        cell.add_to_layer(1, devices)

        return cell

