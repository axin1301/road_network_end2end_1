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
from mapcompare_baseline1_last import *
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
    
    # var1 = int(os.path.exists('../temp_output/GraphSamplingToolkit-main/lipingxian_2021/groundtruth/lipingxian_2021_edges_osm.txt'))
    # var2 = int(os.path.exists('../temp_output/GraphSamplingToolkit-main/congjiangxian_2021/groundtruth/congjiangxian_2021_edges_osm.txt'))
    # while (var1+var2)!=2:
    #     time.sleep(2000)
    #     var1 = int(os.path.exists('../temp_output/GraphSamplingToolkit-main/lipingxian_2021/groundtruth/lipingxian_2021_edges_osm.txt'))
    #     var2 = int(os.path.exists('../temp_output/GraphSamplingToolkit-main/congjiangxian_2021/groundtruth/congjiangxian_2021_edges_osm.txt'))

    #     if (var1+var2)==2:
    #         break
    
    df_all1 = pd.DataFrame({})
    df_all2 = pd.DataFrame({})

    year = 2017 
    county = 'debaoxian'

    df1 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline1.csv')
    df2 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline2.csv')

    df_all1 = pd.concat([df_all1, df1])
    df_all2 = pd.concat([df_all2, df2])

    df_all1.to_csv('validation_statistics_all_last10cts_baseline1.csv', index=False)
    df_all2.to_csv('validation_statistics_all_last10cts_baseline2.csv', index=False)

    for county in ['debaoxian','zhuoluxian','shangyixian','songxian','sinanxian','tongjiangxian','lipingxian','mingshuixian','xijixian','congjiangxian']:
        for year in [2017,2021]:
            if year == 2017 and county == 'debaoxian':
                continue

            print('working correctly')

            mapcompare_baseline1('../temp_output_b1/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year,'baseline1')
            mapcompare_baseline1('../temp_output_b2/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year,'baseline2')

            df_all1 = pd.read_csv('validation_statistics_all_last10cts_baseline1.csv')
            df_all2 = pd.read_csv('validation_statistics_all_last10cts_baseline2.csv')

            df1 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline1.csv')
            df2 = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline2.csv')

            df_all1 = pd.concat([df_all1, df1])
            df_all2 = pd.concat([df_all2, df2])

            df_all1.to_csv('validation_statistics_all_last10cts_baseline1.csv', index=False)
            df_all2.to_csv('validation_statistics_all_last10cts_baseline2.csv', index=False)

            print('working correctly2')




if __name__=="__main__":
    main()