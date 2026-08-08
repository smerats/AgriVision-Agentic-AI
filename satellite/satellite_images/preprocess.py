"""
preprocess.py

Purpose:
---------
Preprocess Sentinel-2 bands B2, B3, B4 and B8.

Handles:
- Sentinel-2 NoData value (-10000)
- Invalid values such as 32767
- Reflectance scaling
- Common valid-data mask

Author:
Gopika Hajra
"""

import os
import numpy as np
import rasterio


class Preprocessor:

    def __init__(self):

        self.project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.data_folder = os.path.join(
            self.project_root,
            "data"
        )

        self.band_files = {
            "B2": "B2.tif",
            "B3": "B3.tif",
            "B4": "B4.tif",
            "B8": "B8.tif"
        }

    # --------------------------------------------------
    # READ ONE BAND
    # --------------------------------------------------

    def read_band(self, band_name):

        path = os.path.join(
            self.data_folder,
            self.band_files[band_name]
        )

        print(f"Reading {band_name}...")

        with rasterio.open(path) as src:

            data = src.read(1).astype(np.float32)

            nodata = src.nodata

        # Start with finite values
        valid = np.isfinite(data)

        # Remove declared NoData
        if nodata is not None:
            valid &= data != nodata

        # Remove negative values
        valid &= data >= 0

        # Remove abnormal values
        valid &= data <= 10000

        # Convert digital number to reflectance
        data = data / 10000.0

        # Invalid pixels become NaN
        data[~valid] = np.nan

        return data, valid

    # --------------------------------------------------
    # PREPROCESS ALL BANDS
    # --------------------------------------------------

    def preprocess(self):

        print("Reading Sentinel-2 bands...")
        print("Handling NoData and invalid pixels...")
        print("Normalizing reflectance...\n")

        bands = {}
        masks = []

        # Read B2, B3, B4, B8
        for band_name in self.band_files:

            data, valid = self.read_band(
                band_name
            )

            bands[band_name] = data
            masks.append(valid)

        # --------------------------------------------------
        # COMMON VALID MASK
        # --------------------------------------------------

        common_mask = masks[0].copy()

        for mask in masks[1:]:

            common_mask &= mask

        # Apply common mask to every band
        for band_name in bands:

            bands[band_name][~common_mask] = np.nan

        # --------------------------------------------------
        # STATISTICS
        # --------------------------------------------------

        total_pixels = common_mask.size

        valid_pixels = np.sum(common_mask)

        nodata_pixels = total_pixels - valid_pixels

        valid_percentage = (
            valid_pixels / total_pixels
        ) * 100

        nodata_percentage = (
            nodata_pixels / total_pixels
        ) * 100

        print()
        print("=" * 50)
        print("PREPROCESSING INFORMATION")
        print("=" * 50)

        print(
            f"Total pixels : {total_pixels:,}"
        )

        print(
            f"Valid pixels : {valid_pixels:,}"
        )

        print(
            f"NoData pixels: {nodata_pixels:,}"
        )

        print(
            f"Valid area   : {valid_percentage:.2f}%"
        )

        print(
            f"NoData area  : {nodata_percentage:.2f}%"
        )

        print("=" * 50)

        # --------------------------------------------------
        # BAND STATISTICS
        # --------------------------------------------------

        print("\nBAND STATISTICS")
        print("-" * 50)

        for band_name, data in bands.items():

            valid_values = data[
                ~np.isnan(data)
            ]

            if len(valid_values) > 0:

                print(
                    f"{band_name}: "
                    f"Min={np.min(valid_values):.4f}, "
                    f"Max={np.max(valid_values):.4f}, "
                    f"Mean={np.mean(valid_values):.4f}"
                )

            else:

                print(
                    f"{band_name}: No valid pixels"
                )

        print()

        print(
            "Preprocessing Completed Successfully."
        )

        return bands


# ------------------------------------------------------
# TEST
# ------------------------------------------------------

if __name__ == "__main__":

    preprocessor = Preprocessor()

    bands = preprocessor.preprocess()