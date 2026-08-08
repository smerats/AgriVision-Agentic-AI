"""
health_score.py

AgriVision - Overall Crop Health Score

Reads:
    output/health.npy

Health classes:
    0 = NoData
    1 = Poor
    2 = Moderate
    3 = Healthy

Outputs:
    output/health_score.txt
"""

import os
import numpy as np


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
# HEALTH SCORE ANALYZER
# =========================================================

class HealthScoreAnalyzer:

    def __init__(self):

        self.health_path = os.path.join(
            OUTPUT_FOLDER,
            "health.npy"
        )

        self.output_path = os.path.join(
            OUTPUT_FOLDER,
            "health_score.txt"
        )

    # =====================================================
    # LOAD HEALTH MAP
    # =====================================================

    def load_health(self):

        print("Loading crop health data...")

        if not os.path.exists(
            self.health_path
        ):

            raise FileNotFoundError(
                f"Health file not found:\n"
                f"{self.health_path}\n\n"
                "Run health.py first."
            )

        health = np.load(
            self.health_path
        )

        print(
            f"Health map shape: {health.shape}"
        )

        return health

    # =====================================================
    # CALCULATE CLASS PERCENTAGES
    # =====================================================

    def calculate_percentages(
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

        poor_percent = (
            poor * 100.0 / total
        )

        moderate_percent = (
            moderate * 100.0 / total
        )

        healthy_percent = (
            healthy * 100.0 / total
        )

        return (
            poor_percent,
            moderate_percent,
            healthy_percent
        )

    # =====================================================
    # CALCULATE OVERALL SCORE
    # =====================================================

    def calculate_overall_score(
        self,
        poor_percent,
        moderate_percent,
        healthy_percent
    ):

        # -------------------------------------------------
        # Assign scores to health categories
        #
        # Poor     = 25
        # Moderate = 60
        # Healthy  = 90
        # -------------------------------------------------

        score = (
            (poor_percent * 25)
            +
            (moderate_percent * 60)
            +
            (healthy_percent * 90)
        ) / 100.0

        return score

    # =====================================================
    # INTERPRET SCORE
    # =====================================================

    def interpret_score(
        self,
        score
    ):

        if score < 40:

            status = "POOR"

            recommendation = (
                "Large portions of the area "
                "show vegetation stress. "
                "Further field inspection "
                "is recommended."
            )

        elif score < 70:

            status = "MODERATE"

            recommendation = (
                "Vegetation condition is mixed. "
                "Monitor stressed areas and "
                "consider targeted inspection."
            )

        else:

            status = "HEALTHY"

            recommendation = (
                "Vegetation condition is generally "
                "healthy. Continue regular monitoring."
            )

        return status, recommendation

    # =====================================================
    # PRINT REPORT
    # =====================================================

    def print_report(
        self,
        poor_percent,
        moderate_percent,
        healthy_percent,
        score,
        status,
        recommendation
    ):

        print(
            "\n=========================================="
        )

        print(
            "       AGRIVISION CROP HEALTH REPORT"
        )

        print(
            "=========================================="
        )

        print(
            f"Poor Area       : "
            f"{poor_percent:.2f}%"
        )

        print(
            f"Moderate Area   : "
            f"{moderate_percent:.2f}%"
        )

        print(
            f"Healthy Area    : "
            f"{healthy_percent:.2f}%"
        )

        print(
            "------------------------------------------"
        )

        print(
            f"Overall Health Score : "
            f"{score:.2f} / 100"
        )

        print(
            f"Overall Status       : "
            f"{status}"
        )

        print(
            "------------------------------------------"
        )

        print(
            "Recommendation:"
        )

        print(
            recommendation
        )

        print(
            "=========================================="
        )

    # =====================================================
    # SAVE REPORT
    # =====================================================

    def save_report(
        self,
        poor_percent,
        moderate_percent,
        healthy_percent,
        score,
        status,
        recommendation
    ):

        with open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "AGRIVISION CROP HEALTH REPORT\n"
            )

            file.write(
                "==============================\n\n"
            )

            file.write(
                f"Poor Area      : "
                f"{poor_percent:.2f}%\n"
            )

            file.write(
                f"Moderate Area  : "
                f"{moderate_percent:.2f}%\n"
            )

            file.write(
                f"Healthy Area   : "
                f"{healthy_percent:.2f}%\n\n"
            )

            file.write(
                f"Overall Health Score : "
                f"{score:.2f}/100\n"
            )

            file.write(
                f"Overall Status      : "
                f"{status}\n\n"
            )

            file.write(
                "Recommendation:\n"
            )

            file.write(
                recommendation
            )

        print(
            f"\nHealth score report saved:\n"
            f"{self.output_path}"
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        health = self.load_health()

        (
            poor_percent,
            moderate_percent,
            healthy_percent
        ) = self.calculate_percentages(
            health
        )

        score = self.calculate_overall_score(
            poor_percent,
            moderate_percent,
            healthy_percent
        )

        (
            status,
            recommendation
        ) = self.interpret_score(
            score
        )

        self.print_report(
            poor_percent,
            moderate_percent,
            healthy_percent,
            score,
            status,
            recommendation
        )

        self.save_report(
            poor_percent,
            moderate_percent,
            healthy_percent,
            score,
            status,
            recommendation
        )

        print(
            "\n=========================================="
        )

        print(
            "Health Score Module Completed Successfully."
        )

        print(
            "=========================================="
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    analyzer = HealthScoreAnalyzer()

    analyzer.run()