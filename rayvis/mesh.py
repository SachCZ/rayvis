from matplotlib.collections import PolyCollection
import numpy as np
import vtk
from dataclasses import dataclass


@dataclass
class Mesh:
    """Python mesh abstraction to enable communication between loaders and plotters"""
    nodes: np.ndarray
    elements: np.ndarray


def read_mfem_mesh(open_file):
    """
    Reads a mesh from opened mfem mesh file. Use: with open(filename) as f: read_mfem_mesh(f)
    :param open_file:
    :return: Mesh
    """
    lines = open_file.readlines()
    elements_begin = 0
    elements_number = 0
    nodes_begin = 0
    nodes_number = 0
    elements = []
    nodes = []
    for i, line in enumerate(lines):
        if line == "elements\n":
            elements_number = int(lines[i + 1])
            elements_begin = i + 2

    for i, line in enumerate(lines):
        if line == "vertices\n":
            nodes_number = int(lines[i + 1])
            nodes_begin = i + 3

    for i in range(elements_begin, elements_begin + elements_number):
        data = lines[i].split()
        if int(data[1]) == 3:
            elements.append([int(data[2]), int(data[3]), int(data[4]), int(data[5])])
        if int(data[1]) == 2:
            elements.append([int(data[2]), int(data[3]), int(data[4])])

    for i in range(nodes_begin, nodes_begin + nodes_number):
        data = lines[i].split()
        nodes.append([float(data[0]), float(data[1])])

    return Mesh(np.asarray(nodes), np.asarray(elements))


def read_vtk_mesh(open_file):
    """
    Reads a mesh from opened vtk mesh file. Use: with open(filename) as f: read_vtk_mesh(f)
    :param open_file: 
    :return: Mesh
    """""
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetInputString(open_file.read())
    reader.ReadFromInputStringOn()
    reader.Update()

    nodes = np.array(reader.GetOutput().GetPoints().GetData())
    nodes = nodes[:, :-1]

    points_count = reader.GetOutput().GetCell(0).GetNumberOfPoints()

    elements = np.array(reader.GetOutput().GetCells().GetData()).reshape((-1, points_count + 1))
    elements = elements[:, 1:]
    return Mesh(np.asarray(nodes), np.asarray(elements))


def plot_mesh(axes, mesh, **kwargs):
    """
    Add a PolyCollection to given axis representing the mesh.
    :param axes: plt axis
    :param mesh: Mesh
    :param kwargs: any arguments for the matplotlib.collections.PolyCollection
    :return: None
    """
    kwargs.setdefault("facecolors", "none")
    kwargs.setdefault("linewidth", 0.5)
    poly_collection = PolyCollection(mesh.nodes[mesh.elements], **kwargs)
    axes.add_collection(poly_collection)
    axes.autoscale()
