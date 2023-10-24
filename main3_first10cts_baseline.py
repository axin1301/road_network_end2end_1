import os
from test import *
from RoadNetwortLable_by_each_road import *
from concat_all_label_image import *
from GT_post_processing import *
from shp2txt_transform import *
import sys  
sys.path.append('topology_construction') 
from topology_construction.transform_graph_main import *

from mapcompare import *
from mapcompare_OSM import *
from mapcompare_baseline1_first import *
import glob
import PIL
from PIL import Image
import pandas as pd
import numpy as np
PIL.Image.MAX_IMAGE_PIXELS = None
import datetime

def main():
    print("Hello World")
    #test()
    df_all1 = pd.DataFrame({})
    df_all2 = pd.DataFrame({})
    df_all1.to_csv('validation_statistics_all_first10cts_baseline1.csv', index=False)
    df_all2.to_csv('validation_statistics_all_first10cts_baseline2.csv', index=False)

    # with open("time_log_first10cts_base.txt","w") as log_f:
    for county in ['shufuxian','xixiangxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
        for year in [2017,2021]: 
            mapcompare_baseline1('../temp_output_b1/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year, 'baseline1')
            mapcompare_baseline1('../temp_output_b2/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year, 'baseline2')

            df_all1 = pd.read_csv('validation_statistics_all_first10cts_baseline1.csv')
            df_all2 = pd.read_csv('validation_statistics_all_first10cts_baseline2.csv')

            df1 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline1.csv')
            df2 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline2.csv')

            df_all1 = pd.concat([df_all1, df1])
            df_all2 = pd.concat([df_all2, df2])

            df_all1.to_csv('validation_statistics_all_first10cts_baseline1.csv', index=False)
            df_all2.to_csv('validation_statistics_all_first10cts_baseline2.csv', index=False)


if __name__=="__main__":
    main()