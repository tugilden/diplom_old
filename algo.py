import numpy as np
from math import ceil
from transform import forward_transform


def iteration(h, w):
    t = ceil(w[-2] / w[-1])
    h_next = t * h[-1] - h[-2]
    w_next = t * w[-1] - w[-2]
    h.append(h_next)
    w.append(w_next)


def algorithm(line2, line1):
    alpha, beta, gamma, beta2, identity_matrix = forward_transform(line1, line2)

    h1 = np.array([1, 0])
    h2 = np.array([0, 1])
    h = [h1, h2]

    weight = [alpha, beta]

    gamma0 = gamma - (gamma // alpha) * alpha
    gamma_lst = [gamma0, gamma0 - (gamma0 // beta) * beta]

    T0 = np.array([gamma // alpha, 0])
    if gamma0 // beta == 0:
        T_lst = [T0]
    else:
        T_lst = [T0, T0 + (gamma0 // beta) * h2]

    eps = 0.0000001
    while gamma_lst[-1] > eps:
        iteration(h, weight)
        if weight[-1] <= gamma_lst[-1]:
            k = gamma_lst[-1] // weight[-1]
            gamma_next = gamma_lst[-1] - k * weight[-1]
            gamma_lst.append(gamma_next)
            T_lst.append(T_lst[-1] + k * h[-1])

    T_fin_lst = [identity_matrix.dot(np.array([vec[0], vec[1] - int(line2["gamma"] / abs(beta2))])) for vec in T_lst]

    return(T_fin_lst)