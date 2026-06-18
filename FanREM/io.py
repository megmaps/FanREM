import geopandas as gpd
import rasterio
from rasterio.mask import mask


def load_vector(path):
    return gpd.read_file(path)


def clip_dem_to_polygon(dem_path, polygon_gdf):
    with rasterio.open(dem_path) as src:
        if str(polygon_gdf.crs) != str(src.crs):
            polygon_gdf = polygon_gdf.to_crs(src.crs)

        polygon = polygon_gdf.geometry.iloc[0]
        out_image, out_transform = mask(src, [polygon], crop=True)
        out_meta = src.meta.copy()

    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    return out_image[0], out_transform, out_meta


def write_raster(path, array, meta):
    with rasterio.open(path, 'w', **meta) as dst:
        dst.write(array.astype("float32"), 1)