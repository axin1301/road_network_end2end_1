import networkx as nx
import pickle
import geopandas as gpd
from shapely.geometry import Point

def construct_node_shp():
    dir_ori = '../../RoadNetwork_Validation_final/data/tdrive_sample/'
    for year in [2017,2021]:
        for county in ['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
            nodes_shp_path = dir_ori + 'results_GT_'+county+'_'+str(year)+'/'+'extracted_rn/nodes.shp'  # 替换成你的节点 Shapefile 文件路径
            edges_shp_path = dir_ori + 'results_GT_'+county+'_'+str(year)+'/'+'extracted_rn/edges.shp'  # 替换成你的边 Shapefile 文件路径

            nodes_gdf = gpd.read_file(nodes_shp_path)  # 替换成你的节点 Shapefile 文件路径
            edges_gdf = gpd.read_file(edges_shp_path)  # 替换成你的边 Shapefile 文件路径
            # edges_gdf.reset_index(drop=True)
            edges_gdf.crs = 'epsg:4326'  # Set the CRS to EPSG 4326
            nodes_gdf.crs = 'epsg:4326'
            # print(nodes_gdf.head())
            # print(edges_gdf.head())

            # 创建空的 NetworkX 图形
            G = nx.Graph()

            # Add nodes to the graph
            for index, row in nodes_gdf.iterrows():
                # print(row['geometry'].coords[0][0],row['geometry'].coords[0][1])
                G.add_node(row['FID'],longitude = row['geometry'].coords[0][0], latitude = row['geometry'].coords[0][1])

            # Build a spatial index for nodes
            nodes_sindex = nodes_gdf.sindex

            # Build a spatial index for edges
            edges_sindex = edges_gdf.sindex

            # Add edges to the graph
            for index, row in edges_gdf.iterrows():
                edge_id = row['eid']
                edge_geometry = row['geometry']
                start_node = edge_geometry.coords[0]
                end_node = edge_geometry.coords[-1]
                # Calculate edge length as weight
                # edge_length = row['length_m']

                # Find potential nodes near the start and end points of the edge
                possible_start_matches = list(nodes_sindex.intersection(start_node))
                possible_end_matches = list(nodes_sindex.intersection(end_node))

                # Check if the edge geometry intersects or is contained by any node geometry
                for match_index in possible_start_matches:
                    node_geometry = nodes_gdf.loc[match_index, 'geometry']
                    if edge_geometry.intersects(node_geometry) or edge_geometry.touches(node_geometry):
                        start_id = nodes_gdf.loc[match_index, 'FID']
                        break

                for match_index in possible_end_matches:
                    node_geometry = nodes_gdf.loc[match_index, 'geometry']
                    if edge_geometry.intersects(node_geometry) or edge_geometry.touches(node_geometry):
                        end_id = nodes_gdf.loc[match_index, 'FID']
                        break

                if start_id is not None and end_id is not None:
                    G.add_edge(start_id, end_id)# , weight=edge_length

            # Get the number of nodes and edges in the graph
            nodes_count = G.number_of_nodes()
            edges_count = G.number_of_edges()

            print(f"Number of nodes: {nodes_count}")
            print(f"Number of edges: {edges_count}")

            # nx.write_gpickle(G, 'cjx_OSM.gpickle')

            # 找出度大于2的节点
            nodes_degree_gt_2 = [node for node, degree in dict(G.degree()).items() if degree >= 2]

            # 提取这些节点的地理信息
            node_data = []
            for node in nodes_degree_gt_2:
                node_attributes = G.nodes[node]
                # 假设节点属性中有'longitude'和'latitude'作为经纬度信息
                if 'longitude' in node_attributes and 'latitude' in node_attributes:
                    lon = node_attributes['longitude']
                    lat = node_attributes['latitude']
                    node_data.append({'geometry': Point(lon, lat)})  # Point是shapely.geometry中的类

            # 创建 GeoDataFrame
            print(len(node_data))
            if node_data:
                gdf = gpd.GeoDataFrame(node_data, crs="EPSG:4326")  # 设置地理坐标系
                # 如果需要将GeoDataFrame保存为Shapefile
                gdf.to_file('GT/'+county+'_'+str(year)+'_nodes_degree_gt_2.shp')


            # 找出度大于2的节点
            nodes_degree_gt_3 = [node for node, degree in dict(G.degree()).items() if degree >= 3]

            # 提取这些节点的地理信息
            node_data = []
            for node in nodes_degree_gt_3:
                node_attributes = G.nodes[node]
                # 假设节点属性中有'longitude'和'latitude'作为经纬度信息
                if 'longitude' in node_attributes and 'latitude' in node_attributes:
                    lon = node_attributes['longitude']
                    lat = node_attributes['latitude']
                    node_data.append({'geometry': Point(lon, lat)})  # Point是shapely.geometry中的类

            # 创建 GeoDataFrame
            print(len(node_data))
            if node_data:
                gdf = gpd.GeoDataFrame(node_data, crs="EPSG:4326")  # 设置地理坐标系
                # 如果需要将GeoDataFrame保存为Shapefile
                gdf.to_file('GT/'+county+'_'+str(year)+'_nodes_degree_gt_3.shp')