# step1
- またロボットは左上(grid[0][0])
- ロボットはゴール(右下grid[-1][-1])に動こうとする，障害物があるといけない
- grid[i][j]のパス数は，grid[i-1][j]とgrid[i][j-1]の和で，それぞれに障害物がないときとして計算できそう．
- これnCrで計算はできなさそう
- とりあえずDPで実装してみる

```py
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        # ゴールが塞がれてたらnum_pathsは0
        if obstacleGrid[-1][-1] == 1:
            return 0
        num_row = len(obstacleGrid)
        num_col = len(obstacleGrid[0])
        num_paths = [[0] * num_col for _ in range(num_row)]
        for i in range(num_row):
            for j in range(num_col):
                if i == 0 or j == 0:
                    num_paths[i][j] = 1
                    continue
                if obstacleGrid[i-1][j] == 0:
                    num_paths[i][j] += num_paths[i-1][j]
                if obstacleGrid[i][j-1] == 0:
                    num_paths[i][j] += num_paths[i][j-1]
        return num_paths[-1][-1]

```
- 入力が[[1, 0]]のとき，死んだ
- スタートとゴール，どちらかが塞がれてたら0か
- 入力が[[0,1,0,0]]の時も死んだ
- 障害物があるから，`if i == 0 or j == 0:`の条件式が成立しないのか
- ちょっと例外処理が多すぎる
- 根本的にやり方を考えたほうがよさそう
- 前回と違うところ
- 前回は外周が確定で1だったのに対し，今回は0のパターンもある
- forを1スタートで回したいけど，壁沿いの初期化の処理が記述量多くなりそう
- とりあえずAcceptedした
```py
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
```
ここまで20分
空間計算量：O(nm)
時間計算量：O(mn)

# step2
- https://github.com/olsen-blue/Arai60/pull/34/files#r2038733249
- そもそも，配列は0で初期化されているから，breakしたらいいのか
```py
for r in range(num_rows):
    if obstacleGrid[r][0] == 1:
        break
    num_of_paths[r][0] = 1
for c in range(num_cols):
    if obstacleGrid[0][c] == 1:
        break
```
>  遷移元の位置に障害物があるかどうかを if で条件分岐するのは大変そうなので、やりたくない。注目しているグリッド座標が障害物かどうかで if 分岐したい。
- この考え方はなかったな．ifで条件分岐をやりたくないという発想がまずなかった．確かに書いててとても煩雑だった．
- いわゆる貰うDPを意識しすぎて，solutionがこれに凝り固まってた気がする．
- https://github.com/philip82148/leetcode-swejp/pull/10/files
>たぶん、これは目的から考えたらいいと思います。
>最終目的は「仕事の場に出て問題なく一緒に仕事ができること」です。
>コードが絡む場面は大きく2つあって、書くところと読むところです。
>書くところは、「ある程度の時間で書ける。動くだけではなく、書いたコードが変更しやすく周りの人に分かりやすくしておくなどの基準で。」で、読むところは、「色々な書き方をすんなり読めるようにしておく。」でしょう。
>一回目書いて他の人のコードを読むと「ボードゲームでいえばルール、全体像が分かった」状態になります。では、仮にこの知識、現在の視点があったら、はじめに自分はどう振る舞っていたであろうか、どう振る舞っていたらよかったか、それを二回目三回目あたりで考えてみるとよいだろうと思っています。
>やってみた結果、一切改善点が見つからないならば、そもそも、不要な練習なのかもしれません。
- https://google.github.io/styleguide/go/decisions#variable-names
>The general rule of thumb is that the length of a name should be proportional to the size of its scope and inversely proportional to the number of times that it is used within that scope. A variable created at file scope may require multiple words, whereas a variable scoped to a single inner block may be a single word or even just a character or two, to keep the code clear and avoid extraneous information.
変数名の話．今回はスコープがだいぶ限られてるし，`i, j`よりも`r, c`で書いたほうが直感でわかりやすいのか．
- https://github.com/hayashi-ay/leetcode/blob/99583536e1b149d0db2da4985b87a2828f379e8d/63.%20Unique%20Paths%20II.md
- `==1`のマジックナンバーはやめたほうがいいね．
- `height, width = len(obstacleGrid), len(obstacleGrid[0])`なんか一行にまとめるのruffのlinterで怒られた記憶があってやってこなかったけど，むしろこっちのほうが見やすいと思う

## 解法1: 2D-DP
- 初期化処理にbreakをつけて変数を減らした
- `obstacleGrid[r][c]`に`OBSTACLE`があったらはじくように変更した．
```py
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

```
- これ，rowとcol初期化処理まとめたいなぁ
- https://github.com/hayashi-ay/leetcode/pull/44/files
- 1DPのやり方もある
```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        OBSTACLE = 1

        height = len(obstacleGrid)
        width = len(obstacleGrid[0])

        num_ways = [0] * width
        for row in range(height):
            for col in range(width):
                if obstacleGrid[row][col] == OBSTACLE:
                    num_ways[col] = 0
                    continue
                if row == 0 and col == 0:
                    num_ways[0] = 1
                    continue
                if col > 0:
                    num_ways[col] += num_ways[col - 1]
        return num_ways[-1]
```
- 空間計算量がO(n)に減る
- 元のコードでも，`m, n <= 100`なので空間計算量が問題になることはないけど
- やっぱり1D-DPはイメージしにくい．やっていることは何となく理解できるけど，コードと問題のイメージにもう1 layer挟まないといけない．

- 再帰でもやろうとしたが，壁沿いの初期化処理が，毎回壁の出現位置を見に行かないといけない気がした．これはあまりにもやりたくない．のでやらない

# step3
- forループの範囲ミスでWA
- 何のための初期化処理かちゃんとかみ砕けてない
- 動きません
```py
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        OBSTACLE = 1
        if obstacleGrid[0][0] == OBSTACLE or obstacleGrid[-1][-1] == OBSTACLE:
            return 0
        num_rows, num_cols = len(obstacleGrid), len(obstacleGrid[0])
        num_paths = [[0] * num_cols for _ in range(num_rows)]
        for r in range(num_rows):
            if obstacleGrid[r][0] == OBSTACLE:
                break
            num_paths[r][0] = 1
        for c in range(num_cols):
            if obstacleGrid[0][c] == OBSTACLE:
                break
            num_paths[0][c] = 1
        
        for r in range(num_rows):
            for c in range(num_cols):
                if obstacleGrid[r][c] == OBSTACLE:
                    continue
                num_paths[r][c] = num_paths[r-1][c] + num_paths[r][c-1]
        return num_paths[-1][-1]

```

- アンダーバーに対するtypoが多い
- ちゃんと指のホームポジションを復習したい
- Vimを返してくれ
```py
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        OBSTACLE = 1
        if obstacleGrid[0][0] == OBSTACLE or obstacleGrid[-1][-1] == OBSTACLE:
            return 0
        num_rows, num_cols = len(obstacleGrid), len(obstacleGrid[0])
        num_paths = [[0] * num_cols for _ in range(num_rows)]
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
```
