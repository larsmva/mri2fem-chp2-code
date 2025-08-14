
import logging
from pathlib import Path

import tarfile
import requests
from tqdm import tqdm


here = Path(__file__).absolute().parent
logger = logging.getLogger(__name__)

def download(path, link, desc=None, params=None):
    if desc is None:
        desc = f"Download data to {path}"
    if params is None:
        params = {}

    response = requests.get(link, params, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True, desc=desc)

    with open(path, "wb") as handle:
        for data in response.iter_content(chunk_size=1000 * 1024):
            progress_bar.update(len(data))
            handle.write(data)
    progress_bar.close()

    folder = path.resolve().parent
    logger.info(f"Extracting {path} to {folder}")
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(folder,filter='data')
    path.unlink()


def download_mri2femii_chp2_dataset(output: Path = Path("mri2femii-chp2-dataset.tar.gz")) -> None:
    link = "https://zenodo.org/records/14536218/files/mri2femii-chp2-dataset.tar.gz?download=1"
    logger.info(f"Downloading MRI2FEMII chapter 2 dataset to {output}")
    download(output, link)


def main(output):
    download_mri2femii_chp2_dataset(Path(f"{output}/mri2femii-chp2-dataset.tar.gz"))


def add_arguments(parser):
    
   from pathlib import Path
   parser.add_argument(
      "-o",
      "--output", 
      help="Output directory of the downloaded dataset.")
   

   


if __name__ == '__main__':

    import argparse
    import time 

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', 
                        '--output'    ,type=str, help="Output directory of the downloaded dataset.")

    start_time = time.time()        
    Z = parser.parse_args()    
    
    download_mri2femii_chp2_dataset( Path(f"{Z.output}/mri2femii-chp2-dataset.tar.gz"))
    
