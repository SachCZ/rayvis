import unittest
import rayvis
from matplotlib import pyplot as plt


class TestGridFunction(unittest.TestCase):

    def test_read_vtk_mesh(self):
        with open("rays.msgpack", "rb") as f:
            rays = rayvis.read_msgpack_rays(f)
        fig, axes = plt.subplots()
        rayvis.plot_rays(axes, rays)
        self.assertEqual(len(axes.lines), 100)

