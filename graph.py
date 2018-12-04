import networkx as nx
import matplotlib.pyplot as plt
import re
import os


def get_legend(legend_full_item_list, legend_full_value_list):
    legend_item_list = []
    legend_value_list = []
    for legend_item in legend_full_item_list:
        if legend_item is not None:
            legend_item_list.append(legend_item)
            legend_value_list.append(legend_full_value_list[legend_full_item_list.index(legend_item)])
    return legend_item_list, legend_value_list


def draw_plot(switches_dict, graph_path, vlanmap=False):

    # Fill list Sets in the next format: [(vlan_num, 'dev_name_int'),(...)]
    sets = []
    for switch in switches_dict:
        result_dict = {}
        for iface in switches_dict[switch]:
            if len(switches_dict[switch][iface]) > 0:
                # Make short name of interface
                iface_short = re.sub('[a-z]', '', iface)
                result_dict.update({iface_short: switches_dict[switch][iface]})

        for iface_vlans in result_dict:
            for vlan in result_dict[iface_vlans]:
                # Make short name of switch
                switch_short = os.path.splitext(switch)[0]
                sets.append((vlan, switch_short + ' ' + iface_vlans))

    # Fill 2 lists with central and edges nodes
    central_nodes_list = []
    edge_nodes_list    = []
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

    # For PDF format, otherwise internal error will occur (future feature)
    # plt.rcParams['pdf.fonttype'] = 42
    # plt.rcParams['font.family'] = 'Calibri'

    # draw graph
    G = nx.Graph()
    G.add_edges_from(sets)

    # Remove excess connections (all interfaces to all vlans)
    remove_list = []
    for node_pair in sets:
        found = False
        for next_node_pair in sets:
            if node_pair == next_node_pair:
                continue
            if node_pair[1] == next_node_pair[1]:
                found = True
                break
        if found == False:
            remove_list.append(node_pair[1])
    G.remove_nodes_from(remove_list)

    # get items position, where K is the optimal distance between nodes
    pos = nx.spring_layout(G, k=0.2)

    # Define plot size
    plt.figure(figsize=(16,9))

    if not vlanmap:
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=0, node_color='white')
        legend_edge_node = nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes_list,    node_shape='*',  node_color="#ffff80")
        legend_cent_node = nx.draw_networkx_nodes(G, pos, nodelist=central_nodes_list, node_shape='o',  node_color="#ff80ff")

        # Draw edges (connections)
        legend_conn_int  = nx.draw_networkx_edges(G, pos, edge_color='black', style='dotted')

        # Building legend without errors
        legend_full_item_list  = [legend_edge_node, legend_cent_node, legend_conn_int]
        legend_full_value_list = ['Single vlans', 'Multiple vlans', 'Connected interface']

        legend_item_list, legend_value_list = get_legend(legend_full_item_list,legend_full_value_list)

        plt.legend(legend_item_list,
                   legend_value_list,
                   loc=1, framealpha=0.5, fontsize='small', markerscale=0.5, edgecolor='Black')

    else:
        # Get nodes lists
        dmz_central        = list(set(vlanmap[0]) & set(central_nodes_list))
        dmz_edge           = list(set(vlanmap[0]) & set(edge_nodes_list))
        management_central = list(set(vlanmap[2]) & set(central_nodes_list))
        management_edge    = list(set(vlanmap[2]) & set(edge_nodes_list))

        others_central = list(set(central_nodes_list) - set(management_central) - set(dmz_central))
        others_edge    = list(set(edge_nodes_list)    - set(management_edge)    - set(dmz_edge))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=0, node_color='white')
        legend_dmz_central        = nx.draw_networkx_nodes(G, pos, nodelist=dmz_central,        node_shape='o', node_color="#ff8080")
        legend_dmz_edge           = nx.draw_networkx_nodes(G, pos, nodelist=dmz_edge,           node_shape='*', node_color="#ff8080")
        legend_management_central = nx.draw_networkx_nodes(G, pos, nodelist=management_central, node_shape='o', node_color="#8080ff")
        legend_management_edge    = nx.draw_networkx_nodes(G, pos, nodelist=management_edge,    node_shape='*', node_color="#8080ff")
        legend_others_central     = nx.draw_networkx_nodes(G, pos, nodelist=others_central,     node_shape='o', node_color="#80ff80")
        legend_others_edge        = nx.draw_networkx_nodes(G, pos, nodelist=others_edge,        node_shape='*', node_color="#80ff80")

        # Draw edges (connections)
        legend_conn_int = nx.draw_networkx_edges(G, pos, edge_color='black', style='dotted')
        legend_conn_alert = None

        # Draw dangerous connections between "dmz" and "others"
        for dmz_vlan in vlanmap[0]:
            for management_vlan in vlanmap[2]:
                try:
                    path_between_nodes = nx.has_path(G, source=dmz_vlan, target=management_vlan)
                except nx.exception.NodeNotFound:
                    print('There is no {} or {} vlan from vlanmap in your devices'.format(dmz_vlan,management_vlan))
                    continue

                if path_between_nodes:
                    # All shortest paths in graph
                    routes = nx.all_shortest_paths(G, source=dmz_vlan, target=management_vlan)

                    # ALL paths in graph, don't even try it with connected to each other central nodes number > 10
                    # routes = nx.all_simple_paths(G, source=dmz_vlan, target=management_vlan)

                    # This method is working, but doesn't color paths, may be later...
                    # for path in map(nx.utils.pairwise, routes):
                    #     print(list(path))
                    #     legend_conn_alert = nx.draw_networkx_edges(G, pos, edgelist=(list(path)), edge_color='red')

                    for path in routes:
                        route_edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
                        legend_conn_alert = nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', style='dotted')

        # Building legend without errors
        legend_full_item_list  = [legend_dmz_central, legend_dmz_edge, legend_management_central, legend_management_edge,
                                  legend_others_central, legend_others_edge, legend_conn_int, legend_conn_alert]
        legend_full_value_list = ['DMZ multiple vlan', 'DMZ single vlan', 'Management multiple vlan',
                                  'Management single vlan', 'Other multiple vlan', 'Other single vlan',
                                  'Connected interface', 'Dangerous connection']

        legend_item_list, legend_value_list = get_legend(legend_full_item_list,legend_full_value_list)

        plt.legend(legend_item_list,
                   legend_value_list,
                   loc=1, framealpha=0.5, fontsize='small', markerscale=0.5, edgecolor='Black')

    # Delete X and Y symbols and values on graph
    plt.xticks([])
    plt.yticks([])

    # Delete space between plot and window edge
    plt.tight_layout()

    # Save graph as png picture
    if graph_path:
        vlam_labels = {}
        for key in pos:
            if type(key) is int:
                vlam_labels.update({key: key})

        # Draw only vlan numbers
        nx.draw_networkx_labels(G, pos, labels=vlam_labels, font_size=10)

        # 800 dpi may be too high value, try different
        plt.savefig(graph_path+".png", dpi=800)

    # Interactive mode
    else:
        # Draw all labels
        nx.draw_networkx_labels(G, pos, font_size=12)

        plt.show()
