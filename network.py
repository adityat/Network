import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
import math
import random
import numpy as np

def distance(pos1,pos2):
	return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

def mag(vec):
	return math.sqrt(vec[0]**2+vec[1]**2)

class Disk:
	def __init__(self, radius, pos,inpipe,dist):
		self.radius = radius
		self.pos = pos
		self.inpipe=inpipe
		self.dist=dist

arrayList = []

G=nx.Graph()

G.add_nodes_from([1,2,3,4,5,6])

G.add_edges_from([(1,2),(2,3),(2,4),(3,4),(4,5),(1,6),(5,6)])

G[1][2]['cond']=10
G[2][3]['cond']=10
G[2][4]['cond']=10
G[3][4]['cond']=10
G[4][5]['cond']=10
G[1][6]['cond']=10
G[5][6]['cond']=10

pos={1: (0,0), 2: (1,0), 3:(1.5,1),4:(2,0), 5: (3,0),6: (1.5,-0.5)}

for i in G.edges():
	ind1=i[0]
	ind2=i[1]

	G[ind1][ind2]['length']=distance(pos[ind1],pos[ind2])

print G[5][6]['length']

source = 1 #Defining the source
sink = 5 

#print pos[2],pos[1]

#for n,nbrs in G.adjacency_iter():
#	for m,mnbrs in nbrs.items():
#		print (n,m,mnbrs['cond'])


plt.ion()
T=10 #(1/frequency)
for t in range (0,200):
	print t
	speed=0.05
	for i in G.edges():
		ind1=i[0]
		ind2=i[1]
		nx.draw_networkx_nodes(G,pos)
		nx.draw_networkx_edges(G,pos,edgelist={i},width=G[ind1][ind2]['cond'])
		#print i[1]
	
	
		
	#Source
	if (t%T==0) :
		newDisk=Disk(0.02,list(pos[source]),[source,random.choice(G.neighbors(source))],0)
		arrayList.append(newDisk)

	#Update positions
	for mem in arrayList:
		ind1=mem.inpipe[0]
		ind2=mem.inpipe[1]
		mod=distance(pos[ind1],pos[ind2])
		direct=[(pos[ind2][0]-pos[ind1][0])/mod,(pos[ind2][1]-pos[ind1][1])/mod]
		#print "mag", mag(direct)
		
		mem.dist+=speed
		mem.pos[0]=pos[ind1][0]+mem.dist*direct[0]
		mem.pos[1]=pos[ind1][1]+mem.dist*direct[1]
		
		
		
		
		#print mem.dist, mem.pos

		if math.fabs(mem.dist-G[ind1][ind2]['length'])<=0.03:
			if(ind2==sink):
				arrayList.remove(mem)
			else:
				mem.inpipe[0]=ind2
				mem.dist=0
				mem.pos=list(pos[ind2])
				#number=len(G[ind2])-1
				
			
				while True:
					rand=random.choice(G.neighbors(ind2))
					if rand!=ind1:
						mem.inpipe[1]=rand
						break

		plt.gca().add_patch(plt.Circle(mem.pos,mem.radius, color='g'))
		
		#print mem.pos
	plt.draw()	
