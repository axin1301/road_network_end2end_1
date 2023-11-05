import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from PIL import Image
import PIL
PIL.Image.MAX_IMAGE_PIXELS = None
from skimage import morphology,draw
import argparse
import os

def shp2txt_transform_roadtype(year, district):

    for roadclass in [49,41000,42000,43000,44000,45000,47000,51000,52000,53000,54000]:

        if not os.path.exists('../data/tdrive_sample_roadtype/results_GT_'+district+'_'+str(roadclass)+'_'+str(year)+'/extracted_rn/nodes.shp') or \
            not os.path.exists('../data/tdrive_sample_roadtype/results_GT_'+district+'_'+str(roadclass)+'_'+str(year)+'/extracted_rn/edges.shp'):
            continue

        if not os.path.exists('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/groundtruth/'):
            os.makedirs('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/groundtruth/')

        if not os.path.exists('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/algorithm/xyx/'):
            os.makedirs('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/algorithm/xyx/')

        df = gpd.read_file('../data/tdrive_sample_roadtype/results_GT_'+district+'_'+str(roadclass)+'_'+str(year)+'/extracted_rn/nodes.shp')
        # print(df.at[0,'geometry'])

        df2 = gpd.read_file('../data/tdrive_sample_roadtype/results_GT_'+district+'_'+str(roadclass)+'_'+str(year)+'/extracted_rn/edges.shp')
        # print(df2.head())

        # df = gpd.read_file('DeepMG-master/data/tdrive_sample/results_pred_'+district+'_'+str(year)+'/extracted_rn/nodes.shp')
        # # print(df.at[0,'geometry'])

        # df2 = gpd.read_file('DeepMG-master/data/tdrive_sample/results_pred_'+district+'_'+str(year)+'/extracted_rn/edges.shp')
        # # print(df2.head())

        lng_list = []
        lat_list = []
        cnt_list = []

        for i in range(len(df)):
            kk = df.at[i,'geometry']
            cnt_list.append(1+i)
            lng_list.append(kk.x)
            lat_list.append(kk.y)

        pd_dict = pd.DataFrame({'cnt':cnt_list, 'lng':lng_list, 'lat':lat_list})
        pd_dict.to_csv('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/groundtruth/'+district+'_'+str(year)+'_vertices_osm.txt',sep = ',', header = 0 , index = False)
        # pd_dict.to_csv('../temp_output/GraphSamplingToolkit-main/'+district+'_'+str(year)+'/algorithm/xyx/'+district+'_'+str(year)+'_vertices_osm.txt',sep = ',', header = 0 , index = False)



        p1_list = []
        p2_list = []
        cnt_list = []
        flg_list = []
        for i in range(len(df2)):
            
            line = df2.at[i,'geometry']

            first = Point(line.coords[0])
            last = Point(line.coords[-1])
            #print(first, last)
            
            first_x = first.x 
            first_y = first.y

            last_x = last.x
            last_y = last.y

            pd_tmp = pd_dict[(pd_dict['lng']==first_x) & (pd_dict['lat']==first_y)]
            p1_list.append(list(pd_tmp['cnt'])[0])

            pd_tmp = pd_dict[(pd_dict['lng']==last_x) & (pd_dict['lat']==last_y)]
            p2_list.append(list(pd_tmp['cnt'])[0])

            cnt_list.append(1+i)
            flg_list.append(1)

        pd_dict = pd.DataFrame({'cnt':cnt_list, 'p1':p1_list, 'p2':p2_list,'flg':flg_list})
        pd_dict.to_csv('../temp_output_roadtype/GraphSamplingToolkit-main/'+district+'_'+str(roadclass)+'_'+str(year)+'/groundtruth/'+district+'_'+str(year)+'_edges_osm.txt',sep = ',', header = 0 , index = False)
        # pd_dict.to_csv('../temp_output/GraphSamplingToolkit-main/'+district+'_'+str(year)+'/algorithm/xyx/'+district+'_'+str(year)+'_edges_osm.txt',sep = ',', header = 0 , index = False)
