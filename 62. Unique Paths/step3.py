class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        num_paths = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    num_paths[i][j] = 1
                    continue
                num_paths[i][j] = num_paths[i-1][j] + num_paths[i][j-1]
        return num_paths[-1][-1]
