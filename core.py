from .io import load_vector, clip_dem_to_polygon, write_raster
from .sampling import sample_centerline
from .interpolation import build_synthetic_fan, interpolate_to_grid

def create_frem(
    apex_path,
    boundary_path,
    centerline_path,
    dem_path,
    road_path=None,
    n_r=10,
    n_theta=100,
    out_synthetic=None,
    out_frem=None
):
    #load vectors
    apex_gdf = load_vector(apex_path)
    boundary_gdf = load_vector(boundary_path)
    centerline_gdf = load_vector(centerline_path)
    roads_gdf = load_vector(road_path) if road_path else None

    apex = apex_gdf.geometry.iloc[0]
    fan_polygon = boundary_gdf.geometry.iloc[0]
    centerline = centerline_gdf.geometry.iloc[0]

    #clip DEM to fan boundary
    dem, transform, meta = clip_dem_to_polygon(dem_path, boundary_gdf)

    #sample channel centerline
    cl_x, cl_y, cl_elevs = sample_centerline(centerline, dem, transform, n_r, roads_gdf)

    #build synthetic fan and interpolate
    X, Y, Z = build_synthetic_fan(apex, fan_polygon, cl_x, cl_y, cl_elevs, n_theta)
    Z_synth = interpolate_to_grid(X, Y, Z, transform, meta["width"], meta["height"])

    #write synthetic fan raster
    if out_synthetic:
        write_raster(out_synthetic, Z_synth, meta)

    #compute FREM
    Z_frem = dem - Z_synth
    if out_frem:
        write_raster(out_frem, Z_frem, meta)

    return Z_frem