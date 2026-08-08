"""
download.py

Purpose:
- Check if Sentinel-2 band files exist.
- Read metadata from each band.
- Return file paths for preprocessing.


"""

import os
import rasterio


class SatelliteDownloader:

    def __init__(self):

        # Get project root folder
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Data folder
        self.data_folder = os.path.join(self.base_dir, "data")

        # Sentinel-2 bands
        self.band_files = {
            "B2": os.path.join(self.data_folder, "B2.tif"),
            "B3": os.path.join(self.data_folder, "B3.tif"),
            "B4": os.path.join(self.data_folder, "B4.tif"),
            "B8": os.path.join(self.data_folder, "B8.tif")
        }

    def load_images(self):
        """
        Verify that all required Sentinel-2 bands exist.
        """

        print("Checking Sentinel-2 band files...\n")

        for band, path in self.band_files.items():

            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"{band}.tif not found!\nExpected location:\n{path}"
                )

            print(f"✅ {band}.tif found")

        print("\nAll required Sentinel-2 bands are available.\n")

        return self.band_files

    def image_info(self):
        """
        Display metadata for each band.
        """

        print("=" * 60)

        for band, path in self.band_files.items():

            with rasterio.open(path) as src:

                print(f"\n{band} INFORMATION")
                print("-" * 30)
                print("Filename   :", os.path.basename(path))
                print("Width      :", src.width)
                print("Height     :", src.height)
                print("Bands      :", src.count)
                print("CRS        :", src.crs)
                print("Resolution :", src.res)
                print("Bounds     :", src.bounds)

        print("\n" + "=" * 60)

    def get_band_paths(self):
        """
        Returns dictionary containing paths of all bands.
        """
        return self.band_files


if __name__ == "__main__":

    downloader = SatelliteDownloader()

    downloader.load_images()

    downloader.image_info()