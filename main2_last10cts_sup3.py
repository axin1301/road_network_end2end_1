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
from mapcompare_d500_last import *
import glob
import PIL
from PIL import Image
import pandas as pd
import numpy as np
PIL.Image.MAX_IMAGE_PIXELS = None
import datetime
import time

def main():
    print("Hello World")
    #test()

    df_all = pd.DataFrame({})
    for year in [2017,2021]:
        for county in ['debaoxian','zhuoluxian','shangyixian','songxian','sinanxian','tongjiangxian','lipingxian','mingshuixian','xijixian','congjiangxian']:
            if os.path.exists('../output/'+county+'_'+str(year)+'_d500.csv'):
                print(county, year)
                df = pd.read_csv('../output/'+county+'_'+str(year)+'_d500.csv')
                df_all = pd.concat([df_all, df])

    df_all.to_csv('validation_statistics_all_last_10cts_d500_part.csv', index=False)




if __name__=="__main__":
    main()