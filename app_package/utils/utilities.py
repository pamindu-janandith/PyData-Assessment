import os, pandas as pd, glob

def get_data_frame():
    path = r'..\data_sources'
    filenames = glob.glob(os.path.join(path + "/*.csv"))
    li = []

    for filename in filenames:
        df = pd.read_csv(filename, index_col=None, header=0)
        df['Country'] = filename.split('\\')[2].split('_')[0]
        li.append(df)

    
    frame = pd.concat(li, axis=0, ignore_index=True)

    return frame

