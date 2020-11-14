import numpy as np
from dataclasses import dataclass
from matplotlib.collections import PolyCollection

from rayvis.mesh import Mesh


@dataclass
class GridFunction:
    """Python grid_function abstraction to enable communication between loaders and plotters"""
    values: np.ndarray
    mesh: Mesh


def read_grid_function(open_file, mesh):
    """
    Reads a grid function from opened mfem grid_function file and maps it to mesh.
    Use: with open(filename) as f: read_grid_function(f, mesh)
    :param mesh:
    :param open_file:
    :return: GridFunction
    """
    return GridFunction(np.genfromtxt(open_file, skip_header=5), mesh)


def plot_grid_function(axes, grid_function, **kwargs):
    """
    Add a PolyCollection to given axis representing the grid function
    :param axes:
    :param grid_function:
    :param kwargs: any kwargs for the PolyCollection
    :return: None
    """
    poly_collection = PolyCollection(grid_function.mesh.nodes[grid_function.mesh.elements], **kwargs)
    poly_collection.set_array(grid_function.values)
    axes.add_collection(poly_collection)
    axes.autoscale()
    return poly_collection
