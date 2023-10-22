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
    with open("time_log_first10cts_test_pipeline.txt","w") as log_f:
        for year in [2017]:#,2021
            for county in ['xixiangxian']:#,'shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                mapcompare('../temp_output/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year)
                # now_time = datetime.datetime.now()
                # log_f.write(county+'   ' +str(year) +'  '+'mapcompare'+ '  '+str(now_time))
                # log_f.write('\n')


        # year_list1 = []
        # county_list1 = []
        # positive_pixel_list = []
        # image_weight_list = []
        # image_height_list = []


        # for year in [2017,2021]:
        #     for county in ['shufuxian','xixiangxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
        #         img = Image.open('../temp_output/'+'topology_construction/'+county+'_GT_'+str(year)+'.png')
        #         img_np = np.array(img)
        #         pos_idx = np.where(img_np>0)
        #         year_list1.append(year)
        #         county_list1.append(county)
        #         positive_pixel_list.append(len(pos_idx[0]))
        #         image_weight_list.append(img_np.shape[0])
        #         image_height_list.append(img_np.shape[1])
        #         now_time = datetime.datetime.now()
        #         log_f.write(county +  '   ' +str(year) +'  '+'GT_statistics'+ '  '+str(now_time))
        #         log_f.write('\n')
        
        # pd_statis = pd.DataFrame({'county':county_list1, 'year':year_list1,'pos_pixel':positive_pixel_list, \
        #                           'img_weight':image_weight_list,'img_height':image_height_list})
        # pd_statis.to_csv('GT_statistics.csv', index=False)

        df_all = pd.DataFrame({})
        for year in [2017]:#,2021
            for county in ['xixiangxian']:#,'shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                df = pd.read_csv('../output/'+county+'_'+str(year)+'.csv')
                df_all = pd.concat([df_all, df])
                now_time = datetime.datetime.now()
                log_f.write(county +  '   ' +str(year) +'  '+'validation_statistics_all'+ '  '+str(now_time))
                log_f.write('\n')

        df_all.to_csv('validation_statistics_all_first10cts.csv', index=False)


    
    for year in [2018]:#,2022
        for county in ['xixiangxian']:#,'shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
            mapcompare_OSM('../temp_output_OSM/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year)
            # now_time = datetime.datetime.now()
            # log_f.write(county+'   ' +str(year) +'  '+'mapcompare'+ '  '+str(now_time))
            # log_f.write('\n')

    df_all = pd.DataFrame({})
    for year in [2018]: #2022
        for county in ['xixiangxian']:#,'shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
            df = pd.read_csv('../output/'+county+'_'+str(year)+'_OSM.csv')
            df_all = pd.concat([df_all, df])
            now_time = datetime.datetime.now()
            log_f.write(county +  '   ' +str(year) +'  '+'validation_statistics_all_OSM'+ '  '+str(now_time))
            log_f.write('\n')

    df_all.to_csv('validation_statistics_all_first10cts_OSM.csv', index=False)





if __name__=="__main__":
    main()