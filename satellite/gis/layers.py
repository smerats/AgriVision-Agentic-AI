"""
layers.py

AgriVision - GIS Layer Manager

Combines the generated satellite-analysis layers
for visualization.

Layers:
    NDVI
    EVI
    Vegetation
    Crop Health
    Risk Zone

Outputs:
    output/gis_layers.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PROJECT PATHS
# =========================================================

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

NDVI_PATH = os.path.join(
    OUTPUT_FOLDER,
    "ndvi.npy"
)

EVI_PATH = os.path.join(
    OUTPUT_FOLDER,
    "evi.npy"
)

VEGETATION_PATH = os.path.join(
    OUTPUT_FOLDER,
    "vegetation.npy"
)

HEALTH_PATH = os.path.join(
    OUTPUT_FOLDER,
    "health.npy"
)

RISK_PATH = os.path.join(
    OUTPUT_FOLDER,
    "risk_zone.npy"
)

OUTPUT_MAP = os.path.join(
    OUTPUT_FOLDER,
    "gis_layers.png"
)


# =========================================================
# GIS LAYER MANAGER
# =========================================================

class GISLayerManager:

    def __init__(self):

        os.makedirs(
            OUTPUT_FOLDER,
            exist_ok=True
        )

        self.max_display_size = 800


    # =====================================================
    # LOAD LAYERS
    # =====================================================

    def load_layers(self):

        print("Loading GIS layers...")

        paths = {
            "NDVI": NDVI_PATH,
            "EVI": EVI_PATH,
            "Vegetation": VEGETATION_PATH,
            "Crop Health": HEALTH_PATH,
            "Risk Zone": RISK_PATH
        }

        layers = {}

        for name, path in paths.items():

            if not os.path.exists(path):

                print(
                    f"⚠ {name} layer not found:"
                    f"\n  {path}"
                )

                continue

            print(
                f"✓ Loading {name}..."
            )

            layers[name] = np.load(
                path
            )

        if len(layers) == 0:

            raise FileNotFoundError(
                "No GIS layers were found."
            )

        return layers


    # =====================================================
    # DOWNSAMPLE
    # =====================================================

    def downsample(self, array):

        height, width = array.shape

        scale = max(
            height / self.max_display_size,
            width / self.max_display_size
        )

        if scale < 1:
            scale = 1

        step = int(
            np.ceil(scale)
        )

        return array[
            ::step,
            ::step
        ]


    # =====================================================
    # CREATE LAYER VISUALIZATION
    # =====================================================

    def create_visualization(self, layers):

        print(
            "\nGenerating GIS layer visualization..."
        )

        # -------------------------------------------------
        # Create one figure per layer
        # -------------------------------------------------

        for name, array in layers.items():

            display = self.downsample(
                array
            )

            # -------------------------------------------------
            # Mask zero / invalid pixels
            # -------------------------------------------------

            if name in [
                "Crop Health",
                "Risk Zone"
            ]:

                display = np.ma.masked_where(
                    display == 0,
                    display
                )

            else:

                display = np.ma.masked_invalid(
                    display
                )

            # -------------------------------------------------
            # Figure
            # -------------------------------------------------

            plt.figure(
                figsize=(8, 7)
            )

            # -------------------------------------------------
            # Select color map
            # -------------------------------------------------

            if name == "NDVI":

                cmap = "RdYlGn"
                vmin = -1
                vmax = 1

            elif name == "EVI":

                cmap = "RdYlGn"
                vmin = -1
                vmax = 1

            elif name == "Vegetation":

                cmap = "YlGn"
                vmin = 0
                vmax = 4

            elif name == "Crop Health":

                cmap = "RdYlGn"
                vmin = 1
                vmax = 3

            else:

                cmap = "RdYlGn"
                vmin = 1
                vmax = 3

            # -------------------------------------------------
            # Display
            # -------------------------------------------------

            image = plt.imshow(
                display,
                cmap=cmap,
                vmin=vmin,
                vmax=vmax,
                interpolation="nearest",
                aspect="auto"
            )

            plt.colorbar(
                image,
                fraction=0.046,
                pad=0.04
            )

            plt.title(
                f"AgriVision - {name} Layer",
                fontsize=15
            )

            plt.xlabel(
                "Satellite Pixel"
            )

            plt.ylabel(
                "Satellite Pixel"
            )

            plt.tight_layout()

            # -------------------------------------------------
            # Save each layer
            # -------------------------------------------------

            filename = (
                name.lower()
                .replace(" ", "_")
                + "_layer.png"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                filename
            )

            plt.savefig(
                output_path,
                dpi=120,
                bbox_inches="tight"
            )

            plt.close()

            print(
                f"✓ {name} layer saved:"
                f"\n  {output_path}"
            )


    # =====================================================
    # LAYER SUMMARY
    # =====================================================

    def print_summary(self, layers):

        print(
            "\n========== GIS LAYER SUMMARY =========="
        )

        for name, array in layers.items():

            valid = array[
                np.isfinite(array)
            ]

            if valid.size == 0:
                continue

            print(
                f"{name:15} : "
                f"Shape={array.shape}"
            )

        print(
            "========================================"
        )


    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        layers = self.load_layers()

        self.print_summary(
            layers
        )

        self.create_visualization(
            layers
        )

        print(
            "\n======================================"
        )

        print(
            "GIS Layer Module Completed Successfully."
        )

        print(
            "======================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    manager = GISLayerManager()

    manager.run()