WATER = 0

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        seen = set()
        max_area = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] != WATER:
                    location = (x, y)
                    area = self.getAreaOfIsland(location, grid, seen)
                    max_area = area if max_area < area else max_area
        return max_area
    
    def getAreaOfIsland(self, location: tuple[int, int], grid: List[List[int]], seen: Set[tuple[int, int]]) -> int:
        stack = [location]
        area = 0
        while len(stack) >= 1:
            location = stack.pop()
            x, y = location
            # grid外ならはじく
            if not self.isInsideOfGrid(location, grid):
                continue
            # WATERないしはseenならはじく
            if grid[x][y] == WATER or location in seen:
                continue
            seen.add(location)
            # もし未踏のcellならareaを増やす
            area += 1
            # right
            stack.append((x + 1, y))
            # left
            stack.append((x - 1, y))
            # top
            stack.append((x, y + 1))
            # bottom
            stack.append((x, y - 1))
        return area
        
    def isInsideOfGrid(self, location: tuple[int, int], grid: List[List[int]]) -> bool:
        x, y = location
        x_max = len(grid)
        y_max = len(grid[0])
        if x < 0 or y < 0:
            return False
        if x >= x_max or y >= y_max:
            return False
        return True
