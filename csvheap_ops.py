import pandas as pd
import shutil
from pathlib import Path
import math

out_dir = r'D:\paradise\stuff\essence\Pictures\heap\heap_dir'
csfv_file_path = r'D:\paradise\stuff\essence\Pictures\heap\clash_records.csv'

def csv_to_dir():
    df = pd.read_csv(csfv_file_path)
    for i,file_path in enumerate(df['filepath'][1:]):
        file_name = Path(file_path).name
        level = math.floor(math.log(i+2,2))
        level = str(level)
        out_dir_level = Path(out_dir) / level / file_name
        out_dir_level.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file_path, out_dir_level)

if __name__ == '__main__':
    csv_to_dir()
    