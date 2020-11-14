import json
import msgpack
import numpy as np
from dataclasses import dataclass
from matplotlib.lines import Line2D


@dataclass
class Ray:
    """Python ray abstraction to enable communication between loaders and plotters"""
    x: np.ndarray
    y: np.ndarray


def read_json_rays(open_file):
    """
    Read rays from json opened file.
    Use: with open(filename) as f: read_json_rays(f, mesh)
    :param open_file:
    :return:
    """
    rays = np.array(json.load(open_file)["rays"])
    return [Ray(ray[:, 0], ray[:, 1]) for ray in rays]


def read_msgpack_rays(open_file):
    """
    Read rays from msgpack opened file (binary)
    Use: with open(filename, "rb") as f: read_msgpack_rays(f, mesh)
    :param open_file:
    :return:
    """
    rays = msgpack.unpackb(open_file.read())
    return [Ray(ray["x"], ray["y"]) for ray in rays]


def plot_rays(axes, rays, **kwargs):
    """
    Add a Line2D for each ray to the axes
    :param axes:
    :param rays:
    :param kwargs: Any kwargs for  matplotlib.lines.Line2D
    :return:
    """
    kwargs.setdefault("linestyle", "-")
    kwargs.setdefault("linewidth", 1)
    kwargs.setdefault("color", "black")

    for ray in rays:
        axes.add_line(Line2D(ray.x, ray.y, **kwargs))
    axes.autoscale()