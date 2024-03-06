import rasterio
import numpy as np

def calculate_ndvi(red_band, nir_band):
    """
    Calculate NDVI from red and near-infrared bands.
    NDVI = (NIR - Red) / (NIR + Red)
    """
    ndvi = np.zeros_like(red_band, dtype=np.float32)
    mask = np.logical_and(red_band != 0, nir_band != 0)
    ndvi[mask] = (nir_band[mask] - red_band[mask]) / (nir_band[mask] + red_band[mask])
    return ndvi

def read_band(image_path, band_number):
    """
    Read a specific band from a TIF image.
    """
    with rasterio.open(image_path) as src:
        band = src.read(band_number)
    return band

def save_ndvi(ndvi, output_path, src_profile):
    """
    Save NDVI result to a TIF file.
    """
    with rasterio.open(output_path, 'w', **src_profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)

# Paths to input images (RED and NIR bands)
red_band_path = 'red_band.tif'
nir_band_path = 'nir_band.tif'

# Read RED and NIR bands
red_band = read_band(red_band_path, 1)
nir_band = read_band(nir_band_path, 1)

# Calculate NDVI
ndvi = calculate_ndvi(red_band, nir_band)

# Get the profile of one of the input images (assuming they have the same profile)
with rasterio.open(red_band_path) as src:
    src_profile = src.profile

# Save NDVI result
output_path = 'ndvi_result.tif'
save_ndvi(ndvi, output_path, src_profile)

print("NDVI calculation completed and saved to:", output_path)
