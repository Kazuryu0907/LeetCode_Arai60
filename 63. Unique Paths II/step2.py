class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows, num_cols = len(obstacleGrid), len(obstacleGrid[0])
        num_paths = [[0] * num_cols for _ in range(num_rows)]

        if obstacleGrid[0][0] == OBSTACLE or obstacleGrid[-1][-1] == OBSTACLE:
            return 0

        for r in range(num_rows):
            if obstacleGrid[r][0] == OBSTACLE:
                break
            num_paths[r][0] = 1
        for c in range(num_cols):
            if obstacleGrid[0][c] == OBSTACLE:
                break
            num_paths[0][c] = 1
        for r in range(1, num_rows):
            for c in range(1, num_cols):
                if obstacleGrid[r][c] == OBSTACLE:
                    continue
                num_paths[r][c] = num_paths[r-1][c] + num_paths[r][c-1]
        return num_paths[-1][-1]
