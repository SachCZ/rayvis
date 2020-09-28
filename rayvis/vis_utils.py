import matplotlib.collections
import numpy as np
import vtk
import json


def read_rays(filename):
    with open(filename) as rays_file:
        rays_root = json.load(rays_file)
    return rays_root["rays"]


def plot_rays(axis, rays, each_n=1, scale=1, **kwargs):
    for i, ray in enumerate(rays):
        if (i + 1) % each_n != 0 and i != 0:
            continue
        ray = np.asarray(ray)
        x = ray[:, 0]*scale
        y = ray[:, 1]*scale
        axis.plot(x, y, "-", **kwargs)


def read_vtk(filename):
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(filename)
    reader.Update()

    nodes = np.array(reader.GetOutput().GetPoints().GetData())
    nodes = nodes[:, :-1]

    points_count = reader.GetOutput().GetCell(0).GetNumberOfPoints()

    elements = np.array(reader.GetOutput().GetCells().GetData()).reshape((-1, points_count + 1))
    elements = elements[:, 1:]
    return nodes, elements


def read_mesh(filename):
    with open(filename) as file:
        lines = file.readlines()
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

        return np.asarray(nodes), np.asarray(elements)


def read_grid_function(filename):
    return np.genfromtxt(filename, skip_header=5)


def plot_vtk_mesh(axis, nodes, element_indexes, edgecolor="white", facecolors="blue"):
    poly_collection = matplotlib.collections.PolyCollection(nodes[element_indexes], edgecolor=edgecolor,
                                                            facecolors=facecolors, linewidth=0.5)
    axis.add_collection(poly_collection)
    axis.autoscale()


def plot_grid_function(fig, axis, nodes, element_indexes, values, label="", label_top=False, cmap="Blues"):
    poly_collection = matplotlib.collections.PolyCollection(nodes[element_indexes], edgecolor=None, cmap=cmap)
    poly_collection.set_array(values)
    clb = fig.colorbar(poly_collection, ax=axis)
    if label_top:
        clb.ax.set_title(label)
    else:
        clb.ax.set_ylabel(label)
    axis.add_collection(poly_collection)
    axis.autoscale()


def read_gradient(filename):
    data = np.genfromtxt(filename, delimiter=",")
    x = data[:, 0]
    y = data[:, 1]
    grad_x = data[:, 2]
    grad_y = data[:, 3]
    return x, y, grad_x, grad_y


def plot_quiver(axis, x, y, f_x, f_y, **kwargs):
    u, v = np.meshgrid(f_x, f_y)
    axis.quiver(x, y, u, v, **kwargs)


def sample_analytic_gradient(x, y, function):
    grad_x = []
    grad_y = []
    for x0, y0 in zip(x, y):
        grad_x0, grad_y0 = function(x0, y0)
        grad_x.append(grad_x0)
        grad_y.append(grad_y0)
    return np.array(grad_x), np.array(grad_y)
