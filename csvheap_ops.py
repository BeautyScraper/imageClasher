import pandas as pd
import shutil
from pathlib import Path
import math



def csv_to_dir(csfv_file_path,out_dir):
    df = pd.read_csv(csfv_file_path)
    for i,file_path in enumerate(df['filepath'][1:]):
        file_name = Path(file_path).name
        level = math.floor(math.log(i+2,2))
        level = str(level)
        out_dir_level = Path(out_dir) / level / file_name
        out_dir_level.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file_path, out_dir_level)
        
def dir_to_csv(csfv_file_path,out_dir):
    df = pd.read_csv(csfv_file_path)
    lev_dirs = [x for x in Path(out_dir).iterdir() if x.is_dir()] 
    lev_dirs_name = [x.name for x in Path(out_dir).iterdir() if x.is_dir()] 
    for i,dirs in enumerate(lev_dirs):
        if str(i) in lev_dirs_name:
            continue
        shifted_name = min([x for x in lev_dirs if int(x.name) in range(i+1,max([int(x) for x in lev_dirs_name]))])
        shifted_name = str(shifted_name)
        dirs.rename(shifted_name)

def broader_move(level_dir_mapping, csv_file, out_dir_p):
    ld = Path(out_dir_p)
    for level in level_dir_mapping:
            
        move_level(level,str(ld/str(level)),csv_file) 

def move_file(filePath,out_dir):
    outfile = Path(out_dir) / Path(filePath).name
    if outfile.is_file():
        outfile.unlink()
    if Path(filePath).is_file():
        shutil.move(filePath,out_dir)



def move_level(level, out_dir, csv_file):
    # csv_file = csfv_file_path
    df = pd.read_csv(csv_file)
    start_index = 2**level - 1
    end_index = 2**(level+1) - 1
    nf = lambda x:move_file(x, out_dir)
    df.iloc[start_index:end_index,1].apply(nf)
    # breakpoint()
    # df.drop(df.iloc[start_index:end_index,:])
    df = df.drop(labels=range(start_index,end_index+1), axis=0)
    Path(csv_file).unlink()
    df.to_csv(csv_file,index=False)

def main(out_dir):
    
    csfv_file_path = str(Path(out_dir)/ 'clash_records.csv')
    df = pd.read_csv(csfv_file_path)
    if math.floor(math.log(df.shape[0],2)) < 11:
        return
    
    nf = [10,1,6]
    broader_move(nf, csfv_file_path, out_dir)

if __name__ == '__main__':
    main()
    