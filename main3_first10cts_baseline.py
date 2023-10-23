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
    with open("time_log_first10cts_base.txt","w") as log_f:
        for year in [2017,2021]:
            for county in ['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                mapcompare_baseline1('../temp_output_b1/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year, 'baseline1')



        df_all = pd.DataFrame({})
        for year in [2017,2021]:
            for county in ['shufuxian','xixiangxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                df = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline1.csv')
                df_all = pd.concat([df_all, df])
                # now_time = datetime.datetime.now()
                # log_f.write(county +  '   ' +str(year) +'  '+'validation_statistics_all'+ '  '+str(now_time))
                # log_f.write('\n')

        df_all.to_csv('validation_statistics_all_first10cts_baseline1.csv', index=False)


        for year in [2017,2021]:
            for county in ['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                mapcompare_baseline1('../temp_output_b2/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year, 'baseline2')



        df_all = pd.DataFrame({})
        for year in [2017,2021]:
            for county in ['shufuxian','xixiangxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                df = pd.read_csv('../output/'+county+'_'+str(year)+'_baseline2.csv')
                df_all = pd.concat([df_all, df])
                # now_time = datetime.datetime.now()
                # log_f.write(county +  '   ' +str(year) +'  '+'validation_statistics_all'+ '  '+str(now_time))
                # log_f.write('\n')

        df_all.to_csv('validation_statistics_all_first10cts_baseline2.csv', index=False)


 

if __name__=="__main__":
    main()