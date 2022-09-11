#####################################################################
# Did not use this file and the data was downloaded manually
#####################################################################
from tqdm import tqdm
import requests

files = [("energydata_complete.csv", "."), ("energydata_complete.csv", "./evidently_service/datasets")]

print(f"Download files:")
for file, path in files:
    url = f"github.com"
    resp = requests.get(url, stream=True)
    save_path = f"{path}/{file}"
    with open(save_path, "wb") as handle:
        for data in tqdm(resp.iter_content(),
                         desc=f"{file}",
                         postfix=f"save to {save_path}",
                         total=int(resp.headers["Content-Length"])):
            handle.write(data)
