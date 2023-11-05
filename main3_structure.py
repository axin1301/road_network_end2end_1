import pandas as pd
import glob
import os
import geopandas as gpd
import numpy as np
import networkx as nx
import random
from itertools import chain
import random


RL_list2017 = []
RL_list2021 = []

district_list = ['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']

###############################################################################################################
for district in district_list:
    # print(county,year)
    year = 2017
    edges_shp_path = '../../RoadNetwork_Validation_final/data/tdrive_sample/results_GT_'+district+'_'+str(year)+'/extracted_rn/edges.shp'  # 替换成你的边 Shapefile 文件路径
    data = gpd.read_file(edges_shp_path)
    data.crs = "EPSG:4326"
    data.to_crs("EPSG:3857",inplace=True)
    # print(data.crs)
    data['distance'] = data.geometry.length
    # print(data.head())
    distance_list = list(data['distance'])
    RL_list2017.append(np.sum(distance_list)/1000.0)

    year = 2021
    edges_shp_path = '../../RoadNetwork_Validation_final/data/tdrive_sample/results_GT_'+district+'_'+str(year)+'/extracted_rn/edges.shp'  # 替换成你的边 Shapefile 文件路径
    data = gpd.read_file(edges_shp_path)
    data.crs = "EPSG:4326"
    data.to_crs("EPSG:3857",inplace=True)
    # print(data.crs)
    data['distance'] = data.geometry.length
    # print(data.head())
    distance_list = list(data['distance'])
    RL_list2021.append(np.sum(distance_list)/1000.0)
    print('running')

pd_dict = pd.DataFrame({'county':district_list,'rn2017':RL_list2017,'rn2021':RL_list2021})
pd_dict.to_csv('rn_panel_GT.csv', index=False)


