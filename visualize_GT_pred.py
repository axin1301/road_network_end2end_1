import geopandas as gpd
import matplotlib.pyplot as plt

for county in ['danfengxian']:#,'guanghexian','xixiangxian']:
    for year in [2017]:
        
        geo_df1 = gpd.read_file('../data/tdrive_sample/results_GT_'+county+'_'+str(year)+'/extracted_rn/edges.shp')
        geo_df2 = gpd.read_file('../data2/results_pred_'+county+'_'+str(year)+'/extracted_rn/edges.shp')
        ax1=geo_df1.plot(color='r')
        geo_df2.plot(ax=ax1,color='g')
        plt.savefig('../output/'+county+'_'+str(year)+'_visualization_GT_pred.png',dpi=300)
        plt.cla()

        fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)
        geo_df1.plot(ax=ax1, color='r')
        geo_df2.plot(ax=ax2, color='g')
        plt.savefig('../output/'+county+'_'+str(year)+'_visualization_GT_pred_subplot.png',dpi=300)
        # plt.show()
        plt.cla()