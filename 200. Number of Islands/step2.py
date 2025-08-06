ISLAND = "1"
WATER = "0" 

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        height = len(grid)
        width = len(grid[0])
        visited = set()
        def traverse_island(r: int, c: int):
            location = (r, c)
            if not (0 <= r < height and 0 <= c < width):
                return
            if location in visited or grid[r][c] == WATER:
                return
            visited.add(location)
            traverse_island(r-1, c)
            traverse_island(r, c-1)
            traverse_island(r+1, c)
            traverse_island(r, c+1)

        num_of_islands = 0
        for r in range(height):
            for c in range(width):
                location = (r, c)
                if location not in visited and grid[r][c] == ISLAND:
                    num_of_islands += 1
                    traverse_island(r, c)
        
        return num_of_islands
