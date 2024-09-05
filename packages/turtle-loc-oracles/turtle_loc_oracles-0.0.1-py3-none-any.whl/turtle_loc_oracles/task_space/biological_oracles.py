__all__ = [
    "green_sea_turtle_task_space_trajectory_factory",
]
import numpy as np
import scipy.io as sio
from os import PathLike
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple, Union


def green_sea_turtle_task_space_trajectory_factory(
    s: int = 1,
    sf: Union[float, np.ndarray] = 1.0,
    sw: float = 1.0,
    x_off: Optional[np.ndarray] = None,
) -> Tuple[Callable, Callable, Callable, Callable, Callable, Callable]:
    """
    Based on the 4 DoF green sea turtle swimming kinematics of
        van der Geest, N., Garcia, L., Nates, R., & Godoy, D. A. (2022).
        New insight into the swimming kinematics of wild Green sea turtles (Chelonia mydas).
        Scientific Reports, 12(1), 18151.
    Arguments:
        s: int: side sign. +1 for the right flipper, -1 for the left flipper
        sf: float or np.ndarray: spatial scaling factor
        sw: float: speed-up factor
        x_off: np.ndarray: spatial offset
    """
    if type(sf) == float:
        sf = np.array([sf, sf, sf, sf])

    data_path = (
        Path(__file__).parent.parent
        / "data"
        / "green_sea_turtle_swimming_coefficients.mat"
    )
    cfs = sio.loadmat(str(data_path))

    for key, value in cfs.items():
        if type(value) == np.ndarray:
            cfs[key] = value.squeeze()

    # unnormalized duration
    T = 4.2

    # shift the origin such that the mean is at (0, 0, 0)
    x_origin = np.array([-0.12497534, -0.31411964, -0.24547123])

    # extract the coefficients
    a0x, a0y, a0z = cfs["a0x"], cfs["a0y"], cfs["a0z"]
    a1x, a1y, a1z = cfs["a1x"], cfs["a1y"], cfs["a1z"]
    a2x, a2y, a2z = cfs["a2x"], cfs["a2y"], cfs["a2z"]
    a3x, a3y, a3z = cfs["a3x"], cfs["a3y"], cfs["a3z"]
    a4x, a4y, a4z = cfs["a4x"], cfs["a4y"], cfs["a4z"]
    a5x, a5y, a5z = cfs["a5x"], cfs["a5y"], cfs["a5z"]
    a6x, a6y, a6z = cfs["a6x"], cfs["a6y"], cfs["a6z"]
    a7x, a7y, a7z = cfs["a7x"], cfs["a7y"], cfs["a7z"]
    a8x, a8y, a8z = cfs["a8x"], cfs["a8y"], cfs["a8z"]
    b1x, b1y, b1z = cfs["b1x"], cfs["b1y"], cfs["b1z"]
    b2x, b2y, b2z = cfs["b2x"], cfs["b2y"], cfs["b2z"]
    b3x, b3y, b3z = cfs["b3x"], cfs["b3y"], cfs["b3z"]
    b4x, b4y, b4z = cfs["b4x"], cfs["b4y"], cfs["b4z"]
    b5x, b5y, b5z = cfs["b5x"], cfs["b5y"], cfs["b5z"]
    b6x, b6y, b6z = cfs["b6x"], cfs["b6y"], cfs["b6z"]
    b7x, b7y, b7z = cfs["b7x"], cfs["b7y"], cfs["b7z"]
    b8x, b8y, b8z = cfs["b8x"], cfs["b8y"], cfs["b8z"]
    wx, wy, wz = sw * cfs["wx"], sw * cfs["wy"], sw * cfs["wz"]

    def x_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds

        x1 = (
            a0x
            + a1x * np.cos(t * wx)
            + b1x * np.sin(t * wx)
            + a2x * np.cos(2 * t * wx)
            + b2x * np.sin(2 * t * wx)
            + a3x * np.cos(3 * t * wx)
            + b3x * np.sin(3 * t * wx)
            + a4x * np.cos(4 * t * wx)
            + b4x * np.sin(4 * t * wx)
            + a5x * np.cos(5 * t * wx)
            + b5x * np.sin(5 * t * wx)
            + a6x * np.cos(6 * t * wx)
            + b6x * np.sin(6 * t * wx)
            + a7x * np.cos(7 * t * wx)
            + b7x * np.sin(7 * t * wx)
            + a8x * np.cos(8 * t * wx)
            + b8x * np.sin(8 * t * wx)
        )
        x2 = (
            a0y
            + a1y * np.cos(t * wy)
            + b1y * np.sin(t * wy)
            + a2y * np.cos(2 * t * wy)
            + b2y * np.sin(2 * t * wy)
            + a3y * np.cos(3 * t * wy)
            + b3y * np.sin(3 * t * wy)
            + a4y * np.cos(4 * t * wy)
            + b4y * np.sin(4 * t * wy)
            + a5y * np.cos(5 * t * wy)
            + b5y * np.sin(5 * t * wy)
            + a6y * np.cos(6 * t * wy)
            + b6y * np.sin(6 * t * wy)
            + a7y * np.cos(7 * t * wy)
            + b7y * np.sin(7 * t * wy)
            + a8y * np.cos(8 * t * wy)
            + b8y * np.sin(8 * t * wy)
        )
        x3 = (
            a0z
            + a1z * np.cos(t * wz)
            + b1z * np.sin(t * wz)
            + a2z * np.cos(2 * t * wz)
            + b2z * np.sin(2 * t * wz)
            + a3z * np.cos(3 * t * wz)
            + b3z * np.sin(3 * t * wz)
            + a4z * np.cos(4 * t * wz)
            + b4z * np.sin(4 * t * wz)
            + a5z * np.cos(5 * t * wz)
            + b5z * np.sin(5 * t * wz)
            + a6z * np.cos(6 * t * wz)
            + b6z * np.sin(6 * t * wz)
            + a7z * np.cos(7 * t * wz)
            + b7z * np.sin(7 * t * wz)
            + a8z * np.cos(8 * t * wz)
            + b8z * np.sin(8 * t * wz)
        )

        # stack the coordinates
        x = np.stack([x1, x2, x3], axis=-1)

        # map from mm to m
        x = 1e-3 * x

        # shift the origin
        x = x_origin + x

        # rotate into the turtle frame
        x = np.array([s * x[2], -x[0], x[1]])

        # scale the trajectory
        x = x * sf[0:3]

        # add the offset
        if x_off is not None:
            x = x + x_off * np.array([s, 1.0, 1.0])

        return x

    def x_d_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds

        x_d1 = (
            -a1x * wx * np.sin(t * wx)
            + b1x * wx * np.cos(t * wx)
            - 2 * a2x * wx * np.sin(2 * t * wx)
            + 2 * b2x * wx * np.cos(2 * t * wx)
            - 3 * a3x * wx * np.sin(3 * t * wx)
            + 3 * b3x * wx * np.cos(3 * t * wx)
            - 4 * a4x * wx * np.sin(4 * t * wx)
            + 4 * b4x * wx * np.cos(4 * t * wx)
            - 5 * a5x * wx * np.sin(5 * t * wx)
            + 5 * b5x * wx * np.cos(5 * t * wx)
            - 6 * a6x * wx * np.sin(6 * t * wx)
            + 6 * b6x * wx * np.cos(6 * t * wx)
            - 7 * a7x * wx * np.sin(7 * t * wx)
            + 7 * b7x * wx * np.cos(7 * t * wx)
            - 8 * a8x * wx * np.sin(8 * t * wx)
            + 8 * b8x * wx * np.cos(8 * t * wx)
        )
        x_d2 = (
            -a1y * wy * np.sin(t * wy)
            + b1y * wy * np.cos(t * wy)
            - 2 * a2y * wy * np.sin(2 * t * wy)
            + 2 * b2y * wy * np.cos(2 * t * wy)
            - 3 * a3y * wy * np.sin(3 * t * wy)
            + 3 * b3y * wy * np.cos(3 * t * wy)
            - 4 * a4y * wy * np.sin(4 * t * wy)
            + 4 * b4y * wy * np.cos(4 * t * wy)
            - 5 * a5y * wy * np.sin(5 * t * wy)
            + 5 * b5y * wy * np.cos(5 * t * wy)
            - 6 * a6y * wy * np.sin(6 * t * wy)
            + 6 * b6y * wy * np.cos(6 * t * wy)
            - 7 * a7y * wy * np.sin(7 * t * wy)
            + 7 * b7y * wy * np.cos(7 * t * wy)
            - 8 * a8y * wy * np.sin(8 * t * wy)
            + 8 * b8y * wy * np.cos(8 * t * wy)
        )
        x_d3 = (
            -a1z * wz * np.sin(t * wz)
            + b1z * wz * np.cos(t * wz)
            - 2 * a2z * wz * np.sin(2 * t * wz)
            + 2 * b2z * wz * np.cos(2 * t * wz)
            - 3 * a3z * wz * np.sin(3 * t * wz)
            + 3 * b3z * wz * np.cos(3 * t * wz)
            - 4 * a4z * wz * np.sin(4 * t * wz)
            + 4 * b4z * wz * np.cos(4 * t * wz)
            - 5 * a5z * wz * np.sin(5 * t * wz)
            + 5 * b5z * wz * np.cos(5 * t * wz)
            - 6 * a6z * wz * np.sin(6 * t * wz)
            + 6 * b6z * wz * np.cos(6 * t * wz)
            - 7 * a7z * wz * np.sin(7 * t * wz)
            + 7 * b7z * wz * np.cos(7 * t * wz)
            - 8 * a8z * wz * np.sin(8 * t * wz)
            + 8 * b8z * wz * np.cos(8 * t * wz)
        )

        # stack the velocities
        x_d = np.stack([x_d1, x_d2, x_d3], axis=-1)

        # map from mm/s to m/s
        x_d = 1e-3 * x_d

        # rotate into the turtle frame
        x_d = np.array([s * x_d[2], -x_d[0], x_d[1]])

        # scale the trajectory
        x_d = x_d * sf[0:3]

        return x_d

    def x_dd_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds

        x_dd1 = (
            -a1x * wx**2 * np.cos(t * wx)
            - b1x * wx**2 * np.sin(t * wx)
            - 4 * a2x * wx**2 * np.cos(2 * t * wx)
            - 4 * b2x * wx**2 * np.sin(2 * t * wx)
            - 9 * a3x * wx**2 * np.cos(3 * t * wx)
            - 9 * b3x * wx**2 * np.sin(3 * t * wx)
            - 16 * a4x * wx**2 * np.cos(4 * t * wx)
            - 16 * b4x * wx**2 * np.sin(4 * t * wx)
            - 25 * a5x * wx**2 * np.cos(5 * t * wx)
            - 25 * b5x * wx**2 * np.sin(5 * t * wx)
            - 36 * a6x * wx**2 * np.cos(6 * t * wx)
            - 36 * b6x * wx**2 * np.sin(6 * t * wx)
            - 49 * a7x * wx**2 * np.cos(7 * t * wx)
            - 49 * b7x * wx**2 * np.sin(7 * t * wx)
            - 64 * a8x * wx**2 * np.cos(8 * t * wx)
            - 64 * b8x * wx**2 * np.sin(8 * t * wx)
        )
        x_dd2 = (
            -a1y * wy**2 * np.cos(t * wy)
            - b1y * wy**2 * np.sin(t * wy)
            - 4 * a2y * wy**2 * np.cos(2 * t * wy)
            - 4 * b2y * wy**2 * np.sin(2 * t * wy)
            - 9 * a3y * wy**2 * np.cos(3 * t * wy)
            - 9 * b3y * wy**2 * np.sin(3 * t * wy)
            - 16 * a4y * wy**2 * np.cos(4 * t * wy)
            - 16 * b4y * wy**2 * np.sin(4 * t * wy)
            - 25 * a5y * wy**2 * np.cos(5 * t * wy)
            - 25 * b5y * wy**2 * np.sin(5 * t * wy)
            - 36 * a6y * wy**2 * np.cos(6 * t * wy)
            - 36 * b6y * wy**2 * np.sin(6 * t * wy)
            - 49 * a7y * wy**2 * np.cos(7 * t * wy)
            - 49 * b7y * wy**2 * np.sin(7 * t * wy)
            - 64 * a8y * wy**2 * np.cos(8 * t * wy)
            - 64 * b8y * wy**2 * np.sin(8 * t * wy)
        )
        x_dd3 = (
            -a1z * wz**2 * np.cos(t * wz)
            - b1z * wz**2 * np.sin(t * wz)
            - 4 * a2z * wz**2 * np.cos(2 * t * wz)
            - 4 * b2z * wz**2 * np.sin(2 * t * wz)
            - 9 * a3z * wz**2 * np.cos(3 * t * wz)
            - 9 * b3z * wz**2 * np.sin(3 * t * wz)
            - 16 * a4z * wz**2 * np.cos(4 * t * wz)
            - 16 * b4z * wz**2 * np.sin(4 * t * wz)
            - 25 * a5z * wz**2 * np.cos(5 * t * wz)
            - 25 * b5z * wz**2 * np.sin(5 * t * wz)
            - 36 * a6z * wz**2 * np.cos(6 * t * wz)
            - 36 * b6z * wz**2 * np.sin(6 * t * wz)
            - 49 * a7z * wz**2 * np.cos(7 * t * wz)
            - 49 * b7z * wz**2 * np.sin(7 * t * wz)
            - 64 * a8z * wz**2 * np.cos(8 * t * wz)
            - 64 * b8z * wz**2 * np.sin(8 * t * wz)
        )

        # stack the accelerations
        x_dd = np.stack([x_dd1, x_dd2, x_dd3], axis=-1)

        # map from mm/s^2 to m/s^2
        x_dd = 1e-3 * x_dd

        # rotate into the turtle frame
        x_dd = np.array([s * x_dd[2], -x_dd[0], x_dd[1]])

        # scale the trajectory
        x_dd = x_dd * sf[0:3]

        return x_dd

    # twist coefficients
    th_a1x, th_b1x, th_c1x = cfs["th_a1x"], cfs["th_b1x"], cfs["th_c1x"]
    th_a2x, th_b2x, th_c2x = cfs["th_a2x"], cfs["th_b2x"], cfs["th_c2x"]
    th_a3x, th_b3x, th_c3x = cfs["th_a3x"], cfs["th_b3x"], cfs["th_c3x"]
    th_a4x, th_b4x, th_c4x = cfs["th_a4x"], cfs["th_b4x"], cfs["th_c4x"]
    th_a5x, th_b5x, th_c5x = cfs["th_a5x"], cfs["th_b5x"], cfs["th_c5x"]
    th_a1y, th_b1y, th_c1y = cfs["th_a1y"], cfs["th_b1y"], cfs["th_c1y"]
    th_a2y, th_b2y, th_c2y = cfs["th_a2y"], cfs["th_b2y"], cfs["th_c2y"]
    th_a3y, th_b3y, th_c3y = cfs["th_a3y"], cfs["th_b3y"], cfs["th_c3y"]
    th_a4y, th_b4y, th_c4y = cfs["th_a4y"], cfs["th_b4y"], cfs["th_c4y"]
    th_a5y, th_b5y, th_c5y = cfs["th_a5y"], cfs["th_b5y"], cfs["th_c5y"]
    th_a6y, th_c6y = cfs["th_a6y"], cfs["th_c6y"]
    # scale the frequency coefficients
    th_b1x, th_b2x, th_b3x, th_b4x, th_b5x = (
        sw * th_b1x,
        sw * th_b2x,
        sw * th_b3x,
        sw * th_b4x,
        sw * th_b5x,
    )
    th_b1y, th_b2y, th_b3y, th_b4y, th_b5y = (
        sw * th_b1y,
        sw * th_b2y,
        sw * th_b3y,
        sw * th_b4y,
        sw * th_b5y,
    )

    def th_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds
        tn = sw * t

        if 0.0 <= tn < 0.84:
            th = -72.4
        elif 0.84 <= tn < 2.436:
            th = (
                th_a1x * np.sin(th_b1x * t + th_c1x)
                + th_a2x * np.sin(th_b2x * t + th_c2x)
                + th_a3x * np.sin(th_b3x * t + th_c3x)
                + th_a4x * np.sin(th_b4x * t + th_c4x)
                + th_a5x * np.sin(th_b5x * t + th_c5x)
            )
        elif 2.436 <= tn < 3.612:
            th = 27.9
        elif 3.612 <= tn <= 4.2:
            th = (
                th_a1y * np.sin(th_b1y * t + th_c1y)
                + th_a2y * np.sin(th_b2y * t + th_c2y)
                + th_a3y * np.sin(th_b3y * t + th_c3y)
                + th_a4y * np.sin(th_b4y * t + th_c4y)
                + th_a5y * np.sin(th_b5y * t + th_c5y)
                + th_a6y * np.sin(th_b5y * t + th_c6y)
            )
        else:
            raise ValueError(f"Invalid time: {t}")

        # degrees to radians
        th = np.deg2rad(th)

        # scale the trajectory
        th = th * sf[3]

        # rotate into the turtle frame
        th = -s * th

        return th

    def th_d_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds
        tn = sw * t

        if 0.0 <= tn < 0.84:
            th_d = 0.0
        elif 0.84 <= tn < 2.436:
            th_d = (
                th_a1x * th_b1x * np.cos(th_b1x * t + th_c1x)
                + th_a2x * th_b2x * np.cos(th_b2x * t + th_c2x)
                + th_a3x * th_b3x * np.cos(th_b3x * t + th_c3x)
                + th_a4x * th_b4x * np.cos(th_b4x * t + th_c4x)
                + th_a5x * th_b5x * np.cos(th_b5x * t + th_c5x)
            )
        elif 2.436 <= tn < 3.612:
            th_d = 0.0
        elif 3.612 <= tn <= 4.2:
            th_d = (
                th_a1y * th_b1y * np.cos(th_b1y * t + th_c1y)
                + th_a2y * th_b2y * np.cos(th_b2y * t + th_c2y)
                + th_a3y * th_b3y * np.cos(th_b3y * t + th_c3y)
                + th_a4y * th_b4y * np.cos(th_b4y * t + th_c4y)
                + th_a5y * th_b5y * np.cos(th_b5y * t + th_c5y)
                + th_a6y * th_b5y * np.cos(th_b5y * t + th_c6y)
            )
        else:
            raise ValueError(f"Invalid time: {t}")

        # degrees to radians
        th_d = np.deg2rad(th_d)

        # scale the trajectory
        th_d = th_d * sf[3]

        # rotate into the turtle frame
        th_d = -s * th_d

        return th_d

    def th_dd_fn(t: np.ndarray):
        t = t % (T / sw)  # repeat the trajectory every (normalized) 4.2 seconds
        tn = sw * t

        if 0.0 <= tn < 0.84:
            th_dd = 0.0
        elif 0.84 <= tn < 2.436:
            th_dd = (
                -th_a1x * th_b1x**2 * np.sin(th_b1x * t + th_c1x)
                - th_a2x * b2x**2 * np.sin(th_b2x * t + th_c2x)
                - th_a3x * th_b3x**2 * np.sin(th_b3x * t + th_c3x)
                - th_a4x * b4x**2 * np.sin(th_b4x * t + th_c4x)
                - th_a5x * th_b5x**2 * np.sin(th_b5x * t + th_c5x)
            )
        elif 2.436 <= tn < 3.612:
            th_dd = 0.0
        elif 3.612 <= tn <= 4.2:
            th_dd = (
                -th_a1y * th_b1y**2 * np.sin(th_b1y * t + th_c1y)
                - th_a2y * th_b2y**2 * np.sin(th_b2y * t + th_c2y)
                - th_a3y * th_b3y**2 * np.sin(th_b3y * t + th_c3y)
                - th_a4y * th_b4y**2 * np.sin(th_b4y * t + th_c4y)
                - th_a5y * th_b5y**2 * np.sin(th_b5y * t + th_c5y)
                - th_a6y * th_b5y**2 * np.sin(th_b5y * t + th_c6y)
            )
        else:
            raise ValueError(f"Invalid time: {t}")

        # degrees to radians
        th_dd = np.deg2rad(th_dd)

        # scale the trajectory
        th_dd = th_dd * sf[3]

        # rotate into the turtle frame
        th_dd = -s * th_dd

        return th_dd

    return x_fn, x_d_fn, x_dd_fn, th_fn, th_d_fn, th_dd_fn
