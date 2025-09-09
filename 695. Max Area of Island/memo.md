# step1
島の最大面積を求める問題
前回のBFSかDFSかで面積を計算して，最後にmax取ればいけそう
前回のやり方思い出すところから
とりあえず手を動かしてみる．

## 方針
- areaの計算をするので，再帰で端っこから値を戻していくよりも，stack行列作ってそれをwhileで回した方がインクリメントするだけでできるのでよさそう(iterative)
- 
ACしたコード↓
```py
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

```
思い出しながら解いてたら20分かかった
空間計算量はseenが最大O(n*m) (m = len(grid), n = len(grid[0]))
max_areaはO(1)だけど，stackの空間計算量とかどうやって考慮すればいいんだろう．
島の大きさによるよな...?上からつぶすならO(n*m)だけど，考えにくい．

# step2
ほかの人のコードを見てみる
- https://github.com/Kaichi-Irie/leetcode-python/pull/14
あ，またエッジケース考えるの忘れてた
何ならleetCodeの制約条件も見てなかった．よりよいsolutionを考えるには絶対必要だし直していく
制約条件は以下
`1 <= len(grid), len(grid[0]) <= 50`
最大で50^2だから2500か　結構ちっさい？
再帰をするならrecursion limitを考えないといけない大きさだ

~~visitedを引数で受け取らずに，global変数として参照してる．
こういうのってどうなんだろう~~
closureかと思ったらclosureじゃなかった
まあ，ユーザーがseenを変更するモチベーションはないし，する必要もないから，引数として渡す理由は薄いかも
そもそも関数内関数ならこういう使い方をするべきだし，メリットか．スコープ内で完結してるし


この問題だと走査する順番は関係ないから，DFSでもBFSでもどっちでもよさそう
やり方的には全く一緒
- https://github.com/t0hsumi/leetcode/pull/19/files
Union-Findでやってる
```py
uf = UnionFind(lands)
for row, column in lands:
    if (row + 1, column) in lands:
        uf.union((row, column), (row + 1, column))
    if (row, column + 1) in lands:
        uf.union((row, column), (row, column + 1))
return uf.compute_maxsize()
```
隣接してる島に対してunionしていけばいいのか．なるほど
unionが同じ引数に対して何回実行しても，内部のtreeは一緒だからこれでできるのね
grid内の判定を`is_explorable`っていう変数でやってる
explorableって単語存在しないのか．それならisInsideGridとかのほうが直感的で正しいかも．(今回はSolutionのコードにOfがついてたからつけたけど)

関数内関数にしてみた．見通しがよくなっていいと思う
```py
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
```

# step3
`== WATER`から，`!= LAND`に変更した．こっちのほ直感的にわかると思う

```py
LAND = 1
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def getAreaOfIsland(location: tuple[int, int]) -> int:
            area = 0
            stack = [location]
            while len(stack) >= 1:
                location = stack.pop()
                x, y = location
                if not self.isInsideOfGrid(location, grid):
                    continue
                if grid[x][y] != LAND or location in seen:
                    continue
                area += 1
                seen.add(location)

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
                if grid[x][y] != LAND or location in seen:
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
```

===

2025/9/9更新
# step4
Odaさんのcommentを元にもう一回度書いてみる
```py
LAND = 1
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def getAreaOfIsland(location: tuple[int, int]) -> int:
            stack = [location]
            area = 0
            while stack:
                location = stack.pop()
                x, y = location
                # grid外の場合
                if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
                    continue
                # みる必要がない場合
                if grid[x][y] != LAND or location in seen:
                    continue
                area += 1
                seen.add(location)
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
                if grid[x][y] != LAND or location in seen:
                    continue
                area = getAreaOfIsland(location)
                max_area = max(max_area, area)
        
        return max_area
```