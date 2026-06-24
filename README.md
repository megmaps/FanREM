# FanREM

**FanREM** is a Python package for generating **Fan-Relative Elevation Models (FREM)** from a digital elevation model (DEM) and associated GIS data (fan apex, channel centerline, fan boundary, roads).

---

## Installation

Clone the repository:

```bash
git clone https://github.com/megmaps/FanREM.git
cd FanREM
```

Install the package in editable mode: 
```bash
python -m pip install -e .
```

This requires Python ≥ 3.10 and a valid ```pyproject.toml``` file in the repository root.

## Usage
After installation, the package is imported as:

```python
from fanrem import create_frem
```

Once installed, use the package like this:
```bash
from fanrem import create_frem

create_frem(
    apex_path="path/to/apex.shp",
    boundary_path="path/to/fan_boundary.shp",
    centerline_path="path/to/centerline.shp",
    dem_path="path/to/DEM.tif",
    road_path="path/to/roads.shp",
    out_synthetic="path/to/output_synthetic.tif",
    out_frem="path/to/output_FREM.tif"
)
```
The package produces two outputs: the synthetic raster and the FREM (both as tif. files). 

## Requirements

If installation fails, install dependencies manually:

```pip install numpy geopandas rasterio shapely scipy matplotlib```

## Troubleshooting

No FREM output or errors reading files: Check that all input files exist and are in a compatible CRS.

Incorrect fan alignment: Verify that apex, centerline, and fan boundary shapefiles correspond to the same DEM.

## Funding
This package was developed as part of my MASc in 2026. This research was supported by the Natural Sciences and Engineering Research Council of Canada (NSERC) under CGS-M. Thank you for those who provided feedback along the way!


## Contributing / Issues

Contributions, bug reports, and feature requests are welcome.
Please submit issues via the GitHub repository.
