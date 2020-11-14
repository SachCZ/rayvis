import unittest
import rayvis
from matplotlib import pyplot as plt


class TestMesh(unittest.TestCase):

    def test_read_mfem_mesh(self):
        with open("mesh.mfem") as f:
            mesh = rayvis.read_mfem_mesh(f)
        self.assertEqual((39601, 4), mesh.elements.shape)
        self.assertEqual((40000, 2), mesh.nodes.shape)

    def test_read_vtk_mesh(self):
        with open("mesh.vtk") as f:
            mesh = rayvis.read_vtk_mesh(f)
        self.assertEqual((392, 3), mesh.elements.shape)
        self.assertEqual((222, 2), mesh.nodes.shape)

    def test_plot_mesh(self):
        with open("mesh.vtk") as f:
            mesh = rayvis.read_vtk_mesh(f)
        fig, axes = plt.subplots()
        rayvis.plot_mesh(axes, mesh)
        self.assertEqual(1, len(axes.collections))