import msgpack
import numpy as np
from dataclasses import dataclass
from rayvis.grid_function import plot_grid_function, GridFunction


@dataclass
class VectorField:
    """
    Dataclass representing a discrete vector field holding both coordinates at which the vector values are defined
    and the vector values. This class overrides +,-,*,/ f\or operands of type [..., ...] this applies the operation
    on func_x using [..., ] and func_y using [,...], the result is still a VectorField
    """
    coord_x: np.ndarray
    coord_y: np.ndarray
    func_x: np.ndarray
    func_y: np.ndarray

    def norm(self):
        return np.sqrt(self.func_x ** 2 + self.func_y ** 2)

    def __add__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x + b.func_x, self.func_y + b.func_y)

    def __sub__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x - b.func_x, self.func_y - b.func_y)

    def __mul__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x * b.func_x, self.func_y * b.func_y)

    def __truediv__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x / b.func_x, self.func_y / b.func_y)


def plot_vector_field(axes, vector_field: VectorField, dual_mesh, arrow_scale=None, arrow_color="white", **kwargs):
    """
    Plots a vector field using both contour and quiver
    :param arrow_scale:
    :param arrow_color:
    :param axes: axes to plot to
    :param vector_field: the field to plot
    :param dual_mesh: dual mesh to map the norm of the vector field to
    :param kwargs: kwargs for contour
    :return: the contour
    """
    norm = vector_field.norm()
    contour = plot_grid_function(axes, GridFunction(norm, dual_mesh), **kwargs)

    axes.quiver(
        vector_field.coord_x,
        vector_field.coord_y,
        vector_field.func_x,
        vector_field.func_y,
        color=arrow_color,
        scale=12 * max(norm) if not arrow_color else arrow_scale
    )
    return contour


def read_vector_field(open_file):
    """
    Reads a vector field from opened raytracer msgpack vector field file.
    Use: with open(filename) as f: read_vector_field(f)
    :param open_file:
    :return: VectorField
    """
    byte_data = open_file.read()

    data_loaded = np.asarray(msgpack.unpackb(byte_data))
    return VectorField(*np.rollaxis(data_loaded, 1))
