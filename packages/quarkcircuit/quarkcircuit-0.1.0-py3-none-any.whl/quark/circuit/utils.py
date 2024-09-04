# Copyright (c) 2024 XX Xiao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Optional
import numpy as np
from scipy import linalg
from math import atan2

def generate_random_unitary_matrix(dim: int, seed: Optional[int] = None) -> np.ndarray:
    """
    Generate a random complex unitary matrix.
    """
    from scipy.stats import unitary_group
    U = unitary_group.rvs(dim, size=1, random_state=seed)
    return U

def is_equiv_unitary(mat1: np.ndarray, mat2: np.ndarray) -> bool:
    """
    Distinguish whether two unitary operators are equivalent, regardless of the global phase.
    """
    if mat1.shape != mat2.shape:
        raise ValueError(f'Input matrices have different dimensions: {mat1.shape}, {mat2.shape}.')
    d = mat1.shape[0]
    if not np.allclose(mat1 @ mat1.conj().T, np.identity(d)):
        raise ValueError('mat1 is not unitary')
    if not np.allclose(mat2 @ mat2.conj().T, np.identity(d)):
        raise ValueError('mat2 is not unitary')
    mat1f = mat1.ravel()
    mat2f = mat2.ravel()
    idx_uf = np.flatnonzero(mat1f.round(4))  # cut to some precision
    idx_vf = np.flatnonzero(mat2f.round(4))
    try:
        if np.array_equal(idx_uf, idx_vf):
            coe = mat1f[idx_uf] / mat2f[idx_vf]
            return np.allclose(coe / coe[0], np.ones(len(idx_uf)), atol=1e-6)
        return False
    except ValueError:
        return False
    
def simult_svd(mat1: np.ndarray, mat2: np.ndarray):
    r"""
    Simultaneous SVD of two matrices, based on Eckart-Young theorem.

    Given two real matrices A and B who satisfy the condition of simultaneous SVD, then

    .. math::
        A = U D_1 V^{\dagger}, B = U D_2 V^{\dagger}

    Args:
        mat1: real matrix
        mat2: real matrix

    Returns:
        Four real matrices: u, v, d1, d2. u an v are both in SO(2). d1 and d2 are diagonal.

    References:
        'An Introduction to Cartan's KAK Decomposition for QC Programmers'
        https://arxiv.org/abs/quant-ph/0507171
    """
    if mat1.shape != mat2.shape:
        raise ValueError(f'mat1 and mat2 have different dimensions: {mat1.shape}, {mat2.shape}.')
    d = mat1.shape[0]

    # real orthogonal matrices decomposition
    u_a, d_a, v_a_h = linalg.svd(mat1)
    u_a_h = u_a.conj().T
    v_a = v_a_h.conj().T

    if np.count_nonzero(d_a) != d:
        raise ValueError('Not implemented yet for the situation that mat1 is not full-rank')
    # g commutes with d
    g = u_a_h @ mat2 @ v_a
    # because g is hermitian, eigen-decomposition is its spectral decomposition
    _, p = linalg.eigh(g)  # p is unitary or orthogonal
    u = u_a @ p
    v = v_a @ p

    # ensure det(u_a) == det(v_a) == +1
    if linalg.det(u) < 0:
        u[:, 0] *= -1
    if linalg.det(v) < 0:
        v[:, 0] *= -1

    d1 = u.conj().T @ mat1 @ v
    d2 = u.conj().T @ mat2 @ v
    return (u, v), (d1, d2)

def glob_phase(mat: np.ndarray) -> float:
    r"""
    Extract the global phase `\alpha` from a d*d matrix.

    .. math::
        U = e^{i\alpha} S

    in which S is in SU(d).

    Args:
        mat: d*d unitary matrix

    Returns:
        Global phase rad, in range of (-pi, pi].
    """
    d = mat.shape[0]
    if d == 0:
        raise ZeroDivisionError("Dimension of mat can not be zero.")
    exp_alpha = linalg.det(mat) ** (1 / d)
    return np.angle(exp_alpha)


def remove_glob_phase(mat: np.ndarray) -> np.ndarray:
    r"""
    Remove the global phase of a 2x2 unitary matrix by means of ZYZ decomposition.

    That is, remove

    .. math::

        e^{i\alpha}

    from

    .. math::
        U = e^{i\alpha} R_z(\phi) R_y(\theta) R_z(\lambda)

    and return

    .. math::
        R_z(\phi) R_y(\theta) R_z(\lambda)

    Args:
        mat: 2x2 unitary matrix

    Returns:
        2x2 matrix without global phase.
    """
    alpha = glob_phase(mat)
    return mat * np.exp(-1j * alpha)

def kron_factor_4x4_to_2x2s(mat: np.ndarray):
    
    """
    Split a 4x4 matrix U = kron(A, B) into A, B, and a global factor.

    Requires the matrix to be the kronecker product of two 2x2 unitaries.
    Requires the matrix to have a non-zero determinant.
    Giving an incorrect matrix will cause garbage output.

    Args:
        mat: The 4x4 unitary matrix to factor.

    Returns:
        A scalar factor and a pair of 2x2 unit-determinant matrices. The
        kronecker product of all three is equal to the given matrix.

    Raises:
        ValueError:
            The given matrix can't be tensor-factored into 2x2 pieces.
    """
    # Use the entry with the largest magnitude as a reference point.
    a, b = max(((i, j) for i in range(4) for j in range(4)), key=lambda t: abs(mat[t]))

    # Extract sub-factors touching the reference cell.
    f1 = np.zeros((2, 2), dtype=np.complex128)
    f2 = np.zeros((2, 2), dtype=np.complex128)
    for i in range(2):
        for j in range(2):
            f1[(a >> 1) ^ i, (b >> 1) ^ j] = mat[a ^ (i << 1), b ^ (j << 1)]
            f2[(a & 1) ^ i, (b & 1) ^ j] = mat[a ^ i, b ^ j]

    # Rescale factors to have unit determinants.
    f1 /= np.sqrt(np.linalg.det(f1)) or 1
    f2 /= np.sqrt(np.linalg.det(f2)) or 1

    # Determine global phase.
    denominator = f1[a >> 1, b >> 1] * f2[a & 1, b & 1]
    if denominator == 0:
        raise ZeroDivisionError("denominator cannot be zero.")
    g = mat[a, b] / denominator
    if np.real(g) < 0:
        f1 *= -1
        g = -g

    return g, f1, f2

def kak_decompose(mat: np.ndarray):
    r"""
    KAK decomposition (CNOT basis) of an arbitrary two-qubit gate.

    For more detail, please refer to `An Introduction to Cartan's KAK Decomposition for QC
    Programmers <https://arxiv.org/abs/quant-ph/0406176>`_.

    """
    M = np.array([[1, 0, 0, 1j], [0, 1j, 1, 0], [0, 1j, -1, 0], [1, 0, 0, -1j]], dtype=complex) / np.sqrt(2)
    M_DAG = M.conj().T
    A = np.array([[1, 1, -1, 1], [1, 1, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1]],dtype=complex)
    pauli_i = np.eye(2, dtype=complex)
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

    # construct a new matrix replacing U
    u_su4 = M_DAG @ remove_glob_phase(mat) @ M  # ensure the decomposed object is in SU(4)
    ur = np.real(u_su4)  # real part of u_su4
    ui = np.imag(u_su4)  # imagine part of u_su4

    # simultaneous SVD decomposition
    (q_left, q_right), (dr, di) = simult_svd(ur, ui)
    d = dr + 1j * di

    _, a1, a0 = kron_factor_4x4_to_2x2s(M @ q_left @ M_DAG)
    _, b1, b0 = kron_factor_4x4_to_2x2s(M @ q_right.T @ M_DAG)

    k = linalg.inv(A) @ np.angle(np.diag(d))
    h1, h2, h3 = -k[1:]

    u0 = 1j / np.sqrt(2) * (pauli_x + pauli_z) @ linalg.expm(-1j * (h1 - np.pi / 4) * pauli_x)
    v0 = -1j / np.sqrt(2) * (pauli_x + pauli_z)
    u1 = linalg.expm(-1j * h3 * pauli_z)
    v1 = linalg.expm(1j * h2 * pauli_z)
    w = (pauli_i - 1j * pauli_x) / np.sqrt(2)

    # list of operators
    rots1 = [b0, u0, v0, a0 @ w]  # rotation gate on idx1
    rots2 = [b1, u1, v1, a1 @ w.conj().T]
    return rots1, rots2

def zyz_decompose(mat: np.ndarray):
    r"""
    ZYZ decomposition of a 2x2 unitary matrix.

    .. math::
        U = e^{i\alpha} R_z(\phi) R_y(\theta) R_z(\lambda)

    Args:
        mat: 2x2 unitary matrix

    Returns:
        `\alpha`, `\theta`, `\phi`, `\lambda`, four phase angles.
    """
    mat = mat.astype(np.complex128)
    if mat.shape != (2, 2):
        raise ValueError('Input matrix should be a 2*2 matrix')
    coe = linalg.det(mat) ** (-0.5)
    alpha = -np.angle(coe)
    v = coe * mat
    v = v.round(10)
    theta = 2 * atan2(abs(v[1, 0]), abs(v[0, 0]))
    phi_lam_sum = 2 * np.angle(v[1, 1])
    phi_lam_diff = 2 * np.angle(v[1, 0])
    phi = (phi_lam_sum + phi_lam_diff) / 2
    lam = (phi_lam_sum - phi_lam_diff) / 2
    return theta, phi, lam, alpha

def u3_decompose(mat: np.ndarray):
    r"""
    Obtain the U3 parameters of a 2x2 unitary matrix.

    .. math::
        U = exp(i p) U3(\theta, \phi, \lambda)

    Args:
        mat: 2x2 unitary matrix
        return_phase: whether return the global phase `p`.

    Returns:
        Global phase `p` and three parameters `\theta`, `\phi`, `\lambda` of a standard U3 gate.
    """
    theta, phi, lam, alpha = zyz_decompose(mat)
    phase = alpha - (phi + lam) / 2
    return theta, phi, lam, phase