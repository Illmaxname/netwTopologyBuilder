from pyvis.network import Network
import networkx as nx
import pandas as pd

def EndChecking(id, word):#=============deleting unnecessary symbols
    l = len(id)
    lw = len(word)
    if id[l - lw: l] == str(word):
        return id.split(str(word))[0]
    else:
        return id

file_name = 'devices.txt'

f = open(file_name)
full_txt = f.read()

# ========fill nums of neighbors array
list_nums = list()  # ====nums of neighbors

for i in range(1000):
    full_txt = full_txt.replace(':', '', 1)
    res = full_txt.split(': ')[1]
    num = res.split('\n')[0]
    t = res.split('\n')[1]
    list_nums.append(int(num))
    if t == '--':
        break
    full_txt = full_txt.replace(':', '', 1)

f.close()

with open(file_name) as ft:
    line = ft.readline()
    if '>' in line:
        nline = line.split('>')[0]
    elif '#' in line:
        nline = line.split('#')[0]
ids = list()
ids.append(nline)

#==============getting root names
with open(file_name) as ft:
    for num in range(len(list_nums) - 1):
        count = list_nums[num] + 8
        if num > 0:
            count -= 1
        for i in range(count):
            ft.readline()

        fid = ft.readline()
        if '>' in fid:
            id = fid.split('>')[0]
        elif '#' in fid:
            id = fid.split('#')[0]
        ids.append(id)

net = nx.Graph()

#statistic vars
non_rep = ids
repeatable = []

rep = 0
net_ints = []
network_nodes = []
net_ports = []
skp = 5
#=============creating DataFrames
for i in range(len(list_nums)):
    nums = list_nums[i]
    text = pd.read_csv(file_name, sep='\s+', header=None, skiprows=skp, nrows=nums + 1, engine='python')

#==============filling the empty 5 column by value 4 column
    col5 = text[4]
    col4 = text[3]
    for count in range(len(text)):
        if col5[count] is None:
            col5[count] = col4[count]

    skp = skp + nums + 8

    root_node = ids[i]
    root_node = EndChecking(root_node, '.STACK')
    root_node = EndChecking(root_node, '.glavapu.local')
    root_node = EndChecking(root_node, '.glavapu.')
    root_node = EndChecking(root_node, '.C2960')

    root_label = ' '.join(['\n', ids[i]])
    network_nodes = []
    network_nodes.append(root_node)

    net.add_node(root_node, title='Neighbors: '+str(list_nums[i])+'\n'+str(text[1]), font="40", label=root_label, size=20, color='#20f736', width=3)

    name = text[0]
    locInt = text[1]
    port = text[4]
    # ===========add devices (green nodes)
    for nums in range(len(text)):
        name[nums] = EndChecking(name[nums], '.STACK')
        name[nums] = EndChecking(name[nums], '.glavapu.local')
        name[nums] = EndChecking(name[nums], '.glavapu.')
        name[nums] = EndChecking(name[nums], '.C2960')
        label_nodes = ' '.join(['\n', str(name[nums])])


        if name[nums] != port[nums]:
            net.add_node(str(name[nums]), font="40", label=label_nodes, size=20, color='#20f736', width=3)
            if name[nums] not in non_rep:
                non_rep.append(name[nums])
        elif name[nums] == port[nums]:
            net.add_node(str(name[nums]), font="20", label=label_nodes, size=20, color='#00bfff', width=3)
            repeatable.append(name[nums])


    # ===========add interfaces, nodes + edges
    for ints in range(len(text)):

        if 'Ethernet' in locInt[ints]:
            temp = str(locInt[ints])
            locInt[ints] = 'Eth' + str(temp[8:len(temp)])
        elif 'ethernet' in locInt[ints]:
            temp = str(locInt[ints])
            locInt[ints] = 'Eth' + str(temp[8:len(temp)])
        elif 'ether' in locInt[ints]:
            temp = str(locInt[ints])
            locInt[ints] = 'Eth' + str(temp[5:len(temp)])


        id_ints = ''.join(locInt[ints])
        id_ints = id_ints + '|' + '00'

        if id_ints not in net_ints:
            net_ints.append(id_ints)

        else:
            id_ints = ''.join(locInt[ints])
            id_ints = id_ints+'|'+str(rep)

            rep = rep + 1
            net_ints.append(id_ints)


        nt = Network(height=1500, width=1900)
        nt.from_nx(net)

        fl = False
        if id_ints[0:2] != 'Gi':
            rt_n_lst = nt.neighbors(root_node)

            for ns in rt_n_lst:
                if id_ints.split('|')[0] == ns.split('|')[0]:
                    fl = True
                    break
            if fl == True:
                continue
        net.add_node(id_ints, label=locInt[ints], size=5, color='#0f6cf7', width=3)
        net.add_edge(root_node, id_ints, color='black', length=10)
        li = id_ints

        if 'Ethernet' in port[ints]:
            temp = str(port[ints])
            port[ints] = 'Eth'+str(temp[8:len(temp)])
        if 'ethernet' in port[ints]:
            temp = str(port[ints])
            port[ints] = 'Eth'+str(temp[8:len(temp)])


        id_ints = ''.join(port[ints])
        id_ints = id_ints + '|' + '00'
        if id_ints not in net_ints:
            net_ints.append(id_ints)
            net.add_node(id_ints, label=port[ints], size=5, color='#0f6cf7', width=3)
        else:
            id_ints = ''.join(port[ints])
            id_ints = id_ints+'|'+str(rep)

            rep = rep + 1
            net_ints.append(id_ints)
            net.add_node(id_ints, label=port[ints], size=5, color='#0f6cf7', width=3)

        net.add_edge(id_ints, str(name[ints]), color='black', length=10)

        net.add_edge(li, id_ints, color='black', length=10)

n_root = int((len(ids) + len(non_rep))/2)
n_end = len(repeatable)
n_total = n_end+n_root

net.add_node('num_of_root', title='Inaccurate data!', font="60", label='Num of switches: ' + str(n_root) + '\nNum of end devices: '+str(n_end)+'\nTotal num of devices: '+str(n_total), size=40,
                 color='gray', width=3, shape='box', phisics=False, y=1400, x=1800, group='info')


nt = Network(height=1500, width=1900)
nt.from_nx(net)
nt.show_buttons(filter_=['physics'])

nt.show('topo_base_camp.html')

