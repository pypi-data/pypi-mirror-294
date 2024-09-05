import numpy as np


def extrinsic_from_Rt(R: np.ndarray, tvec: np.ndarray) -> np.ndarray:
    """returns 4x3 extrinsic matrix from 3x3 rotation matrix R and 1x3 translation vector tvec"""
    extrinsic = np.zeros(shape=(3, 4))
    extrinsic[:3, :3] = R
    extrinsic[:, 3] = np.squeeze(tvec)
    return extrinsic


def P_from_RtvecK(R: np.ndarray, tvec: np.ndarray, intrinsic: np.ndarray) -> np.ndarray:
    """returns projection matrix P from 3x3 rotation matrix R, 1x3 translation vector tvec and 3x3 intrinsic matrix K"""
    if R is None or tvec is None or intrinsic is None:
        return None
    extrinsic = extrinsic_from_Rt(R, tvec)
    P = np.matmul(intrinsic, extrinsic)
    return P


"""
n-view linear triangulation
https://github.com/smidm/camera.py/blob/master/camera.py
"""

# @jit(nopython=True, parallel=True)
def triangulate(camera_mats, points):
    num_cams = len(camera_mats)
    A = np.zeros((num_cams * 2, 4))
    for i in range(num_cams):
        x, y = points[i]
        mat = camera_mats[i]
        A[(i * 2) : (i * 2 + 1)] = x * mat[2] - mat[0]
        A[(i * 2 + 1) : (i * 2 + 2)] = y * mat[2] - mat[1]
    u, s, vh = np.linalg.svd(A, full_matrices=True)
    p3d = vh[-1]
    p3d = p3d[:3] / p3d[3]
    return p3d
