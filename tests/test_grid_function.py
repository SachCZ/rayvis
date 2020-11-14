import unittest
import rayvis
from matplotlib import pyplot as plt


class TestGridFunction(unittest.TestCase):

    def test_read_and_plot_grid_function(self):
        with open("mesh.vtk") as f:
            mesh = rayvis.read_vtk_mesh(f)
        with open("grid_function.gf") as f:
            grid_function = rayvis.read_grid_function(f, mesh)
        fig, axes = plt.subplots()
        rayvis.plot_grid_function(axes, grid_function)
        self.assertEqual(1, len(axes.collections))
