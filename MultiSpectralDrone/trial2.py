import rasterio
import numpy as np
import matplotlib.pyplot as plt

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

def visualize_ndvi(ndvi):
    """
    Visualize NDVI with colormap.
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(ndvi, cmap='RdYlGn')
    cbar = plt.colorbar()
    cbar.set_label('NDVI')
    plt.title('Normalized Difference Vegetation Index (NDVI)')
    plt.axis('off')
    plt.show()

# Paths to input images (RED and NIR bands)
red_band_path = 'red_band.tif'
nir_band_path = 'nir_band.tif'

# Read RED and NIR bands
red_band = read_band(red_band_path, 1)
nir_band = read_band(nir_band_path, 1)

# Calculate NDVI
ndvi = calculate_ndvi(red_band, nir_band)

# Visualize NDVI
visualize_ndvi(ndvi)
