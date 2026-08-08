"""
risk_zone.py

AgriVision - GIS Risk Zone Analysis

Uses:
    output/health.npy

Health classes:
    1 = Poor
    2 = Moderate
    3 = Healthy

Risk classes:
    1 = High Risk
    2 = Medium Risk
    3 = Low Risk

Outputs:
    output/risk_zone.npy
    output/risk_zone.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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

HEALTH_PATH = os.path.join(
    OUTPUT_FOLDER,
    "health.npy"
)

RISK_PATH = os.path.join(
    OUTPUT_FOLDER,
    "risk_zone.npy"
)

RISK_MAP = os.path.join(
    OUTPUT_FOLDER,
    "risk_zone.png"
)


# =========================================================
# RISK ZONE CLASS
# =========================================================

class RiskZoneAnalyzer:

    def __init__(self):

        os.makedirs(
            OUTPUT_FOLDER,
            exist_ok=True
        )

        # Only visualization is downsampled
        self.max_display_size = 1200


    # =====================================================
    # LOAD HEALTH DATA
    # =====================================================

    def load_health(self):

        print("Loading crop health data...")

        if not os.path.exists(HEALTH_PATH):

            raise FileNotFoundError(
                f"\nHealth data not found:\n"
                f"{HEALTH_PATH}\n\n"
                f"Run first:\n"
                f"python crop_health/health.py"
            )

        health = np.load(
            HEALTH_PATH
        )

        print(
            f"Health array shape: {health.shape}"
        )

        return health


    # =====================================================
    # GENERATE RISK ZONES
    # =====================================================

    def calculate_risk(self, health):

        print("\nCalculating risk zones...")

        risk = np.zeros(
            health.shape,
            dtype=np.uint8
        )

        # -------------------------------------------------
        # Health:
        #
        # 1 = Poor     -> High Risk
        # 2 = Moderate -> Medium Risk
        # 3 = Healthy  -> Low Risk
        #
        # 0 = NoData
        # -------------------------------------------------

        risk[health == 1] = 1
        risk[health == 2] = 2
        risk[health == 3] = 3

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        valid = risk > 0

        total = np.sum(valid)

        if total == 0:

            raise ValueError(
                "No valid crop-health pixels found."
            )

        high = np.sum(risk == 1)
        medium = np.sum(risk == 2)
        low = np.sum(risk == 3)

        print("\n========== RISK ZONE SUMMARY ==========")

        print(
            f"High Risk      : "
            f"{(high / total) * 100:.2f}%"
        )

        print(
            f"Medium Risk    : "
            f"{(medium / total) * 100:.2f}%"
        )

        print(
            f"Low Risk       : "
            f"{(low / total) * 100:.2f}%"
        )

        print("========================================")

        # -------------------------------------------------
        # Save full-resolution risk array
        # -------------------------------------------------

        np.save(
            RISK_PATH,
            risk
        )

        print(
            f"\nRisk zone array saved:\n"
            f"{RISK_PATH}"
        )

        return risk


    # =====================================================
    # DOWNSAMPLE ONLY FOR VISUALIZATION
    # =====================================================

    def downsample(self, risk):

        height, width = risk.shape

        scale = max(
            height / self.max_display_size,
            width / self.max_display_size
        )

        if scale < 1:
            scale = 1

        step = int(
            np.ceil(scale)
        )

        small = risk[
            ::step,
            ::step
        ]

        print(
            f"\nOriginal size : "
            f"{height} x {width}"
        )

        print(
            f"Display size  : "
            f"{small.shape[0]} x {small.shape[1]}"
        )

        print(
            f"Sampling step : {step}"
        )

        return small


    # =====================================================
    # CREATE RISK MAP
    # =====================================================

    def create_map(self, risk):

        print(
            "\nGenerating risk zone PNG..."
        )

        display_risk = self.downsample(
            risk
        )

        # -------------------------------------------------
        # Mask NoData
        # -------------------------------------------------

        masked = np.ma.masked_where(
            display_risk == 0,
            display_risk
        )

        # -------------------------------------------------
        # Risk colors
        # -------------------------------------------------

        cmap = ListedColormap(
            [
                "red",
                "yellow",
                "green"
            ]
        )

        cmap.set_bad(
            "white"
        )

        # -------------------------------------------------
        # Create figure
        # -------------------------------------------------

        plt.figure(
            figsize=(10, 8)
        )

        image = plt.imshow(
            masked,
            cmap=cmap,
            vmin=1,
            vmax=3,
            interpolation="nearest",
            aspect="auto"
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
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ]
        )

        colorbar.set_label(
            "Agricultural Risk",
            fontsize=11
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        plt.title(
            "AgriVision - Agricultural Risk Zones",
            fontsize=16
        )

        plt.xlabel(
            "Satellite Pixel"
        )

        plt.ylabel(
            "Satellite Pixel"
        )

        plt.grid(
            alpha=0.2
        )

        # -------------------------------------------------
        # Save PNG
        # -------------------------------------------------

        plt.savefig(
            RISK_MAP,
            dpi=150,
            bbox_inches="tight",
            facecolor="white"
        )

        plt.close()

        print(
            f"\nRisk zone map saved:\n"
            f"{RISK_MAP}"
        )


    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        health = self.load_health()

        risk = self.calculate_risk(
            health
        )

        self.create_map(
            risk
        )

        print(
            "\n======================================"
        )

        print(
            "Risk Zone Module Completed Successfully."
        )

        print(
            "======================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    analyzer = RiskZoneAnalyzer()

    analyzer.run()