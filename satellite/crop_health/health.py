"""
health.py

AgriVision - Crop Health Analysis

Uses:
    NDVI
    EVI

to generate a combined crop health map.

Health classes:

0 = NoData
1 = Poor
2 = Moderate
3 = Healthy

Outputs:
    output/health.npy
    output/health_map.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap


# =========================================================
# PROJECT PATH
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

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =========================================================
# CROP HEALTH ANALYZER
# =========================================================

class CropHealthAnalyzer:

    def __init__(self):

        self.ndvi_path = os.path.join(
            OUTPUT_FOLDER,
            "ndvi.npy"
        )

        self.evi_path = os.path.join(
            OUTPUT_FOLDER,
            "evi.npy"
        )

        self.health_path = os.path.join(
            OUTPUT_FOLDER,
            "health.npy"
        )

        self.map_path = os.path.join(
            OUTPUT_FOLDER,
            "health_map.png"
        )

    # =====================================================
    # LOAD NDVI AND EVI
    # =====================================================

    def load_indices(self):

        print("Loading NDVI and EVI data...")

        if not os.path.exists(
            self.ndvi_path
        ):
            raise FileNotFoundError(
                f"NDVI file not found:\n"
                f"{self.ndvi_path}"
            )

        if not os.path.exists(
            self.evi_path
        ):
            raise FileNotFoundError(
                f"EVI file not found:\n"
                f"{self.evi_path}"
            )

        ndvi = np.load(
            self.ndvi_path
        )

        evi = np.load(
            self.evi_path
        )

        print(
            f"NDVI shape: {ndvi.shape}"
        )

        print(
            f"EVI shape: {evi.shape}"
        )

        # Make sure both arrays have same shape
        if ndvi.shape != evi.shape:

            raise ValueError(
                "NDVI and EVI shapes are different."
            )

        return ndvi, evi

    # =====================================================
    # CALCULATE HEALTH SCORE
    # =====================================================

    def calculate_health_score(
        self,
        ndvi,
        evi
    ):

        print(
            "\nCalculating combined crop health..."
        )

        # -------------------------------------------------
        # Valid pixels
        # -------------------------------------------------

        valid = (
            ~np.isnan(ndvi)
            &
            ~np.isnan(evi)
        )

        # -------------------------------------------------
        # Normalize NDVI and EVI
        #
        # -1 → 0
        #  0 → 0.5
        # +1 → 1
        # -------------------------------------------------

        ndvi_normalized = (
            ndvi + 1.0
        ) / 2.0

        evi_normalized = (
            evi + 1.0
        ) / 2.0

        # -------------------------------------------------
        # Combined score
        #
        # NDVI = 60%
        # EVI  = 40%
        # -------------------------------------------------

        combined = (
            0.60 * ndvi_normalized
            +
            0.40 * evi_normalized
        )

        # -------------------------------------------------
        # Convert to 0-100
        # -------------------------------------------------

        health_score = np.full(
            ndvi.shape,
            np.nan,
            dtype=np.float32
        )

        health_score[valid] = (
            combined[valid] * 100.0
        )

        # -------------------------------------------------
        # Remove impossible values
        # -------------------------------------------------

        health_score[
            (health_score < 0)
            |
            (health_score > 100)
        ] = np.nan

        return health_score

    # =====================================================
    # CLASSIFY HEALTH
    # =====================================================

    def classify_health(
        self,
        health_score,
        ndvi
    ):

        print(
            "\nClassifying crop health..."
        )

        # -------------------------------------------------
        # 0 = NoData
        # 1 = Poor
        # 2 = Moderate
        # 3 = Healthy
        # -------------------------------------------------

        health = np.zeros(
            health_score.shape,
            dtype=np.uint8
        )

        valid = ~np.isnan(
            health_score
        )

        # -------------------------------------------------
        # POOR
        #
        # Score < 40
        # -------------------------------------------------

        health[
            valid &
            (health_score < 40)
        ] = 1

        # -------------------------------------------------
        # MODERATE
        #
        # 40 <= Score < 70
        # -------------------------------------------------

        health[
            valid &
            (health_score >= 40) &
            (health_score < 70)
        ] = 2

        # -------------------------------------------------
        # HEALTHY
        #
        # Score >= 70
        # -------------------------------------------------

        health[
            valid &
            (health_score >= 70)
        ] = 3

        return health

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(
        self,
        health
    ):

        valid = health > 0

        total = np.sum(
            valid
        )

        if total == 0:

            raise ValueError(
                "No valid crop health pixels found."
            )

        poor = np.sum(
            health == 1
        )

        moderate = np.sum(
            health == 2
        )

        healthy = np.sum(
            health == 3
        )

        print(
            "\n========== CROP HEALTH =========="
        )

        print(
            f"Poor Crops      : "
            f"{poor * 100 / total:.2f}%"
        )

        print(
            f"Moderate Crops  : "
            f"{moderate * 100 / total:.2f}%"
        )

        print(
            f"Healthy Crops   : "
            f"{healthy * 100 / total:.2f}%"
        )

        print(
            "================================="
        )

    # =====================================================
    # HEALTH SCORE STATISTICS
    # =====================================================

    def score_statistics(
        self,
        health_score
    ):

        valid = health_score[
            ~np.isnan(
                health_score
            )
        ]

        if len(valid) == 0:
            return

        print(
            "\n========== HEALTH SCORE =========="
        )

        print(
            f"Minimum Score : "
            f"{np.min(valid):.2f}"
        )

        print(
            f"Maximum Score : "
            f"{np.max(valid):.2f}"
        )

        print(
            f"Average Score : "
            f"{np.mean(valid):.2f}"
        )

        print(
            "=================================="
        )

    # =====================================================
    # SAVE HEALTH ARRAY
    # =====================================================

    def save_array(
        self,
        health
    ):

        np.save(
            self.health_path,
            health
        )

        print(
            f"\nHealth array saved:\n"
            f"{self.health_path}"
        )

    # =====================================================
    # SAVE HEALTH MAP
    # =====================================================

    def save_map(
        self,
        health
    ):

        print(
            "\nGenerating crop health PNG map..."
        )

        # -------------------------------------------------
        # Valid pixels
        # -------------------------------------------------

        valid = health > 0

        if not np.any(valid):

            raise ValueError(
                "No valid health pixels available."
            )

        # -------------------------------------------------
        # Find valid area
        # -------------------------------------------------

        rows, cols = np.where(
            valid
        )

        row_min = rows.min()
        row_max = rows.max()

        col_min = cols.min()
        col_max = cols.max()

        # -------------------------------------------------
        # Crop to satellite footprint
        # -------------------------------------------------

        cropped = health[
            row_min:row_max + 1,
            col_min:col_max + 1
        ]

        # -------------------------------------------------
        # Mask NoData
        # -------------------------------------------------

        masked = np.ma.masked_where(
            cropped == 0,
            cropped
        )

        # -------------------------------------------------
        # Health colors
        #
        # Poor     = Red
        # Moderate = Yellow
        # Healthy  = Green
        # -------------------------------------------------

        cmap = ListedColormap(
            [
                "red",
                "yellow",
                "green"
            ]
        )

        # -------------------------------------------------
        # Figure
        # -------------------------------------------------

        plt.figure(
            figsize=(12, 10)
        )

        image = plt.imshow(
            masked,
            cmap=cmap,
            vmin=1,
            vmax=3,
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

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        plt.title(
            "AgriVision - Crop Health Map",
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

        plt.savefig(
            self.map_path,
            dpi=200,
            bbox_inches="tight",
            facecolor="white"
        )

        plt.close()

        print(
            f"\nHealth map saved:\n"
            f"{self.map_path}"
        )

    # =====================================================
    # COMPLETE PIPELINE
    # =====================================================

    def run(self):

        # Load NDVI + EVI

        ndvi, evi = (
            self.load_indices()
        )

        # Calculate numerical health score

        health_score = (
            self.calculate_health_score(
                ndvi,
                evi
            )
        )

        # Classify into 3 categories

        health = (
            self.classify_health(
                health_score,
                ndvi
            )
        )

        # Print statistics

        self.score_statistics(
            health_score
        )

        self.statistics(
            health
        )

        # Save classification

        self.save_array(
            health
        )

        # Save PNG map

        self.save_map(
            health
        )

        print(
            "\n================================="
        )

        print(
            "Crop Health Module Completed Successfully."
        )

        print(
            "================================="
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    analyzer = CropHealthAnalyzer()

    analyzer.run()