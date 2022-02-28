from pwn import *
import itertools
import numpy as np
from functools import reduce
from operator import mul
import math


url = 'chall.ctf.bamboofox.tw'
port = 10069

conn = remote(url, port)


def cmp(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


class Easy_Solver(object):
    def __init__(self, grid, size):
        self.grid = list(itertools.chain(*grid))
        self.size = size
        self.graph = {}
        self.connected_groups = []

        self.simpify_grid()
        self.generate_graph()
        self.get_all_connected_groups()
        sorted(self.connected_groups, key=len, reverse=True)

        self.print_grid()
        # print(self.graph)
        print(self.connected_groups)

    def print_grid(self, grid=None):
        if grid is None:
            grid = self.grid

        for i in range(self.size):
            for j in range(self.size):
                print(grid[i * self.size + j], end='')
            print() 
        print()

    def simpify_grid(self):
        swaps = True
        while swaps:
            swaps = False
            for pos in range(len(self.grid)):
                row = pos // self.size
                col = pos % self.size

                if self.grid[pos] == '#':
                    moves = self.get_possible_moves(row, col)
                    if len(moves) == 1:
                        self.grid[pos] = '-'
                        self.grid[moves[0]] = '-'
                        swaps = True

    def generate_graph(self):
        for pos in range(self.size * self.size):
            if self.grid[pos] == '#':
                row = pos // self.size
                col = pos % self.size
                self.graph[pos] = set(self.get_possible_moves(row, col))

    def get_all_connected_groups(self):
        already_seen = set()
        for node in self.graph:
            if node not in already_seen:
                connected_group, already_seen = self.get_connected_group(node, already_seen)
                self.connected_groups.append(connected_group)

    def get_connected_group(self, node, already_seen):
        result = []
        nodes = set([node])
        while nodes:
            node = nodes.pop()
            already_seen.add(node)
            nodes.update(n for n in self.graph[node] if n not in already_seen)
            result.append(node)
        return result, already_seen

    def get_possible_moves(self, row, col):
        moves = []
        if col + 1 < self.size and self.grid[row * self.size + col + 1] == '#':
            moves.append(row * self.size + col + 1)

        if col - 1 >= 0 and self.grid[row * self.size + col - 1] == '#':
            moves.append(row * self.size + col - 1)

        if row + 1 < self.size and self.grid[(row + 1) * self.size + col] == '#':
            moves.append((row + 1) * self.size + col)

        if row - 1 >= 0 and self.grid[(row - 1) * self.size + col] == '#':
            moves.append((row - 1) * self.size + col)

        return moves

    def solve(self):
        if self.grid.count('#') % 2 == 1:
            ans = "no"
        else:
            ans = "yes"
            for component in self.connected_groups:
                if len(component) % 2 == 1:
                    ans = "no"
                    break
                # if not self.hamilton(len(component), component[0]):
                #     ans = "no"
                #     break

        return ans


class Ex_Solver(Easy_Solver):
    def __init__(self, grid, size):
        Easy_Solver.__init__(self, grid, size)
        self.path_count = 0
        self.paths = []
        print(self.graph)
        print()

    def form_adjacency(self):
        if self.size % 2 == 1:
            num_black = self.size ** 2 // 2 + 1
            num_white = self.size ** 2 // 2
        else:
            num_black = num_white = self.size ** 2 // 2

        M = [[0] * num_white for i in range(num_black)]
        black_tiles = {}
        white_tiles = {}
        black_count = white_count = 0
        tile_mapping = {}

        for pos in range(self.size ** 2):
            row = pos // self.size
            col = pos % self.size
            if (row + col) % 2 == 0:
                if self.grid[pos] == '#':
                    black_tiles[pos] = black_count
                black_count += 1
            else:
                if self.grid[pos] == '#':
                    white_tiles[pos] = white_count
                white_count += 1

        for pos in black_tiles:
            row = pos // self.size
            col = pos % self.size
            for j in self.get_possible_moves(row, col):
                if black_tiles[pos] < white_tiles[j]:
                    M[black_tiles[pos]][white_tiles[j]] = 1
                else:
                    M[black_tiles[pos]][white_tiles[j]] = -1

        return M

    def per(self, mtx, column, selected, prod, output=False):
        """
        Row expansion for the permanent of matrix mtx.
        The counter column is the current column, 
        selected is a list of indices of selected rows,
        and prod accumulates the current product.
        """
        if column == mtx.shape[1]:
            if output:
                print(selected, prod)
            return prod
        else:
            result = 0
            for row in range(mtx.shape[0]):
                if not row in selected:
                    result += self.per(mtx, column+1, selected+[row], prod*mtx[row,column])
            return result

    @staticmethod
    def npperm(M):
        print(M)
        n = M.shape[0]
        d = np.ones(n)
        j =  0
        s = 1
        f = np.arange(n)
        v = M.sum(axis=0)
        p = np.prod(v)
        while (j < n-1):
            v -= 2*d[j]*M[j]
            d[j] = -d[j]
            s = -s
            prod = np.prod(v)
            p += s*prod
            f[0] = 0
            f[j] = f[j+1]
            f[j+1] = j+1
            j = f[0]
        return p/2**(n-1) 

    def hamilton(self, size, pt, path=None, or_path=None):
        if path is None and or_path is None:
            path = []
            or_path = []

        # print('hamilton called with pt={}, path={}'.format(pt, path))
        if pt not in set(path):
            path.append(pt)
            if len(path)==size:
                temp = ['-' for i in range(self.size**2)]
                second = False
                for i in range(size):
                    if second and abs(path[i] - prev) == self.size:
                        temp[path[i-1]] = 'v'
                        temp[path[i]] = 'v'
                        second = False
                    elif second and abs(path[i] - prev) == 1:
                        temp[path[i-1]] = 'h'
                        temp[path[i]] = 'h'
                        second = False
                    else:
                        prev = path[i]
                        second = True 

                if temp not in self.paths:
                    self.paths.append(temp)
                    self.path_count += 1
                    # self.print_grid(temp)
                    # print(path)
            for pt_next in self.graph.get(pt, []):
                res_path = [i for i in path]
                candidate = self.hamilton(size, pt_next, res_path)
                if candidate is not None:  # skip loop or dead end
                    return candidate
            # print('path {} is a dead end'.format(path))
        else:
            # print('pt {} already in path {}'.format(pt, path))
            pass
        # return False

    def solve(self):
        if self.grid.count('#') % 2 == 1:
            ans = 0
        elif self.grid.count('-') == self.size ** 2:
            ans = 1
        else:
            adj = self.form_adjacency()
            print(np.array(adj))
            # ans = self.per(np.array(adj), 0, [], 1)
            # ans = self.fast_glynn_perm(adj)
            # ans = self.npperm(np.asarray(adj, dtype=np.float64))
            ans = math.sqrt(np.linalg.det(np.array(adj)))
            print(ans)
            ans = int(ans)
            # ans = 1
            # for component in self.connected_groups:
            #     if len(component) % 2 == 1:
            #         ans = 0
            #         break
                
            #     self.path_count = 0
            #     for start in component:
            #         self.hamilton(len(component), start)
            #     ans *= self.path_count

        return str(ans)


def main():
    # mode = 'easy'
    mode = 'excruciating'
    solver = Easy_Solver if mode == 'easy' else Ex_Solver
    num_tests = 32

    ################
    # intro stuff
    ################

    print('\n' + '=' * 100 + '\n')
    intro = conn.recv().decode('utf-8')
    print(intro)
    print('=' * 100 + '\n')

    ################
    # set game mode
    ################

    conn.sendline(mode)
    example = conn.recv().decode('utf-8')
    print(example)

    ################
    # start game
    ################

    conn.sendline()

    for i in range(num_tests):
        # test = conn.recv().decode('utf-8').strip().split('\n')
        # print(test)
        test_no = conn.recvline().decode('utf-8').strip()
        conn.recvline()

        size = int(conn.recvline().decode('utf-8').strip())
        grid = []
        for i in range(size):
            grid.append(list(conn.recvline().decode('utf-8').strip()))
        conn.recvline()
        conn.recvline()

        print(test_no)
        print("Original Grid:", grid)
        # print(size)

        ans = solver(grid, size).solve()
        print("Ans:", ans)
        conn.sendline(ans)

        result = conn.recvline().decode('utf-8')
        print(result)

    print(conn.recv().decode('utf-8'))


def test():
    grid = ['#', '#', '#', '#', '-', '#', '-', '-', '#']
    ans = Easy_Solver(grid, 3).solve()
    print(ans, '\n')

    grid = list('####--##########')
    ans = Easy_Solver(grid, 4).solve()
    print(ans, '\n')

    grid = list('----##---###---#####----##----------')
    ans = Ex_Solver(grid, 6).solve()
    print(ans, '\n')

    grid = list('---######')
    ans = Ex_Solver(grid, 3).solve()
    print(ans, '\n')


if __name__ == '__main__':
    # test()
    main()