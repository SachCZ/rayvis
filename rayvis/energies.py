import msgpack
import numpy as np


def read_msgpack_energies(open_file):
    """
        Read energies from msgpack opened file (binary)
        Use: with open(filename, "rb") as f: read_msgpack_energies(f, mesh)
        :param open_file:
        :return:
    """
    arrays = msgpack.unpackb(open_file.read())
    return [np.asarray(arr) for arr in arrays]
