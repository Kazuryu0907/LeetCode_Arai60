WATER = 0
LAND = 1
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def getAreaOfIsland(location: tuple[int, int]) -> int:
            area = 0
            stack = [location]
            while len(stack) >= 1:
                location = stack.pop()
                x, y = location
                # grid外ならはじく
                if not self.isInsideOfGrid(location, grid):
                    continue
                # 見る必要ないCellならはじく
                if grid[x][y] != LAND or location in seen:
                    continue
                seen.add(location)
                area += 1
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

            return area

        seen = set()
        max_area = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                location = (x, y)
                if grid[x][y] == WATER or location in seen:
                    continue
                area = getAreaOfIsland(location)
                max_area = max(max_area, area)
        return max_area
    
    def isInsideOfGrid(self, location: tuple[int, int], grid: List[List[int]]) -> bool:
        x, y = location
        if x < 0 or y < 0:
            return False
        if x >= len(grid) or y >= len(grid[0]):
            return False
        return True 
