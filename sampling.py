import numpy as np
from shapely.geometry import Point


def distance(p1, p2):
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])


def sample_dem_at_point(px, py, dem_arr, dem_transform):
    col, row = ~dem_transform * (px, py)
    col_i, row_i = int(np.round(col)), int(np.round(row))
    row_i = np.clip(row_i, 0, dem_arr.shape[0] - 1)
    col_i = np.clip(col_i, 0, dem_arr.shape[1] - 1)
    return dem_arr[row_i, col_i]


def sample_centerline(centerline, dem, transform, n_r, roads_gdf=None):
    cl_coords = np.array(centerline.coords)

    cl_lengths = np.cumsum(
        [0] + [distance(cl_coords[i], cl_coords[i + 1])
               for i in range(len(cl_coords) - 1)]
    )

    Lc = cl_lengths[-1]
    s_vals = np.linspace(0, Lc, n_r)

    cl_x = np.interp(s_vals, cl_lengths, cl_coords[:, 0])
    cl_y = np.interp(s_vals, cl_lengths, cl_coords[:, 1])

    cl_points = [Point(x, y) for x, y in zip(cl_x, cl_y)]

    if roads_gdf is not None:
        mask = np.array([
            not roads_gdf.geometry.intersects(pt).any()
            for pt in cl_points
        ])
    else:
        mask = np.ones(len(cl_points), dtype=bool)

    cl_x_valid = cl_x[mask]
    cl_y_valid = cl_y[mask]

    elevations = np.array([
        sample_dem_at_point(x, y, dem, transform)
        for x, y in zip(cl_x_valid, cl_y_valid)
    ])

    return cl_x_valid, cl_y_valid, elevations