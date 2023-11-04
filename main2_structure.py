import pandas as pd
import glob
import os
import geopandas as gpd
import numpy as np
import networkx as nx
import random
from itertools import chain
import random


def gini(data):
    sorted_data = np.sort(data)  # 对数据进行排序
    n = len(data)
    index = np.arange(1, n + 1)  # 创建索引
    return ((np.sum((2 * index - n - 1) * sorted_data)) / (n * np.sum(sorted_data)))  # 计算基尼系数

district_list = ['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']

###############################################################################################################
a_list = []
b_list = []
c_list = []
y_list = []
d_list = []
edge_length_list = []
node_length_list=[]

alpha_list = []
beta_list = []
gamma_list = []

for county in district_list:
    for year in [2017,2021]:
        print(county,year)
        G = nx.read_gpickle('RN_graph/'+county+'_'+str(year)+'.gpickle')
         # 获取图的所有连通分量
        connected_components = list(nx.connected_components(G))

        # 存储每个连通分量的特征路径长度
        # 遍历每个连通分量并计算特征路径长度
        # for comp in connected_components:
        #     # 获取每个连通分量的子图
        #     subgraph = G.subgraph(comp)
        nodes_count = G.number_of_nodes()
        edges_count = G.number_of_edges()
        #     if nodes_count>3:
        alpha = (edges_count - nodes_count +1)/(2*nodes_count-5)
        beta = edges_count/nodes_count
        gamma = edges_count/(3*(nodes_count-2))
        alpha_list.append(alpha)
        beta_list.append(beta)
        gamma_list.append(gamma)

        # if alpha_list and beta_list and gamma_list:
        #     # 每个连通分量中心性指标的平均值
        #     avg_alpha = sum(alpha_list) / len(alpha_list)
        #     avg_beta = sum(beta_list) / len(beta_list)
        #     avg_gamma = sum(gamma_list) / len(gamma_list)
        
        edge_length_list.append(edges_count)
        node_length_list.append(nodes_count)
        # a_list.append(avg_alpha)
        # b_list.append(avg_beta)
        # c_list.append(avg_gamma)
        y_list.append(year)
        d_list.append(county)

pd_dict = pd.DataFrame({'county':d_list,'year':y_list,'alpha':alpha_list,'beta':beta_list,'gamma':gamma_list,'edge':edge_length_list,'node':node_length_list})
pd_dict.to_csv('a_b_g_graph_feature_GT_whole.csv', index=False)

##################################################################################################################################################

# 方法1：对采样节点计算平均最短路径长度
def sample_average_shortest_path(G, samples=100):
    if len(list(G.nodes()))<samples:
        samples = len(list(G.nodes()))
    sampled_nodes = random.sample(G.nodes(), samples)
    total_paths = 0
    total_length = 0
    for u in sampled_nodes:
        for v in sampled_nodes:
            if u != v:
                path_length = nx.shortest_path_length(G, u, v)
                total_paths += 1
                total_length += path_length
    return total_length / total_paths

# 方法2：使用 A* 算法估计平均最短路径长度
def astar_approx_avg_path_length(G):
    # 选择随机节点对
    nodes = list(G.nodes())
    u, v = random.choice(nodes), random.choice(nodes)
    return nx.astar_path_length(G, u, v)

a_list = []
y_list = []
d_list = []

for county in district_list:
    for year in [2017,2021]:
        print(county,year)
        G = nx.read_gpickle('RN_graph/'+county+'_'+str(year)+'.gpickle')

        # 获取图中的连通分量
        connected_components = list(nx.connected_components(G))

        # 存储每个连通分量的特征路径长度
        component_path_lengths = []

        # 遍历每个连通分量并计算特征路径长度
        for comp in connected_components:
            # 获取每个连通分量的子图
            print(connected_components.index(comp),'  ',len(connected_components))
            subgraph = G.subgraph(comp)

            # 计算每个连通分量的特征路径长度
            if len(comp) > 1:  # 仅对节点数大于1的连通分量计算路径长度
                # path_length = nx.average_shortest_path_length(subgraph, weight='weight',method='floyd-warshall')
                # astar_approx_path_length = astar_approx_avg_path_length(subgraph)
                
                approx_avg_path_length = sample_average_shortest_path(subgraph, samples=100)  ##原始版本50，这次增加到100
                component_path_lengths.append(approx_avg_path_length)
            # print(path_length)

        # 计算不连通的图的特征路径长度
        if component_path_lengths:
            avg_characteristic_path_length = sum(component_path_lengths) / len(component_path_lengths)
            print(f"不连通的带权重图的特征路径长度为: {avg_characteristic_path_length}")
        else:
            print("没有找到不连通的带权重图的特征路径长度。")
        
        a_list.append(avg_characteristic_path_length)
        y_list.append(year)
        d_list.append(county)

pd_dict = pd.DataFrame({'county':d_list,'year':y_list,'cpl':a_list})
pd_dict.to_csv('statis/cpl_graph_feature_GT_100.csv', index=False)

#####################################################################################################################################

def approximate_closeness_centrality(G, nodes, n_samples):
    closeness = {}
    for node in nodes:
        path_lengths = []
        for _ in range(n_samples):
            random_node = random.choice(nodes)
            if node != random_node:
                path_length = nx.shortest_path_length(G, source=node, target=random_node)
                path_lengths.append(path_length)
        closeness[node] = 0 if len(path_lengths) == 0 else 1 / sum(path_lengths)
    return closeness

def approximate_closeness_centrality(G, nodes_to_sample):
    closeness_centrality = {}
    for node in nodes_to_sample:
        # 使用随机采样估计节点的Closeness Centrality
        closeness = nx.closeness_centrality(G, u=node)
        closeness_centrality[node] = closeness
    return closeness_centrality

ave_deg_list = []
ave_bet_list = []
ave_clo_list = []
gini_deg_list = []
gini_bet_list = []
gini_clo_list = []
y_list = []
d_list = []

for county in district_list:
    for year in [2017, 2021]:
        # print(county,year)
        G = nx.read_gpickle('RN_graph/'+county+'_'+str(year)+'.gpickle')

        # 获取图中的连通分量
        connected_components = list(nx.connected_components(G))

        # 获取图的所有连通分量
        connected_components = list(nx.connected_components(G))

        # 存储每个连通分量的中心性指标
        component_degrees = []
        component_betweenness = []
        component_closeness = []

        # 遍历每个连通分量并计算中心性指标
        for comp in connected_components:
            # 获取每个连通分量的子图
            print(county,year, connected_components.index(comp),'  ',len(connected_components))
            subgraph = G.subgraph(comp)

            # 计算每个连通分量的中心性指标
            if len(comp) > 1:  # 仅对节点数大于1的连通分量计算中心性指标
                # Degree centrality
                degree = nx.degree_centrality(subgraph)
                component_degrees.append(degree)
                print('degree')

                # Betweenness centrality
                nodes_count = subgraph.number_of_nodes()
                sample_node_count = min(nodes_count, 100)#####最开始都是50，增加到100
                betweenness = nx.betweenness_centrality(subgraph, weight='weight', k=sample_node_count, normalized=True, endpoints=False)
                component_betweenness.append(betweenness)
                print('betweenness')

                # # Closeness centrality
                nodes = list(subgraph.nodes())
                # # 近似计算
                n_samples = min(nodes_count, 100)  # 可根据需求调整采样次数  #####最开始都是50，增加到100
                # approx_closeness = approximate_closeness_centrality(subgraph, nodes, n_samples)
                # # closeness = nx.closeness_centrality(subgraph, distance='weight', wf_improved=False)
                nodes_to_sample = random.sample(G.nodes(), n_samples)  # 采样10%的节点
                approx_closeness = approximate_closeness_centrality(G, nodes_to_sample)
                print('closeness')
                component_closeness.append(approx_closeness)

        # 计算不连通的图的中心性指标
        # print(list(chain.from_iterable([list(betweenness_dict.values()) for betweenness_dict in component_betweenness])))
        if component_degrees and component_betweenness and component_closeness:
            # 每个连通分量中心性指标的平均值
            avg_betweenness = np.average(np.array(list(chain.from_iterable([list(betweenness_dict.values()) for betweenness_dict in component_betweenness]))))
            avg_degree = np.average(np.array(list(chain.from_iterable([list(degree_dict.values()) for degree_dict in component_degrees]))))
            # avg_betweenness = {k: sum(b[k] for b in component_betweenness) / len(component_betweenness) for k in component_betweenness[0]}
            avg_closeness = np.average(np.array(list(chain.from_iterable([list(closeness_dict.values()) for closeness_dict in component_closeness]))))

            gini_degree = gini(np.array(list(chain.from_iterable([list(degree_dict.values()) for degree_dict in component_degrees]))))
            gini_betweenness = gini(np.array(list(chain.from_iterable([list(betweenness_dict.values()) for betweenness_dict in component_betweenness]))))
            gini_clossness = gini(np.array(list(chain.from_iterable([list(closeness_dict.values()) for closeness_dict in component_closeness]))))

            print(f"不连通的带权重图的平均度中心性为: {avg_degree}")
            print(f"不连通的带权重图的平均介数中心性为: {avg_betweenness}")
            print(f"不连通的带权重图的平均接近度中心性为: {avg_closeness}")
        else:
            print("没有找到不连通的带权重图的中心性指标。")
        
        ave_deg_list.append(avg_degree)
        ave_bet_list.append(avg_betweenness)
        ave_clo_list.append(avg_closeness)
        gini_deg_list.append(gini_degree)
        gini_bet_list.append(gini_betweenness)
        gini_clo_list.append(gini_clossness)
        y_list.append(year)
        d_list.append(county)

pd_dict = pd.DataFrame({'county':d_list,'year':y_list,'ave_deg':ave_deg_list,'ave_bet':ave_bet_list,'ave_clo':ave_clo_list,'gini_deg':gini_deg_list,'gini_bet':gini_bet_list,'gini_clo':gini_clo_list})
pd_dict.to_csv('statis/deg_bet_clo_graph_feature_GT_100.csv', index=False)
#############################################################################################

