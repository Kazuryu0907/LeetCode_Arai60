# step1
- 初めてのGraph
- 1(島)，0(水)が与えられるから，島の数を数える
- 斜めはカウントされない
- こういうやつってUnion-Findしか覚えてない
- DPでも行けそうじゃね...?
- 島のindexをDPに格納して
- 貰うDPで，上と左からもらって，どっちか１なら島のindexを伝播させて，どっちも0ならindexを増加させる
- 本題とそれそうなので後でやる
- Graphの知識がなさすぎるのでお手本見る

- https://github.com/olsen-blue/Arai60/pull/17
- DFSか
```py
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        height = len(grid)
        width = len(grid[0])
        def dfs_delete_one_island(i, j):
            if i < 0 or height <= i or j < 0 or width <= j or grid[i][j] == "0":
                return
            grid[i][j] = "0"
            dfs_delete_one_island(i+1, j)
            dfs_delete_one_island(i, j+1)
            dfs_delete_one_island(i-1, j)
            dfs_delete_one_island(i, j-1)

        num_of_islands = 0
        for i in range(height):
            for j in range(width):
                if grid[i][j] == "1":
                    dfs_delete_one_island(i, j)
                    num_of_islands += 1
        return num_of_islands
```
- なるほど　島からDFSでじわじわ島をたどっていって，島を覆いつくすまで探索していく感じか
- DFSとかvisited変数を使っているイメージ
- 入力破壊がちょっと気になる
- returnの条件文が長いの何とかならないかな．関数に分ける？
- AC
```py
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
```
- Grid(n*m)として
- 時間計算量: O(nm)？再帰の時のオーダー算出が結構怪しい．間違ってる気がする...
- 空間計算量は入力を破壊しているから，実質: O(nm)だと思います

ここまで30分
# step2
- Union-Findについて
- https://discord.com/channels/1084280443945353267/1183683738635346001/1197738650998415500
> union-find  は、微妙に常識から外れるかな(多くの人が知っているだろうが知らなくてもドン引きはされない)、くらいの感覚です。DFS による解法のほうは常識でしょう。
- 最もすぎる話
- まあでも自分が持ってる解法の空間は広いほうがいいと思うので，復習がてらUnion-Find実装してみる
- 動きません
```py
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, i: int):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i: int, j: int):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return
        self.parent[root_i] = root_j

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        height = len(grid)
        width = len(grid[0])
        uf = UnionFind(height*width)

        for r in range(height):
            for c in range(width):
                if grid[r][c] == "0":
                    continue
                idx = r*height + c
                if r > 0 and grid[r-1][c] == "1":
                    uf.union(idx, idx-height)
                if c > 0 and grid[r][c-1] == "1":
                    uf.union(idx, idx-1)
        num_of_islands = 0
        for r in range(height):
            for c in range(width):
                idx = r*height + c
                if uf.find(idx) == idx and grid[r][c] == "1":
                    num_of_islands += 1
        return num_of_islands

```
- union-findの実装は思い出せたけど，`grid = [["1"],["1"]]`の時のidxの貼り方がわからない(`idx = r*height + c`だと`out of range`になる)ため挫折

- DFSを深堀する
- やっぱり入力は破壊するべきではない
- https://github.com/h1rosaka/arai60/pull/21/files#r2218803913
- https://github.com/olsen-blue/Arai60/pull/17/files#r1915967908
- 端判定
- https://github.com/ryosuketc/leetcode_arai60/pull/17/files#r2111434594
```py
if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
```
- https://github.com/olsen-blue/Arai60/pull/17/files#r1931571445
> dfs という単語が平均的なソフトウェアエンジニアにとって、最短で正確に認知負荷低く理解できる単語かどうか、微妙に感じました。 traverse という単語を使う方はいらっしゃると思います。 traverse_and_delete_one_island() はいかがでしょうか？
- 確かに，変数名にアルゴリズム名をつけるのって命名として重要度低い気がする
- これらを基に修正してみる
```py
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
```
- 端判定をmethodの中と外どちらに書くか問題
- https://github.com/sakupan102/arai60-practice/pull/18/files/fbbfb9c86dbb2e178ea2f14495b7ba36cb96d3c8#r1582241335
> この辺の気持ち、まあ、分かるんですけれどもね、しかし、visit_island は、メソッド内のとはいえメソッドなので、雑に扱っても構わないものにしておきたい気持ちがあるんです。
> つまり、将来、これをデバッグするのは自分ではない誰かと思われるので、これを条件に当てはまらないときに呼ぶと例外が投げられる、呼んだやつが悪い、というのはあまり好ましい態度ではないと思うわけです。
> そういうところも含めて読みやすいものにしたいので、上に条件を移したらという気持ちです。そうすると、読む方からすると、こういう条件を満たしている引数で呼んで欲しいのか、と分かるようになりますね。
- 確かにmethodの引数に対する責任はmethodが持つべきな気がするので同意
- 再帰のdepth limit問題
- https://github.com/tarinaihitori/leetcode/pull/17#discussion_r1839410598
- https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
- leetcodeの環境だと550000だった
- 確かに全部島で制約上サイズが300*300なので，最大90000になる
- こういうところに注意を向けていけるようになりたい
- https://github.com/ryosuketc/leetcode_arai60/blob/628964e10a6599197a896873f638be9764eee52c/200_number_of_islands/step2.py#L46
- これを回避するためにiterativeにstackを使うやり方
```py
def traverse_island(start_row, start_col):
    stack = [(start_row, start_col)]
    while stack:
        row, col = stack.pop()
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            continue
        if (row, col) in visited:
            continue
        if grid[row][col] == _SEA:
            continue
        visited.add((row, col))
        stack.append((row - 1, col))
        stack.append((row + 1, col))
        stack.append((row, col - 1))
        stack.append((row, col + 1))
```
- 視座が高い
- スレッドセーフの話
- https://github.com/colorbox/leetcode/pull/31/files#r1881098955
> これをメンバ変数で持つと、numIslands のスレッド並列性が失われます。失っては絶対にいけないわけではないですが、機能の複雑性とのバランスを考えたときに失うほどのものかとは思います。
- https://github.com/Ryotaro25/leetcode_first60/pull/20#discussion_r1687455278
> 絶対駄目というよりは状況次第ではあります。ただ、二回呼べない、スレッドセーフでない、などの制約があるならば注をつけて欲しいんですよね。
> コードを書くのってエンジニアリングです。要するに誰かに何かをしてあげたい気持ちの発露です。このコードはその単純さに比してわざわざ機能を落としているように見えます。例えば HTML パーサーがパースごとにオブジェクトを作り直さないといけない作りでもまあいいんですよ。ただ、これ連結成分を数えるだけなのにスレッドセーフではないというのは失っているものが大きいです。それで選択肢や帰結が見えているかが気になります。
> つまり、メンバ変数を使っては駄目という学習をして欲しくないです。「このコードを呼び出す人、使う人の気持になって考えて、自分はできることを行った。どこに行っても自分は恥じることがない。」といえるならばよいのです。
- なるほどな．確かにメンバ変数で持つとthreadが並列化されないな
- 今のコードはthread並列性があるか？
- `traverse_island`自体が`visited`を持っているから並列性あるね

ここまで2時間15分
ちょっと時間かかりすぎでコストが高くてよくない．
# step3

```py
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
            traverse_island(r+1, c)
            traverse_island(r, c-1)
            traverse_island(r, c+1)
        
        num_of_islands = 0
        for r in range(height):
            for c in range(width):
                location = (r, c)
                if location not in visited and grid[r][c] == ISLAND:
                    traverse_island(r, c)
                    num_of_islands += 1
        return num_of_islands
```
- 最後のlocation判定，notが抜けてWA
- 2時間27分
- 時間あったからいいけど，もっと短時間で納めないと今後がつらい
