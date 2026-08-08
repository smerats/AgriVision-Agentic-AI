"""
ndvi.py

AgriVision - Satellite Image Analysis

Calculates NDVI using:
B4 = Red
B8 = Near Infrared (NIR)

Outputs:
    output/ndvi.npy
    output/ndvi_map.png
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PROJECT PATH
# =========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

SATELLITE_IMAGES_DIR = os.path.join(
    PROJECT_ROOT,
    "satellite_images"
)

sys.path.insert(0, SATELLITE_IMAGES_DIR)

from preprocess import Preprocessor


# =========================================================
# NDVI CALCULATOR
# =========================================================

class NDVICalculator:

    def __init__(self):

        self.output_folder = os.path.join(
            PROJECT_ROOT,
            "output"
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    # =====================================================
    # LOAD BANDS
    # =====================================================

    def load_bands(self):

        print("Reading Sentinel-2 bands...")

        processor = Preprocessor()

        bands = processor.preprocess()

        self.red = bands["B4"]
        self.nir = bands["B8"]

        print("\nB4 (RED) loaded.")
        print("B8 (NIR) loaded.")

    # =====================================================
    # CALCULATE NDVI
    # =====================================================

    def calculate_ndvi(self):

        print("\nCalculating NDVI...")

        denominator = self.nir + self.red

        valid = (
            ~np.isnan(self.nir)
            &
            ~np.isnan(self.red)
            &
            (denominator != 0)
        )

        ndvi = np.full(
            self.red.shape,
            np.nan,
            dtype=np.float32
        )

        ndvi[valid] = (
            (self.nir[valid] - self.red[valid])
            /
            denominator[valid]
        )

        # Remove impossible values
        ndvi[
            (ndvi < -1) |
            (ndvi > 1)
        ] = np.nan

        print("NDVI calculation completed.")

        return ndvi

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self, ndvi):

        valid = ndvi[
            ~np.isnan(ndvi)
        ]

        if len(valid) == 0:
            raise ValueError(
                "No valid NDVI pixels found."
            )

        print("\n========== NDVI STATISTICS ==========")

        print(
            f"Minimum NDVI : {np.min(valid):.3f}"
        )

        print(
            f"Maximum NDVI : {np.max(valid):.3f}"
        )

        print(
            f"Average NDVI : {np.mean(valid):.3f}"
        )

        print(
            f"Valid Pixels : {len(valid):,}"
        )

        print(
            "====================================="
        )

    # =====================================================
    # VEGETATION SUMMARY
    # =====================================================

    def vegetation_summary(self, ndvi):

        valid = ndvi[
            ~np.isnan(ndvi)
        ]

        total = len(valid)

        water_barren = np.sum(
            valid < 0
        )

        poor = np.sum(
            (valid >= 0) &
            (valid < 0.2)
        )

        moderate = np.sum(
            (valid >= 0.2) &
            (valid < 0.5)
        )

        healthy = np.sum(
            valid >= 0.5
        )

        print("\n========== VEGETATION SUMMARY ==========")

        print(
            f"Water/Barren       : "
            f"{water_barren * 100 / total:.2f}%"
        )

        print(
            f"Poor Vegetation    : "
            f"{poor * 100 / total:.2f}%"
        )

        print(
            f"Moderate Vegetation: "
            f"{moderate * 100 / total:.2f}%"
        )

        print(
            f"Healthy Vegetation : "
            f"{healthy * 100 / total:.2f}%"
        )

        print(
            "========================================"
        )

    # =====================================================
    # SAVE NDVI ARRAY
    # =====================================================

    def save_array(self, ndvi):

        path = os.path.join(
            self.output_folder,
            "ndvi.npy"
        )

        np.save(
            path,
            ndvi
        )

        print(
            f"\nNDVI array saved:\n{path}"
        )

    # =====================================================
    # SAVE PNG MAP
    # =====================================================

    def save_map(self, ndvi):

        print("\nGenerating NDVI PNG map...")

        # -------------------------------------------------
        # Find valid pixels
        # -------------------------------------------------

        valid_mask = ~np.isnan(ndvi)

        if not np.any(valid_mask):

            raise ValueError(
                "No valid NDVI pixels available for mapping."
            )

        # -------------------------------------------------
        # Find valid-data bounding box
        # -------------------------------------------------

        rows, cols = np.where(valid_mask)

        row_min = rows.min()
        row_max = rows.max()

        col_min = cols.min()
        col_max = cols.max()

        print(
            f"Valid area rows: {row_min} - {row_max}"
        )

        print(
            f"Valid area columns: {col_min} - {col_max}"
        )

        # -------------------------------------------------
        # Crop to valid area
        # -------------------------------------------------

        cropped_ndvi = ndvi[
            row_min:row_max + 1,
            col_min:col_max + 1
        ]

        # Mask NaN values
        masked_ndvi = np.ma.masked_invalid(
            cropped_ndvi
        )

        # -------------------------------------------------
        # CREATE FIGURE
        # -------------------------------------------------

        plt.figure(
            figsize=(12, 10)
        )

        image = plt.imshow(
            masked_ndvi,
            cmap="RdYlGn",
            vmin=-1,
            vmax=1,
            interpolation="nearest"
        )

        # NoData shown as white
        image.cmap.set_bad("white")

        # -------------------------------------------------
        # COLORBAR
        # -------------------------------------------------

        colorbar = plt.colorbar(
            image,
            fraction=0.046,
            pad=0.04
        )

        colorbar.set_label(
            "NDVI",
            fontsize=12
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        plt.title(
            "AgriVision - NDVI Map",
            fontsize=18
        )

        plt.xlabel(
            "Satellite Pixel"
        )

        plt.ylabel(
            "Satellite Pixel"
        )

        # -------------------------------------------------
        # SAVE PNG
        # -------------------------------------------------

        save_path = os.path.join(
            self.output_folder,
            "ndvi_map.png"
        )

        plt.savefig(
            save_path,
            dpi=200,
            bbox_inches="tight",
            facecolor="white"
        )

        plt.close()

        print(
            f"\nNDVI PNG saved:\n{save_path}"
        )

    # =====================================================
    # RUN COMPLETE MODULE
    # =====================================================

    def run(self):

        self.load_bands()

        ndvi = self.calculate_ndvi()

        self.statistics(ndvi)

        self.vegetation_summary(ndvi)

        self.save_array(ndvi)

        self.save_map(ndvi)

        print(
            "\n====================================="
        )

        print(
            "NDVI Module Completed Successfully."
        )

        print(
            "====================================="
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    calculator = NDVICalculator()

    calculator.run()