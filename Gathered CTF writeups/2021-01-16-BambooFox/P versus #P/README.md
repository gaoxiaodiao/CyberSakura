# P versus #P

> Points: 500 [500]

## Description

> Welcome to the BambooFox CTF interactive online judge system v0.1!
> 
> In this challenge, you have to solve a problem with 32 test cases in total.
> If you answer a test case correctly, the judge will show you the next test case.
> If you answer a test case incorrectly, the judge will immediately exit.
> You have 30 seconds to solve each of them.
> 
> There are 2 versions for this problem: EASY and EXCRUCIATING.
> You'll receive the flag only if you answer all test cases of the EXCRUCIATING
> version correctly.
> 
> Let the fun begin!
> 
> Which version do you want to solve? (EASY or EXCRUCIATING)
> 
> OK, here is the EXCRUCIATING problem.
> 
> A 'domino tile' is a 1x2 rectangle that can cover two adjacent cells on the
> grid. Each domino tile can be either horizontal or vertical. For example, in
> the grid below, you can cover two cells of the same number with a domino tile:
```
------
-11-2-
----2-
------
```

> In this problem, you will be given an integer n (2 <= n <= 50) and an n*n grid
> Each grid cell contains one character: '#' or '-'. A "valid configuration" is a
> way of placing dominoes on the grid, such that each domino tile covers two '#'
> characters, and each '#' is covered by exactly one domino.
> 
> Given the grid, your task is to count the number of valid configurations.
> 
> An example input is:
```
4
##-#
##-#
###-
#---
```
> The answer is 2, and all valid configurations are
```
11-3           12-3
22-3           12-3
455-    and    455-
4---           4---
```
> where each domino tile covers two cells with the same number.
> 
> Another example input is:
```
3
#--
##-
-##
```
> The answer is 0. There are an odd number of '#'s to cover, and since each domino
> tile covers exactly two cells, no valid configuration exists.

## Solution

I worked on this problem for half a day but still did not manage to solve it in the end :(

**Idea 1**

I first tried the naive method of brute forcing all possible ways to place the dominos using the back tracking algorithm. *See Easy_Solver*

**Idea 2**

I realised the problem set could be simplified since there would be some pieces where there would only be one possible way to place the domino. *See Easy_Solver.simplify_grid*

**Idea 3**

After spending close to 3 hours working on the problem so far, I realised the domino placing could be modeled using a hamilton path. *See Ex_Solver.hamilton*
1. The original problem space would first be mapped to a graph
2. Decompose the graph into its respective component graph such that all the component graphs are connected.
3. Find the number of unique hamilton paths for each component.
4. Find the product of all the unique paths in each component.

Problems:
* The tilings for the dominos may not be unique even if the hamilton path is unique. Could be solved by storing the dominoconfiguration of the path instead of the path itself
* Still too slow

**Idea 4**

Use the FKT algorithm. Did not manage to finish this.
> The FKT algorithm, named after Fisher, Kasteleyn, and Temperley, counts the number of perfect matchings in a planar graph in polynomial time. 
> This same task is #P-complete for general graphs. For matchings that are not required to be perfect, counting them remains #P-complete even for planar graphs. 
> The key idea of the FKT algorithm is to convert the problem into a Pfaffian computation of a skew-symmetric matrix derived from a planar embedding of the graph. 
> The Pfaffian of this matrix is then computed efficiently using standard determinant algorithms.

1. Find a graph H that is a directed version of G, such that an odd number of edges are oriented clockwise for every face in G.
2. Calculate B, the (1,−1,0)-adjacency matrix of H.
3. The perfect number of matchings for G is pf(B)=sqrt(det(B))

*Assume that the vertex set of G is {1,…,n}. If i and j are not adjacent, set Bi,j=0. If i and j are adjacent and i<j, set Bi,j=+1 and Bj,i=−1; if i and j are adjacent and i>j set Bi,j=−1 and Bj,i=+1. Now B is skew symmetric and det(B) is the square of the number of perfect matchings of G.*

## References
* Thank to arseny30 for providing the [solution](FKT.py)
* http://numberworld.blogspot.com/2014/03/an-implementation-of-fkt-algorithm.html
* https://www.math.cmu.edu/~bwsulliv/domino-tilings.pdf


## Flag
``