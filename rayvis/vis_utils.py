import matplotlib.collections
import numpy as np
import vtk
import json


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
