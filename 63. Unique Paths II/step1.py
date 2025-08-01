class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        # ゴールが塞がれてたらnum_pathsは0
        if obstacleGrid[-1][-1] == 1 or obstacleGrid[0][0] == 1:
            return 0
        num_row = len(obstacleGrid)
        num_col = len(obstacleGrid[0])
        num_paths = [[0] * num_col for _ in range(num_row)]
        exist_row_obstacle = False
        exist_col_obstacle = False
        for i in range(num_row):
            if obstacleGrid[i][0] == 1:
                exist_row_obstacle = True
            num_paths[i][0] = 0 if exist_row_obstacle else 1
        for i in range(num_col):
            if obstacleGrid[0][i] == 1:
                exist_col_obstacle = True
            num_paths[0][i] = 0 if exist_col_obstacle else 1
        for i in range(1, num_row):
            for j in range(1, num_col):
                if obstacleGrid[i-1][j] == 0:
                    num_paths[i][j] += num_paths[i-1][j]
                if obstacleGrid[i][j-1] == 0:
                    num_paths[i][j] += num_paths[i][j-1]
        return num_paths[-1][-1]
