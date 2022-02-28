"""
Created on Wed May 15 11:54:57 2019
@author: daryl

#######################################################################
# BASED On An Original Sage Version by:
# AUTHOR: Dr. Christian Schridde
# E-MAIL: christianschridde [at] googlemail [dot] com
#
# DESCRIPTION: Implementation of the FKT-algorithm
#
# INPUT:  Adjacency matrix A of a undirected loop-free planar graph G
# OUTPUT: The number of perfect matchings of G
########################################################################
"""

import networkx as nx #Requires at least netwrokx 2.3+
import matplotlib.pyplot as plt
import random
import math
import numpy as np
import time
import sage.all
import sympy
import scipy
import pwn
import sys
sys.setrecursionlimit(100000)

#Helper Functions
def doNothing():
    return 0;

def find_faces(embd):
    

    #Returns a list of faces of the planar embedding by 
    #the edges that bound the face
    ed_list = list(embd.edges())
    faces=[]
    
    for ed in embd.edges():
        if ed in ed_list:
            faces.append(embd.traverse_face(ed[0],ed[1]))
            
            for i in range(len(faces[-1])):
                ed_list.remove((faces[-1][i],faces[-1][(i+1)%len(faces[-1])]))
                
    face_edges=[]
    for face in faces:
        face_edges.append([])
        for i in range(len(face)):
            face_edges[-1].append((face[i],face[(i+1)%len(face)]))
            
                
    return face_edges


def toSkewSymmetricMatrix(A):
    #Skew--symmetrize a matrix
     
    A[(A==1).T] = -1

    return A

def numberOfClockwiseEdges(face, edgesT1):

    #Iterate over edges of a face to determine
    #the number of positive orientations

    clockwise = 0
    for edge in face:
        if edge in edgesT1:
            clockwise += 1
    return clockwise


def isClockwise(e,face):
    #Checks orientation of an edge on a face
    try:
        face.index(e);
    except ValueError:
        return False
    else:
        return True



#Main Function
def FKT(A):
    n = len(A)
    B_graph = A[:]

    G = nx.Graph(A)
    # matching_size = len(nx.algorithms.matching.maximal_matching(G))
    # print(matching_size, n)
    side = n // 2
    matching_size_2 = sum([x != - 1 for x in scipy.sparse.csgraph.maximum_bipartite_matching(scipy.sparse.coo_matrix(A[0:side, side:side*2]))])
    print(matching_size_2 , n)
    if matching_size_2 * 2 != n:
        return 0

    tf, embd = nx.check_planarity(G)
    
    if embd is None:
        return 0
 
    faces = find_faces(embd)

    T1 = nx.minimum_spanning_tree(G)
    T1 = nx.Graph(T1)

    mask = np.random.randint(2, size=(n, n))
    mask = ((mask + mask.T) == 1)

    B_digraph = A * mask

    G = nx.DiGraph(B_digraph)

    edgesT1 = T1.edges();
    adj_T1 = (nx.adjacency_matrix(T1)).todense();

    for edge in edgesT1:
        if (B_digraph[edge[0], edge[1]] == 0):
            adj_T1[edge[0], edge[1]] = 0
        else:
            adj_T1[edge[1], edge[0]] = 0

    T1 = nx.DiGraph(adj_T1)
    edgesT1 = set(T1.edges())
    if embd is not None:
        faces.sort(key=len)
        faces.reverse()
        faces.pop(0)

    ready_faces = []
    
    if embd is not None:
        while (len(faces) > 0):
            index = -1;
            for face in faces:
                countMissingEdges = 0;
                missingEdge = 0;
                index += 1;
                for edge in face:
                    rev_edge = (edge[1], edge[0])
                    if edge not in edgesT1 and rev_edge not in edgesT1:
                        countMissingEdges += 1;
                        missingEdge = edge;

                if (countMissingEdges == 1):
                # in this face, only one edge is missing.
                # Place the missing edge such that the total number
                # of clockwise edges of this face is odd
                # add this edge to the spanning tree
                    forward = True
                    if ((numberOfClockwiseEdges(face, edgesT1)) % 2 == 1):
                    # insert counterclockwise in adj_T1;
                        if (isClockwise(missingEdge, face) == False):
                            adj_T1[missingEdge[0], missingEdge[1]] = 1;
                        else:
                            adj_T1[missingEdge[1], missingEdge[0]] = 1;
                            forward = False
                    else:
                    # insert clockwise in adj_T1
                        if (isClockwise(missingEdge, face) == True):
                            adj_T1[missingEdge[0], missingEdge[1]] = 1;
                        else:
                            adj_T1[missingEdge[1], missingEdge[0]] = 1;
                            forward = False

                # rebuild the graph
                    old = edgesT1
                    if forward:
                      old.add(missingEdge)
                    else:
                      old.add((missingEdge[1], missingEdge[0]))

                    # T1 = nx.DiGraph(adj_T1);
                    # edgesT1 = list(T1.edges());
                    # print(missingEdge)
                    # print(set(old).symmetric_difference(set(edgesT1)))

                # remove the face that was found
                    faceFound = faces.pop(index);
                    break;
        try: 
            # print(adj_T1.shape)
            n = adj_T1.shape[0] // 2
            m = toSkewSymmetricMatrix(adj_T1)[0:n,n:(n+n)]
            
            print(m.shape)
            return abs(sage.all.matrix(m).det())


            # print(m)
            # print(toSkewSymmetricMatrix(adj_T1))
            # b = math.sqrt(np.linalg.det(toSkewSymmetricMatrix(adj_T1)));
            # print(a, b)

        except ValueError: 
            pass    
    
    

def dfs(v, G, was, color, v_color):
    if was[v]:
        return
    was[v] = True
    color[v_color].append(v)
    for u in range(len(G)):
        if G[u][v]:
            dfs(u, G, was, color, v_color)
    

def solve(n, mask = None):
    size = n * n
    ID = [ [0] * size  for _ in range(size) ] 

    black_id = 0
    white_id = 0
    for i in range(n):
        for j in range(n):
            if mask and mask[i][j] != '#':
                continue
            if (i + j) % 2 == 0:
                ID[i][j] = black_id
                black_id += 1
            else:
                ID[i][j] = white_id
                white_id += 1

     
    real_size = black_id + white_id
    G = [ [0] * real_size  for _ in range(real_size) ] 
    print(n, mask, real_size)

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                ID[i][j] += white_id

    for i in range(n):
        for j in range(n):
            src = ID[i][j]
            if mask and mask[i][j] != '#':
                continue
            if j + 1 < n and (not mask or mask[i][j + 1] == '#'):
              to = ID[i][j + 1]
              G[src][to] = 1
              G[to][src] = 1
            if i + 1 < n and (not mask or mask[i+1][j] == '#'):
              to = ID[i + 1][j]
              G[src][to] = 1
              G[to][src] = 1

    was = [False] * real_size
    color = [[] for _ in range(real_size)]
    next_color = 0
    for v in range(real_size):
        if not was[v]:
            dfs(v, G, was, color, next_color)
            next_color += 1

    res = 1
    for i in range(next_color):
      vs = color[i]
      vs.sort()
      vn = len(vs)
      print(f"{i}th component = ", vs)
      GG = [ [0] * vn  for _ in range(vn) ] 
      for i in range(vn):
          for j in range(vn):
              GG[i][j] = G[vs[i]][vs[j]]
      GG = np.asarray(GG)
      r = FKT(GG)
      print(r)
      res *= r

    print(res)
    return res

solve(3, [
    '-##\n', 
    '---\n', 
    '-##\n'])
solve(3, ['---\n', '--#\n', '-#-\n'])
# solve(3, ['-##\n', '#--\n', '###\n'])
# solve(3, ['###\n', '###\n', '###\n'])
# solve(3, ['###\n', '#--\n', '---\n'])
# exit()


pwn.context.log_level = 'debug'
io = pwn.remote('chall.ctf.bamboofox.tw', 10069)
io.recv()
#io.sendline("EASY")
io.sendline("EXCRUCIATING")
io.recv()
io.sendline("")

while True:
  io.recvuntil(b'===')
  io.recvline()
  n = int(io.recvline())
  print(n)
  mask = [io.recvline().decode('utf-8') for i in range(n)]
  res = solve(n, mask)
  io.recv()
  io.sendline(str(res))
  continue
  if res == 0:
      io.sendline("no")
  else:
      io.sendline("yes")


