class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = [[0 for _ in range(n)] for _ in range(m)]
        paths[0] = [1 for _ in range(n)]
        for i in range(m):
            paths[i][0] = 1
        for i in range(1, m):
            for j in range(1, n):
                paths[i][j] = paths[i-1][j] + paths[i][j-1]
        return paths[-1][-1]
