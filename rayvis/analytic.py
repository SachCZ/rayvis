from matplotlib import pyplot as plt
import scipy.integrate as integrate
import numpy as np


def right_hand_side(s, variables):
    y, z, theta = variables
    return [-np.sin(theta), -np.cos(theta), np.sin(theta) / z]


def analytic_solution(initial_x, initial_y, vec_x, vec_y):
    theta = np.arctan(vec_y / vec_x)
    solution = integrate.solve_ivp(right_hand_side, [0, 2], [initial_y, -initial_x, -theta], max_step=1e-2)
    x, y =  -solution.y[1], solution.y[0]
    x = [x0 for x0, y0 in zip(x, y) if x0 > -1 and y0 < 1]
    y = [y0 for x0, y0 in zip(x, y) if x0 > -1 and y0 < 1]
    return x, y


if __name__ == '__main__':
    _x, _y = analytic_solution(-1.2, 0.2, 1, 1)
    plt.plot(_x, _y)
    plt.show()
