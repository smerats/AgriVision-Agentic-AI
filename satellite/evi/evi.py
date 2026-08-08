"""
evi.py

AgriVision - Enhanced Vegetation Index (EVI)

Sentinel-2 bands:
B2 = Blue
B4 = Red
B8 = Near Infrared (NIR)

EVI formula:

EVI = 2.5 * (NIR - RED) /
      (NIR + 6*RED - 7.5*BLUE + 1)

Outputs:
    output/evi.npy
    output/evi_map.png
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PROJECT PATH
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

SATELLITE_IMAGES_DIR = os.path.join(
    PROJECT_ROOT,
    "satellite_images"
)

sys.path.insert(
    0,
    SATELLITE_IMAGES_DIR
)

from preprocess import Preprocessor


# =========================================================
# EVI CALCULATOR
# =========================================================

class EVICalculator:

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

        self.blue = bands["B2"]
        self.red = bands["B4"]
        self.nir = bands["B8"]

        print("\nB2 (BLUE) loaded.")
        print("B4 (RED) loaded.")
        print("B8 (NIR) loaded.")

    # =====================================================
    # CALCULATE EVI
    # =====================================================

    def calculate_evi(self):

        print("\nCalculating EVI...")

        # -------------------------------------------------
        # EVI denominator
        # -------------------------------------------------

        denominator = (
            self.nir
            + (6.0 * self.red)
            - (7.5 * self.blue)
            + 1.0
        )

        # -------------------------------------------------
        # Valid pixels
        # -------------------------------------------------

        valid = (
            ~np.isnan(self.blue)
            &
            ~np.isnan(self.red)
            &
            ~np.isnan(self.nir)
            &
            (denominator != 0)
        )

        # -------------------------------------------------
        # Create EVI array
        # -------------------------------------------------

        evi = np.full(
            self.red.shape,
            np.nan,
            dtype=np.float32
        )

        evi[valid] = (
            2.5
            *
            (
                self.nir[valid]
                -
                self.red[valid]
            )
            /
            denominator[valid]
        )

        # -------------------------------------------------
        # Remove invalid values
        # -------------------------------------------------

        evi[
            (evi < -1)
            |
            (evi > 1)
        ] = np.nan

        print("EVI calculation completed.")

        return evi

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self, evi):

        valid = evi[
            ~np.isnan(evi)
        ]

        if len(valid) == 0:

            raise ValueError(
                "No valid EVI pixels found."
            )

        print(
            "\n========== EVI STATISTICS =========="
        )

        print(
            f"Minimum EVI : "
            f"{np.min(valid):.3f}"
        )

        print(
            f"Maximum EVI : "
            f"{np.max(valid):.3f}"
        )

        print(
            f"Average EVI : "
            f"{np.mean(valid):.3f}"
        )

        print(
            f"Valid Pixels: "
            f"{len(valid):,}"
        )

        print(
            "===================================="
        )

    # =====================================================
    # VEGETATION SUMMARY
    # =====================================================

    def vegetation_summary(self, evi):

        valid = evi[
            ~np.isnan(evi)
        ]

        total = len(valid)

        low = np.sum(
            valid < 0.2
        )

        medium = np.sum(
            (valid >= 0.2)
            &
            (valid < 0.5)
        )

        high = np.sum(
            valid >= 0.5
        )

        print(
            "\n========== EVI VEGETATION SUMMARY =========="
        )

        print(
            f"Low Vegetation    : "
            f"{low * 100 / total:.2f}%"
        )

        print(
            f"Medium Vegetation : "
            f"{medium * 100 / total:.2f}%"
        )

        print(
            f"High Vegetation   : "
            f"{high * 100 / total:.2f}%"
        )

        print(
            "============================================="
        )

    # =====================================================
    # SAVE EVI ARRAY
    # =====================================================

    def save_array(self, evi):

        path = os.path.join(
            self.output_folder,
            "evi.npy"
        )

        np.save(
            path,
            evi
        )

        print(
            f"\nEVI array saved:\n{path}"
        )

    # =====================================================
    # SAVE EVI PNG MAP
    # =====================================================

    def save_map(self, evi):

        print(
            "\nGenerating EVI PNG map..."
        )

        # -------------------------------------------------
        # Valid pixels
        # -------------------------------------------------

        valid = ~np.isnan(evi)

        if not np.any(valid):

            raise ValueError(
                "No valid EVI pixels available."
            )

        # -------------------------------------------------
        # Find valid-data bounding box
        # -------------------------------------------------

        rows, cols = np.where(valid)

        row_min = rows.min()
        row_max = rows.max()

        col_min = cols.min()
        col_max = cols.max()

        print(
            f"Valid area rows: "
            f"{row_min} - {row_max}"
        )

        print(
            f"Valid area columns: "
            f"{col_min} - {col_max}"
        )

        # -------------------------------------------------
        # Crop valid area
        # -------------------------------------------------

        cropped = evi[
            row_min:row_max + 1,
            col_min:col_max + 1
        ]

        # -------------------------------------------------
        # Mask NoData
        # -------------------------------------------------

        masked = np.ma.masked_invalid(
            cropped
        )

        # -------------------------------------------------
        # Create figure
        # -------------------------------------------------

        plt.figure(
            figsize=(12, 10)
        )

        image = plt.imshow(
            masked,
            cmap="RdYlGn",
            vmin=-1,
            vmax=1,
            interpolation="nearest"
        )

        # NoData = white

        image.cmap.set_bad(
            "white"
        )

        # -------------------------------------------------
        # Colorbar
        # -------------------------------------------------

        colorbar = plt.colorbar(
            image,
            fraction=0.046,
            pad=0.04
        )

        colorbar.set_label(
            "EVI",
            fontsize=12
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        plt.title(
            "AgriVision - EVI Map",
            fontsize=18
        )

        plt.xlabel(
            "Satellite Pixel"
        )

        plt.ylabel(
            "Satellite Pixel"
        )

        # -------------------------------------------------
        # Save PNG
        # -------------------------------------------------

        save_path = os.path.join(
            self.output_folder,
            "evi_map.png"
        )

        plt.savefig(
            save_path,
            dpi=200,
            bbox_inches="tight",
            facecolor="white"
        )

        plt.close()

        print(
            f"\nEVI PNG saved:\n{save_path}"
        )

    # =====================================================
    # RUN COMPLETE MODULE
    # =====================================================

    def run(self):

        self.load_bands()

        evi = self.calculate_evi()

        self.statistics(
            evi
        )

        self.vegetation_summary(
            evi
        )

        self.save_array(
            evi
        )

        self.save_map(
            evi
        )

        print(
            "\n===================================="
        )

        print(
            "EVI Module Completed Successfully."
        )

        print(
            "===================================="


        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    calculator = EVICalculator()

    calculator.run()