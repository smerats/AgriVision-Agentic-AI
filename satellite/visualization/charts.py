"""
charts.py

AgriVision - Satellite Analysis Visualization

Uses:
    output/ndvi.npy
    output/evi.npy
    output/health.npy
    output/risk_zone.npy
    output/health_score.json

Outputs:
    output/charts/
        crop_health_distribution.png
        risk_zone_distribution.png
        ndvi_distribution.png
        evi_distribution.png
        crop_health_score.png
"""

import os
import json

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
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

CHART_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "charts"
)

NDVI_PATH = os.path.join(
    OUTPUT_FOLDER,
    "ndvi.npy"
)

EVI_PATH = os.path.join(
    OUTPUT_FOLDER,
    "evi.npy"
)

HEALTH_PATH = os.path.join(
    OUTPUT_FOLDER,
    "health.npy"
)

RISK_PATH = os.path.join(
    OUTPUT_FOLDER,
    "risk_zone.npy"
)

SCORE_PATH = os.path.join(
    OUTPUT_FOLDER,
    "health_score.json"
)


# ============================================================
# CHART VISUALIZATION CLASS
# ============================================================

class AgriVisionCharts:

    def __init__(self):

        os.makedirs(
            CHART_FOLDER,
            exist_ok=True
        )


    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):

        print(
            "\nLoading visualization data..."
        )

        data = {}

        # ----------------------------------------------------
        # NDVI
        # ----------------------------------------------------

        if os.path.exists(NDVI_PATH):

            data["ndvi"] = np.load(
                NDVI_PATH
            )

            print(
                "✓ NDVI loaded"
            )

        else:

            print(
                "⚠ NDVI file not found"
            )


        # ----------------------------------------------------
        # EVI
        # ----------------------------------------------------

        if os.path.exists(EVI_PATH):

            data["evi"] = np.load(
                EVI_PATH
            )

            print(
                "✓ EVI loaded"
            )

        else:

            print(
                "⚠ EVI file not found"
            )


        # ----------------------------------------------------
        # Health
        # ----------------------------------------------------

        if os.path.exists(HEALTH_PATH):

            data["health"] = np.load(
                HEALTH_PATH
            )

            print(
                "✓ Crop Health loaded"
            )

        else:

            print(
                "⚠ Health file not found"
            )


        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        if os.path.exists(RISK_PATH):

            data["risk"] = np.load(
                RISK_PATH
            )

            print(
                "✓ Risk Zone loaded"
            )

        else:

            print(
                "⚠ Risk Zone file not found"
            )


        # ----------------------------------------------------
        # Health score
        # ----------------------------------------------------

        if os.path.exists(SCORE_PATH):

            with open(
                SCORE_PATH,
                "r"
            ) as file:

                data["score"] = json.load(
                    file
                )

            print(
                "✓ Health Score loaded"
            )

        else:

            print(
                "⚠ Health Score file not found"
            )


        return data


    # ========================================================
    # CROP HEALTH CHART
    # ========================================================

    def crop_health_chart(
        self,
        health
    ):

        print(
            "\nGenerating Crop Health chart..."
        )


        # Count valid pixels

        poor = np.sum(
            health == 1
        )

        moderate = np.sum(
            health == 2
        )

        healthy = np.sum(
            health == 3
        )


        total = (
            poor
            +
            moderate
            +
            healthy
        )


        if total == 0:

            print(
                "No valid crop health data."
            )

            return


        values = [
            poor,
            moderate,
            healthy
        ]


        percentages = [
            (value / total) * 100
            for value in values
        ]


        labels = [
            "Poor",
            "Moderate",
            "Healthy"
        ]


        plt.figure(
            figsize=(8, 6)
        )


        bars = plt.bar(
            labels,
            percentages
        )


        plt.ylabel(
            "Percentage of Area (%)"
        )


        plt.xlabel(
            "Crop Health"
        )


        plt.title(
            "AgriVision - Crop Health Distribution",
            fontsize=15
        )


        # Display values

        for bar, value in zip(
            bars,
            percentages
        ):

            plt.text(
                bar.get_x()
                +
                bar.get_width() / 2,
                value + 0.5,
                f"{value:.2f}%",
                ha="center"
            )


        plt.ylim(
            0,
            max(percentages) + 10
        )


        plt.tight_layout()


        output = os.path.join(
            CHART_FOLDER,
            "crop_health_distribution.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()


        print(
            f"✓ Saved:\n{output}"
        )


    # ========================================================
    # RISK ZONE CHART
    # ========================================================

    def risk_zone_chart(
        self,
        risk
    ):

        print(
            "\nGenerating Risk Zone chart..."
        )


        high = np.sum(
            risk == 1
        )

        medium = np.sum(
            risk == 2
        )

        low = np.sum(
            risk == 3
        )


        total = (
            high
            +
            medium
            +
            low
        )


        if total == 0:

            print(
                "No valid risk-zone data."
            )

            return


        values = [
            high,
            medium,
            low
        ]


        percentages = [
            (value / total) * 100
            for value in values
        ]


        labels = [
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ]


        plt.figure(
            figsize=(8, 6)
        )


        bars = plt.bar(
            labels,
            percentages
        )


        plt.ylabel(
            "Percentage of Area (%)"
        )


        plt.xlabel(
            "Risk Level"
        )


        plt.title(
            "AgriVision - Agricultural Risk Zones",
            fontsize=15
        )


        for bar, value in zip(
            bars,
            percentages
        ):

            plt.text(
                bar.get_x()
                +
                bar.get_width() / 2,
                value + 0.5,
                f"{value:.2f}%",
                ha="center"
            )


        plt.ylim(
            0,
            max(percentages) + 10
        )


        plt.tight_layout()


        output = os.path.join(
            CHART_FOLDER,
            "risk_zone_distribution.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()


        print(
            f"✓ Saved:\n{output}"
        )


    # ========================================================
    # NDVI DISTRIBUTION
    # ========================================================

    def ndvi_chart(
        self,
        ndvi
    ):

        print(
            "\nGenerating NDVI distribution..."
        )


        valid = ndvi[
            np.isfinite(ndvi)
        ]


        # Remove invalid extreme values

        valid = valid[
            (valid >= -1)
            &
            (valid <= 1)
        ]


        if valid.size == 0:

            print(
                "No valid NDVI data."
            )

            return


        plt.figure(
            figsize=(9, 6)
        )


        plt.hist(
            valid,
            bins=50
        )


        plt.xlabel(
            "NDVI Value"
        )


        plt.ylabel(
            "Number of Pixels"
        )


        plt.title(
            "AgriVision - NDVI Distribution",
            fontsize=15
        )


        plt.axvline(
            np.mean(valid),
            linestyle="--",
            label=(
                f"Mean NDVI = "
                f"{np.mean(valid):.3f}"
            )
        )


        plt.legend()


        plt.tight_layout()


        output = os.path.join(
            CHART_FOLDER,
            "ndvi_distribution.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()


        print(
            f"✓ Saved:\n{output}"
        )


    # ========================================================
    # EVI DISTRIBUTION
    # ========================================================

    def evi_chart(
        self,
        evi
    ):

        print(
            "\nGenerating EVI distribution..."
        )


        valid = evi[
            np.isfinite(evi)
        ]


        valid = valid[
            (valid >= -1)
            &
            (valid <= 1)
        ]


        if valid.size == 0:

            print(
                "No valid EVI data."
            )

            return


        plt.figure(
            figsize=(9, 6)
        )


        plt.hist(
            valid,
            bins=50
        )


        plt.xlabel(
            "EVI Value"
        )


        plt.ylabel(
            "Number of Pixels"
        )


        plt.title(
            "AgriVision - EVI Distribution",
            fontsize=15
        )


        plt.axvline(
            np.mean(valid),
            linestyle="--",
            label=(
                f"Mean EVI = "
                f"{np.mean(valid):.3f}"
            )
        )


        plt.legend()


        plt.tight_layout()


        output = os.path.join(
            CHART_FOLDER,
            "evi_distribution.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()


        print(
            f"✓ Saved:\n{output}"
        )


    # ========================================================
    # OVERALL HEALTH SCORE
    # ========================================================

    def health_score_chart(
        self,
        score_data
    ):

        print(
            "\nGenerating overall health score..."
        )


        score = score_data.get(
            "score",
            0
        )


        status = score_data.get(
            "status",
            "Unknown"
        )


        plt.figure(
            figsize=(8, 5)
        )


        bars = plt.bar(
            ["Crop Health Score"],
            [score]
        )


        plt.ylim(
            0,
            100
        )


        plt.ylabel(
            "Score (0 - 100)"
        )


        plt.title(
            "AgriVision - Overall Crop Health Score",
            fontsize=15
        )


        plt.text(
            0,
            score + 3,
            f"{score:.2f}/100\n{status}",
            ha="center",
            fontsize=12
        )


        plt.tight_layout()


        output = os.path.join(
            CHART_FOLDER,
            "crop_health_score.png"
        )


        plt.savefig(
            output,
            dpi=150
        )


        plt.close()


        print(
            f"✓ Saved:\n{output}"
        )


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        data = self.load_data()


        # ----------------------------------------------------
        # Generate available charts
        # ----------------------------------------------------

        if "health" in data:

            self.crop_health_chart(
                data["health"]
            )


        if "risk" in data:

            self.risk_zone_chart(
                data["risk"]
            )


        if "ndvi" in data:

            self.ndvi_chart(
                data["ndvi"]
            )


        if "evi" in data:

            self.evi_chart(
                data["evi"]
            )


        if "score" in data:

            self.health_score_chart(
                data["score"]
            )


        print(
            "\n=========================================="
        )

        print(
            "AgriVision Visualization Completed."
        )

        print(
            "Charts saved in:"
        )

        print(
            CHART_FOLDER
        )

        print(
            "=========================================="
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    charts = AgriVisionCharts()

    charts.run()