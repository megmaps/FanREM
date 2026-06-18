import numpy as np
from shapely.geometry import Point
from scipy.interpolate import griddata

#build the synthetic fan surface
def build_synthetic_fan(apex, fan_polygon, cl_x, cl_y, cl_elevs, n_theta):
    X_list, Y_list, Z_list = [], [], []

    r_vals = np.hypot(cl_x - apex.x, cl_y - apex.y)

#generate concentric circles, clip to fan boundary polygon, and extract elevation points along concentric circles (radial rows)
    for i, r in enumerate(r_vals):

        theta_row = np.linspace(0, 2*np.pi, n_theta)
        x_row = apex.x + r * np.cos(theta_row)
        y_row = apex.y + r * np.sin(theta_row)

        mask = np.array([fan_polygon.contains(Point(x, y)) for x, y in zip(x_row, y_row)])

        z_row = np.full_like(x_row, cl_elevs[i])

        X_list.append(x_row[mask])
        Y_list.append(y_row[mask])
        Z_list.append(z_row[mask])

    return (
        np.concatenate(X_list),
        np.concatenate(Y_list),
        np.concatenate(Z_list)
    )

#interpolate elevation points along radial rows using linear interpolation
def interpolate_to_grid(X, Y, Z, transform, width, height):
    cols = np.arange(width)
    rows = np.arange(height)

    xs = transform.c + (cols + 0.5) * transform.a
    ys = transform.f + (rows + 0.5) * transform.e

    XX, YY = np.meshgrid(xs, ys)
    grid_points = np.column_stack((XX.ravel(), YY.ravel()))

    Z_grid = griddata(
        points=np.column_stack((X, Y)),
        values=Z,
        xi=grid_points,
        method="linear"
    )

    #fill any null values with NN interpolation
    nan_mask = np.isnan(Z_grid)
    if np.any(nan_mask):
        Z_grid[nan_mask] = griddata(
            points=np.column_stack((X, Y)),
            values=Z,
            xi=grid_points[nan_mask],
            method="nearest"
        )

    return Z_grid.reshape((height, width))