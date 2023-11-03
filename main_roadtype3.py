import os
from test import *
import sys   
from RoadNetwortLable_by_each_road_roadtype import *
from concat_all_label_image_roadtype import *
from GT_post_processing_roadtype import *
from shp2txt_transform_roadtype import *
from mapcompare_roadtype import *
from mapcompare_roadtype_OSM import *
sys.path.append('topology_construction') 
from topology_construction.transform_graph_main_roadtype import *

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
    with open("time_log_roadtype2.txt","w") as log_f:
        for year in [2017,2021]:
            for county in ['honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
                now_time = datetime.datetime.now()
                log_f.write(county + '   ' +str(year) + '  ' +str(now_time))
                log_f.write('\n')
                print(county, '   ', year)
                RoadNetwortLable_by_each_road_roadtype(year,county)
                now_time = datetime.datetime.now()
                log_f.write(county +  '   ' +str(year) +'  '+'RoadNetwortLable_by_each_road'+ '  '+str(now_time))
                log_f.write('\n')
                concat_all_label_image_roadtype(year,county)
                now_time = datetime.datetime.now()
                log_f.write(county+ '   ' +str(year) +'  '+'concat_all_label_image'+ '  '+str(now_time))
                log_f.write('\n')
                GT_post_processing_roadtype(year,county)
                now_time = datetime.datetime.now()
                log_f.write(county+ '   ' +str(year) + '  '+'GT_post_processing'+ '  '+str(now_time))
                log_f.write('\n')
                transform_graph_main_roadtype(year,county)
                now_time = datetime.datetime.now()
                log_f.write(county+ '   ' +str(year) + '  '+'transform_graph_main'+ '  '+str(now_time))
                log_f.write('\n')
                shp2txt_transform_roadtype(year,county)
                now_time = datetime.datetime.now()
                log_f.write(county+'   ' +str(year) +'  '+'shp2txt_transform'+ '  '+str(now_time))
                log_f.write('\n')
                mapcompare_roadtype('../temp_output_d500/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year,'d500')
                now_time = datetime.datetime.now()
                log_f.write(county+'   ' +str(year) +'  '+'d500_mapcompare'+ '  '+str(now_time))
                log_f.write('\n')

                mapcompare_roadtype_OSM('../temp_output_OSM/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year+1,'OSM')
                now_time = datetime.datetime.now()
                log_f.write(county+'   ' +str(year) +'  '+'OSM_mapcompare'+ '  '+str(now_time))
                log_f.write('\n')

                mapcompare_roadtype('../temp_output_b1/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year,'b1')
                now_time = datetime.datetime.now()
                log_f.write(county+'   ' +str(year) +'  '+'b1_mapcompare'+ '  '+str(now_time))
                log_f.write('\n')

                mapcompare_roadtype('../temp_output_b2/GraphSamplingToolkit-main',county, 'xyx', 'LCR', year,'b2')
                now_time = datetime.datetime.now()
                log_f.write(county+'   ' +str(year) +'  '+'b2_mapcompare'+ '  '+str(now_time))
                log_f.write('\n')

                for roadclass in [49,41000,42000,43000,44000,45000,47000,51000,52000,53000,54000]:
                    if not os.path.exists('../temp_output_roadtype/'+county+'_road_label_by_image_'+str(roadclass)+'_'+str(year)):
                        continue
        
                    del_list = os.listdir('../temp_output_roadtype/'+county+'_road_label_by_image_'+str(roadclass)+'_'+str(year)+'/')
                    for f in del_list:
                        file_path = os.path.join('../temp_output_roadtype/'+county+'_road_label_by_image_'+str(roadclass)+'_'+str(year)+'/', f)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

                    if not os.path.exists('../temp_output_roadtype/'+county+'_width3_'+str(roadclass)+'_'+str(year)):
                        continue

                    del_list = os.listdir('../temp_output_roadtype/'+county+'_width3_'+str(roadclass)+'_'+str(year)+'/')
                    for f in del_list:
                        file_path = os.path.join('../temp_output_roadtype/'+county+'_width3_'+str(roadclass)+'_'+str(year)+'/', f)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

                    os.removedirs('../temp_output_roadtype/'+county+'_road_label_by_image_'+str(roadclass)+'_'+str(year))
                    os.removedirs('../temp_output_roadtype/'+county+'_width3_'+str(roadclass)+'_'+str(year))


if __name__=="__main__":
    main()