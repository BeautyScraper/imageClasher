import glob
import pandas as pd
import shutil
from pathlib import Path
import math
import random



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


def sort_heap_level(df, level, by='key_worth', ascending=True):
    """
    Sorts the given heap level in the dataframe by random or key_worth.

    Parameters:
    df (pd.DataFrame): The dataframe containing the heap.
    level (int): The heap level to sort.
    by (str): The mode to sort by - 'random' or a column name such as 'key_worth'.
    ascending (bool): Ascending order if True, descending if False.

    Returns:
    pd.DataFrame: A dataframe with the specified heap level sorted.
    """
    start_index = 2**level - 1
    end_index = 2**(level + 1) - 1
    level_df = df.iloc[start_index:end_index]

    if by == 'random':
        level_df = level_df.sample(frac=1).reset_index(drop=True)
    else:
        level_df = level_df.sort_values(by=by, ascending=ascending).reset_index(drop=True)
    
    df.iloc[start_index:end_index] = level_df
    return df

def move_level(level, out_dir, csv_file):
    # csv_file = csfv_file_path
    Path(out_dir).mkdir(parents=True, exist_ok=True)
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

def only_leave_intersection(df, tdir : str, filname_column : str):
    tdir = Path(tdir)
    filesincsv = {Path(x).name  for _,x in enumerate(df[filname_column][1:])}
    filesindir = {Path(x).name  for x in tdir.glob('*.jpg')}
    extra_in_dir = filesindir - filesincsv
    extra_file_dir : Path = tdir / 'extra'
    extra_file_dir.mkdir(parents=True,exist_ok=True)
    extra_row_in_csv : set[str] = filesincsv - filesindir
    for efile in extra_row_in_csv:
        filetocheck = str(tdir / efile)
        # breakpoint()
        df = df[df[filname_column] != filetocheck]
        df = df[df[filname_column] != efile]
    for efile in extra_in_dir:
        efilpath : Path = tdir / efile
        move_file(efilpath, extra_file_dir)
    return df

def main(out_dir):
    rt = 9
    csfv_file_path = str(Path(out_dir)/ 'clash_records.csv')
    df = pd.read_csv(csfv_file_path)
    df = only_leave_intersection(df,out_dir,'filepath')
    Path(csfv_file_path).unlink()
    df.to_csv(csfv_file_path,index=False)
    print(f'count {df.shape[0]=}')
    if math.floor(math.log(df.shape[0],2)) < rt:
        return
    print('segregating')
    nf = [rt-1,1,5]
    for i in range(rt):
        sort_heap_level(df, i)
    broader_move(nf, csfv_file_path, out_dir)
    for i in range(rt):
        sort_heap_level(df, i, 'random' )

    

if __name__ == '__main__':
    main(r'D:\paradise\stuff\essence\Pictures\Heaps\heap_SachMe')
    