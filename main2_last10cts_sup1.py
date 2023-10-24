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

def main():
    print("Hello World")
    #test()
    x_list = []
    y_list = []
    for year in [2017,2021]:
        for county in ['debaoxian','zhuoluxian','shangyixian','songxian','sinanxian','tongjiangxian','lipingxian','mingshuixian','xijixian','congjiangxian']:
        # data = gpd.read_file(county+'/edges.shp')

            data= gpd.read_file('../data/tdrive_sample/results_GT_'+ county +'_'+str(year)+'/extracted_rn/edges.shp')
            data.crs = "EPSG:4326"
            data.to_crs("EPSG:32650",inplace=True)
            # print(data.crs)
            data['distance'] = data.geometry.length
            # print(data.head())

            distance_list = list(data['distance'])
            # print(max(distance_list))
            # print(min(distance_list))

            score = pd.Series(distance_list)
            se1 = pd.cut(score, [0,50,100,200,300,400,500,600,700,800,900,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,100000]) # 统计0-1,1-2依次类推各个区间的数值数量
            df = gpd.read_file('../data/tdrive_sample/results_GT_'+ county +'_'+str(year)+'/extracted_rn/nodes.shp')
            print(county, year,len(df))
            y_list.append(len(df))
            print(list(se1.value_counts()))
            # x_list.append(list(se1.value_counts()))
            x_list.append(list(se1.value_counts()))

    np.savetxt('../data/len_distri_last_GT.txt',x_list,fmt = '%d')
    np.savetxt('../data/len_distri_last_GT2.txt',y_list,fmt = '%d')

    for year in [2021]:
        for county in ['debaoxian','zhuoluxian','shangyixian','songxian','sinanxian','tongjiangxian','lipingxian','mingshuixian','xijixian','congjiangxian']:            
            mapcompare_d500('../temp_output_d500/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year)






if __name__=="__main__":
    main()