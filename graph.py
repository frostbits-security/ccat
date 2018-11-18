import networkx as nx
import matplotlib.pyplot as plt
import re
import os

def draw_plot(switches_dict, vlanmap=False):

    # Fill list Sets in the next format: [(vlan_num, 'dev_name_int'),(...)]
    sets = []
    for switch in switches_dict:
        result_dict = {}
        for iface in switches_dict[switch]:
            if len(switches_dict[switch][iface]) > 0:
                # Make short name of interface
                iface_short = re.sub('[a-z]', '', iface)
                result_dict.update({iface_short: switches_dict[switch][iface]})
        print('..............RESULT DICT.............')
        print(result_dict)
        for iface_vlans in result_dict:
            for vlan in result_dict[iface_vlans]:
                # Make short name of switch
                switch_short = (os.path.splitext(switch)[0])[1:]
                sets.append((vlan, switch_short + ' ' + iface_vlans))

    # Fill 2 lists with central and edges nodes
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
    print('.........................SETS...................')
    print(sets)
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
    print('..........................................REMOVE LIST.............')
    print(remove_list)
    G.remove_nodes_from(remove_list)

    # K is the optimal distance between nodes
    pos = nx.spring_layout(G, k=0.2)

    # Increase plot size, 16:9 may lag, try different
    plt.figure(figsize=(16,9))

    if not vlanmap:
        # Draw nodes
        legend_edge_node = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=edge_nodes_list,    node_shape='*',  node_color="#ffff80")
        legend_cent_node = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=central_nodes_list, node_shape='o',  node_color="#ff80ff")

        # Draw edges (connections)
        legend_conn_int  = nx.draw_networkx_edges(G, pos, edge_color='black', font_size=16, style='dotted')


    print('----------------------VLANMAP------------------')
    print(vlanmap)

    if vlanmap:

        dmz_central    = list(set(vlanmap[0]) & set(central_nodes_list))
        dmz_edge       = list(set(vlanmap[0]) & set(edge_nodes_list))
        management_central = list(set(vlanmap[2]) & set(central_nodes_list))
        management_edge    = list(set(vlanmap[2]) & set(edge_nodes_list))

        others_central = list(set(central_nodes_list) - set(management_central) - set(dmz_central))
        others_edge    = list(set(edge_nodes_list)    - set(management_edge)    - set(dmz_edge))

        # Draw nodes
        legend_dmz_central        = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=dmz_central,        node_shape='o', node_color="#ff8080")
        legend_dmz_edge           = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=dmz_edge,           node_shape='*', node_color="#ff8080")
        legend_others_central     = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=others_central,     node_shape='o', node_color="#80ff80")
        legend_others_edge        = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=others_edge,        node_shape='*', node_color="#80ff80")
        legend_management_central = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=management_central, node_shape='o', node_color="#8080ff")
        legend_management_edge    = nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=management_edge,    node_shape='*', node_color="#8080ff")

        # Draw edges (connections)
        legend_conn_int = nx.draw_networkx_edges(G, pos, edge_color='black', font_size=16, style='dotted')
        legend_conn_alert = []

        # Draw dangerous connections between "dmz" and "others"
        for dmz_vlan in vlanmap[0]:
            for management_vlan in vlanmap[2]:
                try:
                    path_between_nodes = nx.has_path(G, source=dmz_vlan, target=management_vlan)
                except nx.exception.NodeNotFound:
                    print('There is no {} or {} vlan from vlanmap in your devices'.format(dmz_vlan,management_vlan))
                    continue

                if path_between_nodes:
                    routes = nx.all_shortest_paths(G, source=dmz_vlan, target=management_vlan)

                    # ALL paths in graph, don't even try it with central nodes number > 10
                    #routes = nx.all_simple_paths(G, source=dmz_vlan, target=management_vlan)

                    # This method is working, but doesn't color paths, may be later...
                    # for path in map(nx.utils.pairwise, routes):
                    #     print(list(path))
                    #     legend_conn_alert = nx.draw_networkx_edges(G, pos, edgelist=(list(path)), edge_color='red')

                    for path in routes:
                        route_edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
                        legend_conn_alert = nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', style='dotted')

    # FOR PNG Draw labels
    vlam_labels = {}
    for key in pos:
        if type(key) is int:
            vlam_labels.update({key:key})
    print('..........................................POS222222222.............')
    print(vlam_labels)

    # FOR INTERACTIVE All labels
    nx.draw_networkx_labels(G, pos, font_size=12)

    # FOR PNG only vlan nums
    #nx.draw_networkx_labels(G, pos, labels=vlam_labels, font_size=10)


    # Delete X and Y symbols and values on graph
    plt.xticks([])
    plt.yticks([])

    # Plot's legend
    if not vlanmap:
        plt.legend((legend_edge_node, legend_cent_node, legend_conn_int),
                   ('Single vlans', 'Multiple vlans', 'Connected interface'),
                   loc=1, framealpha=0.5, fontsize='small', markerscale=0.5,edgecolor='Black')

    if vlanmap:
        plt.legend((legend_dmz_central, legend_dmz_edge, legend_management_central, legend_management_edge, legend_others_central, legend_others_edge, legend_conn_int, legend_conn_alert),
                   ('DMZ multiple vlan', 'DMZ single vlan', 'Management multiple vlan', 'Management single vlan', 'Other multiple vlan', 'Other single vlan', 'Connected interface', 'Dangerous connection'),
                   loc=1, framealpha=0.5, fontsize='small', markerscale=0.5,edgecolor='Black')


    # Delete space between plot and window edge
    plt.tight_layout()

    # Save graph as png picture, 1000 dpi may be too high value, try different
    plt.savefig("network_map.png", dpi=800)

    # Interactive mode
    plt.show()
