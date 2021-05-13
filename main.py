import os
import time
import shutil
import urllib.request
from datetime import datetime
from kaggle import KaggleApi as kag_api

__version__ = "1.0.0"
DATASET_NAME = "covid-vaccination-dataset"
DATA_FOLDER = "dataset"
URLS = {
    "vaccinations.csv": "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
    "us_state_vaccinations.csv": "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv"
}


def clear_dir(folder):
    for filename in os.listdir(folder):
        if filename == 'dataset-metadata.json':
            pass
        else:
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"[INFO] File removed: {filename}")
            except Exception as e:
                print('[ERROR] Failed to delete %s. Reason: %s' % (file_path, e))


def get_vaccine_data(urls):
    for key, value in urls.items():
        urllib.request.urlretrieve(value, f"{DATA_FOLDER}\\{key}")


if __name__ == '__main__':
    get_vaccine_data(URLS)
    api = kag_api()
    kag_api.authenticate(api)
    print("[INFO] Kaggle credentials authenticated.")
    response = kag_api.dataset_create_version(api, DATA_FOLDER, f"Dataset updated till (UTC): {datetime.utcnow()}",
                                              convert_to_csv=True, delete_old_versions=False)
    if response.status == "ok":
        print(f"[{datetime.now()}][INFO] Kaggle Dataset uploaded.")
    else:
        print(f"[{datetime.now()}][ERROR] {response.error}")
    clear_dir(DATA_FOLDER)
    time.sleep(5)
