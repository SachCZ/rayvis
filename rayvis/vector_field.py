import msgpack
import numpy as np
from dataclasses import dataclass
import matplotlib.tri as tri


@dataclass
class VectorField:
    """
    Dataclass representing a discrete vector field holding both coordinates at which the vector values are defined
    and the vector values. This class overrides +,-,*,/ for operands of type [..., ...] this applies the operation
    on func_x using [..., ] and func_y using [,...], the result is still a VectorField
    """
    coord_x: np.ndarray
    coord_y: np.ndarray
    func_x: np.ndarray
    func_y: np.ndarray

    def norm(self):
        return np.sqrt(self.func_x ** 2 + self.func_y ** 2)

    def __add__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x + b[0], self.func_y + b[1])

    def __sub__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x - b[0], self.func_y - b[1])

    def __mul__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x * b[0], self.func_y * b[1])

    def __truediv__(self, b):
        return VectorField(self.coord_x, self.coord_y, self.func_x / b[0], self.func_y / b[1])


def plot_vector_field(axes, vector_field: VectorField, scale_factor=12, quiver_color="white", subdiv=3, **kwargs):
    """
    Plots a vector field using both contour and quiver
    :param subdiv: subdivision time of triangulation
    :param axes: axes to plot to
    :param vector_field: the field to plot
    :param scale_factor: default is 12
    :param quiver_color: default is white
    :param kwargs: kwargs for contour
    :return: the contour
    """
    norm = vector_field.norm()

    kwargs.setdefault("cmap", "jet")
    kwargs.setdefault("levels", 1000)

    triangulation = tri.Triangulation(vector_field.coord_x, vector_field.coord_y)
    refiner = tri.UniformTriRefiner(triangulation)
    tri_refi, z_test_refi = refiner.refine_field(norm, subdiv=subdiv)
    contour = axes.tricontourf(tri_refi, z_test_refi, **kwargs)
    axes.quiver(
        vector_field.coord_x,
        vector_field.coord_y,
        vector_field.func_x,
        vector_field.func_y,
        scale=scale_factor * max(norm),
        color=quiver_color
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
