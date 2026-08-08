"""
vegetation.py

Purpose:
---------
Classify vegetation using NDVI.

Classes
-------
0 : Water
1 : Bare Soil
2 : Sparse Vegetation
3 : Moderate Vegetation
4 : Dense Vegetation

Author : Gopika Hajra
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class VegetationClassifier:

    def __init__(self):

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.output_folder = os.path.join(
            self.project_root,
            "output"
        )

        os.makedirs(self.output_folder, exist_ok=True)

        self.ndvi_file = os.path.join(
            self.output_folder,
            "ndvi.npy"
        )

    # --------------------------------------------------

    def load_ndvi(self):

        if not os.path.exists(self.ndvi_file):
            raise FileNotFoundError(
                "ndvi.npy not found.\nRun ndvi.py first."
            )

        print("Loading NDVI...\n")

        return np.load(self.ndvi_file)

    # --------------------------------------------------

    def classify(self, ndvi):

        # -1 means NoData
        vegetation = np.full(
            ndvi.shape,
            -1,
            dtype=np.int8
        )

        valid = ~np.isnan(ndvi)

        vegetation[valid & (ndvi < 0)] = 0

        vegetation[
            valid &
            (ndvi >= 0) &
            (ndvi < 0.2)
        ] = 1

        vegetation[
            valid &
            (ndvi >= 0.2) &
            (ndvi < 0.5)
        ] = 2

        vegetation[
            valid &
            (ndvi >= 0.5) &
            (ndvi < 0.7)
        ] = 3

        vegetation[
            valid &
            (ndvi >= 0.7)
        ] = 4

        return vegetation

    # --------------------------------------------------

    def statistics(self, vegetation):

        labels = {
            0: "Water",
            1: "Bare Soil",
            2: "Sparse Vegetation",
            3: "Moderate Vegetation",
            4: "Dense Vegetation"
        }

        valid_pixels = vegetation[vegetation != -1]

        total = len(valid_pixels)

        print("======================================")
        print("VEGETATION STATISTICS")
        print("======================================")

        for cls, name in labels.items():

            pixels = np.sum(valid_pixels == cls)

            percent = pixels * 100 / total

            print(f"{name:<22}: {percent:.2f}%")

        print("======================================\n")

    # --------------------------------------------------

    def save_array(self, vegetation):

        path = os.path.join(
            self.output_folder,
            "vegetation.npy"
        )

        np.save(path, vegetation)

        print("Vegetation array saved")

    # --------------------------------------------------

    def save_image(self, vegetation):

        masked = np.ma.masked_where(
            vegetation == -1,
            vegetation
        )

        colors = [
            "#1f78b4",   # Water
            "#b5651d",   # Soil
            "#ffff66",   # Sparse
            "#66bd63",   # Moderate
            "#006400"    # Dense
        ]

        cmap = ListedColormap(colors)

        cmap.set_bad("white")

        plt.figure(figsize=(10,10))

        img = plt.imshow(
            masked,
            cmap=cmap,
            interpolation="nearest"
        )

        cbar = plt.colorbar(
            img,
            ticks=[0,1,2,3,4]
        )

        cbar.ax.set_yticklabels([
            "Water",
            "Bare Soil",
            "Sparse",
            "Moderate",
            "Dense"
        ])

        plt.title(
            "Vegetation Classification"
        )

        plt.axis("off")

        save_path = os.path.join(
            self.output_folder,
            "vegetation_map.png"
        )

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight",
            format="png"
        )

        plt.close()

        print("Vegetation map saved")
        print(save_path)

    # --------------------------------------------------

    def run(self):

        ndvi = self.load_ndvi()

        vegetation = self.classify(ndvi)

        self.statistics(vegetation)

        self.save_array(vegetation)

        self.save_image(vegetation)

        print("\nVegetation Classification Completed Successfully.")


# --------------------------------------------------

if __name__ == "__main__":

    classifier = VegetationClassifier()

    classifier.run()