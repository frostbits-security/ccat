import networkx as nx
import matplotlib.pyplot as plt


def draw_plot(switches_dict):

    sets = []
    sets2 = []

    for switch in switches_dict:
        result_dict = {}

        for iface in switches_dict[switch]:
            if len(switches_dict[switch][iface]) > 0:
                result_dict.update({iface:switches_dict[switch][iface]})
        print(result_dict)

        for iface_vlans in result_dict:
            for vlan in result_dict[iface_vlans]:
                sets.append((vlan, switch + ' ' + iface_vlans))
    print('..............FULL....SETS.............')
    print(sets)

    # Filling set1 as RED nodes on graph and set2 as BLUE nodes
    sets1 = sets.copy()
    x = 0
    for xxx in sets:
        got_it = False
        x += 1
        fff = x
        while fff < len(sets):
            if xxx[0] == sets[fff][0]:
                sets2.append(sets[fff])
                sets1.remove(sets[fff])
                got_it = True
            fff += 1
        if got_it:
            sets2.append(sets[sets.index(xxx)])
            sets1.remove(sets[sets.index(xxx)])

    print('..................SETS1.............')
    print(sets1)
    print('..................SETS2.............')
    print(sets2)

    # draw graph
    G = nx.Graph()
    G.add_edges_from(sets)
    pos = nx.spring_layout(G)

    print('..............................G NODES......................')
    print(G.nodes)
    print('..............................G EDGES......................')
    print(G.edges)

    # lst1 - list of sets1 nodes, lst2 - list of sets2 nodes
    lst1 = []
    for item in sets1:
        lst1.append(item[0])
    lst2 = []
    for item in sets2:
        lst2.append(item[0])

    print('---------------------------LIST 1 AND LIST 2 --------------------')
    print(lst1)
    print(lst2)
    print('------------------------------POS--------------------------------')
    print(pos)

    nx.draw_networkx_nodes(G, pos, nodelist=lst1, node_color="r", with_labels=False)
    nx.draw_networkx_nodes(G, pos, nodelist=lst2, node_color="b", with_labels=False)

    nx.draw_networkx_edges(G, pos, edge_color='black', font_size=16, with_labels=False)


    # raise text positions
    for p in pos:
        pos[p][1] += 0.07
    nx.draw_networkx_labels(G, pos)

    # Save graph as png picture
    #plt.savefig("network_map.png")

    plt.show()

