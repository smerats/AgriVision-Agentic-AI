"""
map.py

AgriVision - GIS Crop Health Map

Uses:
    output/health.npy
    data/B4.tif

Features:
    - Handles Sentinel-2 NoData pixels
    - Uses GIS coordinates
    - Crops visualization to valid satellite footprint
    - Downsamples only for visualization
    - Does NOT modify original health.npy

Output:
    output/gis_health_map.png
"""

import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# ============================================================
# PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

OUTPUT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "output"
)

DATA_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data"
)

HEALTH_PATH = os.path.join(
    OUTPUT_FOLDER,
    "health.npy"
)

B4_PATH = os.path.join(
    DATA_FOLDER,
    "B4.tif"
)

B4_ALTERNATIVE = os.path.join(
    DATA_FOLDER,
    "B4.tif.tif"
)

OUTPUT_MAP = os.path.join(
    OUTPUT_FOLDER,
    "gis_health_map.png"
)


# ============================================================
# GIS HEALTH MAP
# ============================================================

class GISHealthMap:

    def __init__(self):

        os.makedirs(
            OUTPUT_FOLDER,
            exist_ok=True
        )

        # Visualization limit only
        self.max_display_size = 1200


    # ========================================================
    # FIND B4
    # ========================================================

    def find_b4(self):

        if os.path.exists(B4_PATH):
            return B4_PATH

        if os.path.exists(B4_ALTERNATIVE):
            return B4_ALTERNATIVE

        raise FileNotFoundError(
            "\nB4 GeoTIFF not found.\n\n"
            f"Checked:\n"
            f"{B4_PATH}\n"
            f"{B4_ALTERNATIVE}"
        )


    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):

        print("\nLoading crop health data...")

        if not os.path.exists(HEALTH_PATH):

            raise FileNotFoundError(
                f"\nHealth data not found:\n"
                f"{HEALTH_PATH}\n\n"
                "Run first:\n"
                "python crop_health/health.py"
            )

        health = np.load(
            HEALTH_PATH
        )

        print(
            f"Health array shape : {health.shape}"
        )


        b4_path = self.find_b4()

        print(
            "\nReading Sentinel-2 GIS information..."
        )

        with rasterio.open(b4_path) as src:

            transform = src.transform
            crs = src.crs
            bounds = src.bounds

            width = src.width
            height = src.height

            nodata = src.nodata

            # Raster validity mask
            valid_mask = src.read_masks(1) > 0


        print(
            f"Width      : {width}"
        )

        print(
            f"Height     : {height}"
        )

        print(
            f"CRS        : {crs}"
        )

        print(
            f"Bounds     : {bounds}"
        )

        print(
            f"NoData     : {nodata}"
        )

        print(
            f"Valid pixels   : {valid_mask.sum():,}"
        )

        print(
            f"Invalid pixels : {(~valid_mask).sum():,}"
        )


        if health.shape != valid_mask.shape:

            raise ValueError(
                "\nHealth and B4 dimensions do not match.\n"
                f"Health : {health.shape}\n"
                f"B4     : {valid_mask.shape}"
            )


        return (
            health,
            valid_mask,
            transform,
            crs,
            bounds
        )


    # ========================================================
    # FIND ACTUAL VALID FOOTPRINT
    # ========================================================

    def crop_to_valid_area(
        self,
        health,
        valid_mask
    ):

        print(
            "\nFinding actual satellite footprint..."
        )

        rows, cols = np.where(
            valid_mask
        )

        if len(rows) == 0:

            raise ValueError(
                "No valid satellite pixels found."
            )


        row_min = rows.min()
        row_max = rows.max()

        col_min = cols.min()
        col_max = cols.max()


        print(
            f"Valid rows    : {row_min} - {row_max}"
        )

        print(
            f"Valid columns : {col_min} - {col_max}"
        )


        # Crop both arrays

        cropped_health = health[
            row_min:row_max + 1,
            col_min:col_max + 1
        ]

        cropped_mask = valid_mask[
            row_min:row_max + 1,
            col_min:col_max + 1
        ]


        print(
            f"Cropped size  : {cropped_health.shape}"
        )


        return (
            cropped_health,
            cropped_mask,
            row_min,
            row_max,
            col_min,
            col_max
        )


    # ========================================================
    # DOWNSAMPLE
    # ========================================================

    def downsample(
        self,
        health,
        valid_mask
    ):

        height, width = health.shape

        scale = max(
            height / self.max_display_size,
            width / self.max_display_size
        )

        step = max(
            1,
            int(np.ceil(scale))
        )


        small_health = health[
            ::step,
            ::step
        ]

        small_mask = valid_mask[
            ::step,
            ::step
        ]


        print(
            f"\nVisualization sampling step : {step}"
        )

        print(
            f"Final display size           : "
            f"{small_health.shape}"
        )


        return (
            small_health,
            small_mask,
            step
        )


    # ========================================================
    # CREATE MAP
    # ========================================================

    def create_map(
        self,
        health,
        valid_mask,
        transform,
        crs,
        bounds
    ):

        print(
            "\nPreparing GIS visualization..."
        )


        # ----------------------------------------------------
        # STEP 1
        # Crop to valid satellite footprint
        # ----------------------------------------------------

        (
            cropped_health,
            cropped_mask,
            row_min,
            row_max,
            col_min,
            col_max
        ) = self.crop_to_valid_area(
            health,
            valid_mask
        )


        # ----------------------------------------------------
        # STEP 2
        # Downsample for visualization
        # ----------------------------------------------------

        (
            display_health,
            display_mask,
            step
        ) = self.downsample(
            cropped_health,
            cropped_mask
        )


        # ----------------------------------------------------
        # STEP 3
        # Keep only actual health classes
        # ----------------------------------------------------

        valid_health = (
            display_mask
            &
            np.isin(
                display_health,
                [1, 2, 3]
            )
        )


        masked_health = np.ma.masked_where(
            ~valid_health,
            display_health
        )


        # ----------------------------------------------------
        # STEP 4
        # Calculate cropped GIS coordinates
        # ----------------------------------------------------

        pixel_width = transform.a

        pixel_height = abs(
            transform.e
        )


        cropped_left = (
            bounds.left
            +
            col_min * pixel_width
        )


        cropped_right = (
            bounds.left
            +
            (col_max + 1) * pixel_width
        )


        cropped_top = (
            bounds.top
            -
            row_min * pixel_height
        )


        cropped_bottom = (
            bounds.top
            -
            (row_max + 1) * pixel_height
        )


        cropped_extent = [
            cropped_left,
            cropped_right,
            cropped_bottom,
            cropped_top
        ]


        print(
            "\nCropped GIS extent:"
        )

        print(
            f"Left   : {cropped_left}"
        )

        print(
            f"Right  : {cropped_right}"
        )

        print(
            f"Bottom : {cropped_bottom}"
        )

        print(
            f"Top    : {cropped_top}"
        )


        # ====================================================
        # COLOR MAP
        # ====================================================

        cmap = ListedColormap(
            [
                "red",
                "yellow",
                "green"
            ]
        )

        # NoData = white

        cmap.set_bad(
            "white"
        )


        # ====================================================
        # CREATE FIGURE
        # ====================================================

        fig, ax = plt.subplots(
            figsize=(12, 9)
        )


        image = ax.imshow(
            masked_health,
            cmap=cmap,
            vmin=1,
            vmax=3,
            extent=cropped_extent,
            interpolation="nearest",
            aspect="auto"
        )


        # ====================================================
        # COLORBAR
        # ====================================================

        colorbar = plt.colorbar(
            image,
            ax=ax,
            ticks=[1, 2, 3],
            fraction=0.046,
            pad=0.04
        )


        colorbar.ax.set_yticklabels(
            [
                "Poor",
                "Moderate",
                "Healthy"
            ]
        )


        colorbar.set_label(
            "Crop Health",
            fontsize=12
        )


        # ====================================================
        # TITLE
        # ====================================================

        ax.set_title(
            "AgriVision - GIS Crop Health Map",
            fontsize=18,
            fontweight="bold"
        )


        # ====================================================
        # AXIS LABELS
        # ====================================================

        ax.set_xlabel(
            "Easting (meters)",
            fontsize=11
        )

        ax.set_ylabel(
            "Northing (meters)",
            fontsize=11
        )


        # ====================================================
        # CRS
        # ====================================================

        ax.text(
            0.02,
            0.02,
            f"CRS: {crs}",
            transform=ax.transAxes,
            fontsize=9,
            bbox=dict(
                facecolor="white",
                edgecolor="gray",
                alpha=0.85
            )
        )


        # ====================================================
        # GRID
        # ====================================================

        ax.grid(
            alpha=0.2
        )


        # ====================================================
        # SAVE
        # ====================================================

        print(
            "\nSaving GIS PNG..."
        )


        plt.savefig(
            OUTPUT_MAP,
            dpi=150,
            bbox_inches="tight",
            facecolor="white"
        )


        plt.close()


        print(
            "\nGIS map saved:"
        )

        print(
            OUTPUT_MAP
        )


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        (
            health,
            valid_mask,
            transform,
            crs,
            bounds
        ) = self.load_data()


        self.create_map(
            health,
            valid_mask,
            transform,
            crs,
            bounds
        )


        print(
            "\n=========================================="
        )

        print(
            "GIS Module Completed Successfully."
        )

        print(
            "==========================================" 
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    gis_map = GISHealthMap()

    gis_map.run()