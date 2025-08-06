class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        def dfs_delete_one_island(row: int, col: int):
            if row < 0 or rows <= row or col < 0 or cols <= col or grid[row][col] == "0":
                return
            grid[row][col] = "0"
            dfs_delete_one_island(row+1, col)
            dfs_delete_one_island(row, col+1)
            dfs_delete_one_island(row-1, col)
            dfs_delete_one_island(row, col-1)
        
        num_of_islands = 0
        for col in range(cols):
            for row in range(rows):
                if grid[row][col] == "1":
                    dfs_delete_one_island(row, col)
                    num_of_islands += 1
        return num_of_islands
