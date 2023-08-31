# The pcap file was downloaded from www.github.com/tturba/wireshark
# You open pcap at your own risk

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

# Here change path/file if you are playing with other wireshark data
wireURL = 'wireshark.csv'
wireData = pd.read_csv(wireURL)
# print(wireData.head(10))

#printing most important parts
print('''
************************************************************************
*                                                                      *
*                           HTTP Protocol                              *
*                                                                      *
************************************************************************
''')
print(wireData[wireData['Protocol'] == 'HTTP'])
print('\n\n\n')



print('''
************************************************************************
*                                                                      *
*                            Domain names                              *
*                                                                      *
************************************************************************
''')
print(wireData[~wireData['Domain'].isna()])
print('\n\n\n')

print('''
************************************************************************
*                                                                      *
*                        How is it connected                           *
*     Cool graph is saved in "graph.html", check it out in browser     *
*                                                                      *
************************************************************************
''')

G = nx.from_pandas_edgelist(wireData, source='Source', target='Destination', edge_attr=['Time', 'Protocol', 'Stream', 'Info'])
net = Network(notebook=True)
net.from_nx(G)
net.toggle_physics(True)
net.show('graph.html')

print('''
************************************************************************
*                                                                      *
*                     Percentage of sent packets                       *
*      Please note, that this chart does not provide full statistics   *
*                                                                      *
************************************************************************
''')

data={}
for ip in wireData['Source']:
    if ip in data.keys():
        data[ip]+=1
    else:
        data[ip]=1

labels, dataDict = data.keys(), data.values()
mean=[i*100/len(wireData['Source']) for i in dataDict]

newLabel=[]
newData=[]

for j,k in zip(labels, mean):
    if k > 0.4:
        newLabel.append(j)
        newData.append(k)


plt.figure('Who sent packets')
plt.pie(newData, labels=newLabel, autopct='%.1f%%')
# plt.legend(loc='best')
plt.annotate('Please note, that IP addresses that were sending not enough packets are not shown', (-1.25,-1.22))
plt.title('Percentage of sent packets')
plt.show()


print('''
************************************************************************
*                                                                      *
*                     Percentage of protocols used                     *
*                                                                      *
************************************************************************
''')

dataProtocol={}
for protocol in wireData['Protocol']:
    if protocol in dataProtocol.keys():
        dataProtocol[protocol]+=1
    else:
        dataProtocol[protocol]=1

labelsProtocol, dataDictProtocol = dataProtocol.keys(), dataProtocol.values()
meanProt=[i*100/len(wireData['Protocol']) for i in dataDictProtocol]

newLabelProt=[]
newDataProt=[]

for j,k in zip(labelsProtocol, meanProt):
    if k > 0.4:
        newLabelProt.append(j)
        newDataProt.append(k)


plt.figure('Which protocols used')
plt.pie(newDataProt, labels=newLabelProt, autopct='%.1f%%')
# plt.legend(loc='best')
plt.title('Percentage of protocols used')
plt.show()



print('''
************************************************************************
*                                                                      *
*                         Few more statistics                          *
*                                                                      *
************************************************************************
''')

#sorting dictionary
#we are assuming that host sents the most of data
data={k:v for k,v in sorted(data.items(), key=lambda x: x[1])}
hostIP = list(data.keys())[-1]
ctr = 0
for i in wireData['Destination']:
    if hostIP==i:
        ctr+=1
print(f'Host IP: {hostIP}')
print(f'Packets sent: {data.get(hostIP)}\nPackets received: {ctr}')
print('All IPs that sent at least 1 packet to our host:')

dataKeys = list(data.keys())
for ip in range(len(dataKeys)-1):
    print(dataKeys[ip], end='   ')
print()

