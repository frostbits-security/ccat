import networkx as nx
import matplotlib.pyplot as plt

def draw_plot(switches_dict, vlanmap=False):

    # Fill list Sets in the next format: [(vlan_num, 'dev_name_int'),(...)]
    sets = []
    for switch in switches_dict:
        result_dict = {}
        for iface in switches_dict[switch]:
            if len(switches_dict[switch][iface]) > 0:
                result_dict.update({iface: switches_dict[switch][iface]})
        for iface_vlans in result_dict:
            for vlan in result_dict[iface_vlans]:
                sets.append((vlan, switch + ' ' + iface_vlans))

    # Fill 2 nodes lists to color them in different colors on graph
    central_nodes_list = []
    edge_nodes_list = []
    for node_pair in sets:
        found = False
        if node_pair[0] in central_nodes_list:
            continue
        for next_node_pair in sets:
            if node_pair == next_node_pair:
                continue
            if node_pair[0] == next_node_pair[0]:
                central_nodes_list.append(node_pair[0])
                found = True
                break
        if found is False:
            edge_nodes_list.append(node_pair[0])

    # Debug output
    print('..............CENTRAL NODES LIST.............')
    print(central_nodes_list)
    print('..............EDGE NODES LIST.............')
    print(edge_nodes_list)
    print('--------------IN CASE IF WE HAVE SAME VLANS IN 2 LISTS THE LIST BELOW WONT BE EMPTY--------------')
    print([i for i in central_nodes_list if i in edge_nodes_list])

    # # For PDF format, otherwise internal error will occur
    # plt.rcParams['pdf.fonttype'] = 42
    # plt.rcParams['font.family'] = 'Calibri'

    # draw graph
    G = nx.Graph()
    G.add_edges_from(sets)
    pos = nx.spring_layout(G)

    # Increase plot size
    plt.figure(figsize=(16,9))

    # Draw nodes
    legend_edge_node = nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes_list,    node_color="#ff4d4d", with_labels=False)
    legend_cent_node = nx.draw_networkx_nodes(G, pos, nodelist=central_nodes_list, node_color="#4d4dff", with_labels=False)

    # Draw edges (connections)
    legend_conn_int  = nx.draw_networkx_edges(G, pos, edge_color='black', font_size=16, with_labels=False)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Delete X and Y symbols and values on graph
    plt.xticks([])
    plt.yticks([])

    # Plot's legend
    plt.legend((legend_edge_node, legend_cent_node, legend_conn_int), ('Single vlans', 'Multiple vlans', 'Connected interface'), loc=1, framealpha=0.5, fontsize='small', markerscale=0.5,edgecolor='Black')

    # Delete space between plot and window edge
    plt.tight_layout()

    # Save graph as png picture
    plt.savefig("network_map.png", dpi=1000)

    # Interactive mode
    plt.show()
