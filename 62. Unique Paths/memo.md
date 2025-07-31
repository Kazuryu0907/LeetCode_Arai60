# step1
m x nのマスがあって，ロボットは左上(grid[0][0])にいる．
ロボットは右下(grid[-1][-1])に向かい，↓か→にしか動けない．
このとき，ゴールに到達できるパスの数をreturnする．

- なんか高校受験の時の数え上げでこんなのなかった？
- 数え上げというよりかは，障害物もないので計算すれば終わりそう．
- DPでやるとしたら，その地点grid[i][j]に到達可能なすべてのPathを緩和していく感じ？
- DPの練習なのでこっちでやってみる

- 移動方向の制約から，grid[0][:]とgrid[:][0]へのPathは1ということがわかる．
- gird[i][j]に貰うDPとしてgrid[i - 1][j] と grid[i][j - 1]からの2ルートを足せば全ルート網羅できそう
- 実装してみる

とりあえずAccepted
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = [[0 for _ in range(n)] for _ in range(m)]
        paths[0] = [1 for _ in range(n)]
        for i in range(m):
            paths[i][0] = 1
        for i in range(1, m):
            for j in range(1, n):
                paths[i][j] = paths[i-1][j] + paths[i][j-1]
        return paths[-1][-1]
```
- listのindexのスペース([i-1])は，pepでどちらでもいいという話を見かけたので()，こちらを採用
- 空間計算量：O(mn)
- 時間計算量：O(mn)
ここまで20分ぐらい

# step2
```py
paths[0] = [1 for _ in range(n)]
paths[:][0] = [1 for _ in range(m)]
```
これで
```[[1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]```
こうなるのなぞ
DP配列の初期化処理を何とかしたい
- https://github.com/olsen-blue/Arai60/pull/33/files
```py
num_of_paths = [[0] * n for _ in range(m)]
```
`num_of_paths`のほうが一目で何を保存しているのかわかりやすい．
`[0] * n`は0がimmutableだからshallow copyにならずに済むね
- 初期化をforループに組み込んだほうがわかりやすそう
- https://github.com/hroc135/leetcode/pull/31/files#r1898180689
> - 今回はleetcodeのテストケースを走らせる前に自作テストケースを頭の中で走らせることに
>    - 以前川中さんが「テストケースは機械的に生成するといい」とおっしゃっていたので、以下を試す
>    - (m,n) = (0,0), (0,1), (1,0), (1,1), (1,2), (2,1), (2,2)
>    - 2つほど境界条件関連のバグが見つかった。
>    脳内シミュレーションの練習にもなるので習慣化しよう
これは今の自分に大切かもしれない．こういうイメージ力をつけていきたい．特にEdgeケース．
## 組み合わせを使う方法
`(m + n - 2)! // (m - 1)!(n - 1)!`で求めれるらしい<=そもそもこれがわからん．
- https://xn--48s96ub7b0z5f.net/saitankeiro/
- ここに書いてた．`全体の矢印の数!/(ゴールまでのx)!(ゴールまでのy)!`ってことね．
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        def factorial(n: int) -> int:
            if n == 0:
                return 1
            return n * factorial(n-1)
        return factorial(m+n-2) // (factorial(m-1) * factorial(n-1))
```
- はじめ`if n == 1`にしており，初期条件を満たせずにdepth落ちした．
# 再帰でDPを使う方法
- https://github.com/nittoco/leetcode/pull/26/files#r1677136040
壁に突き当たるまで小人を生成していって，それを吸収していくイメージか
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @cache
        def get_num_paths(m: int, n: int) -> int:
            if m == 0 or n == 0:
                return 1
            return get_num_paths(m - 1, n) + get_num_paths(m, n - 1)
        return get_num_paths(m - 1, n - 1)
``` 
- `if m * n == 0`って書きたかったけど，意味合いが伝わりにくそうだったので却下
- cacheされてるから，空間計算量は変わらずO(mn)のはず
- https://github.com/olsen-blue/Arai60/pull/33/files#r1966730122
>これ、計算量の見積もりできてますか。
>最終的にすべて return 1 になっていて、それが木のように足されていますね。だから、計算量は (n+m)Cm になるはずです。
- n == mのとき，高さn+1の完全二分木になるので，葉の数は2^nになるはず．n != mのときはパスカルの3角形をいい感じに使えそう．
- そもそも再帰のたどる道がパスの道筋と等しい(厳密には同じルートを何度か通る)から，O((n+m)Cm)になる．

## 一次元配をを使ってDPする方法
- https://github.com/olsen-blue/Arai60/pull/33/files#r1979289987https://github.com/olsen-blue/Arai60/pull/33/files#r1979289987
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        num_paths = [0] * n
        num_paths[0] = 1
        for _ in range(m):
            for i in range(1, n):
                num_paths[i] += num_paths[i-1]
        return num_paths[-1]
```
- 確かに対称性があるから，一次元でも行けるのか．
- 空間計算量がO(n)に減った．minを取って，mとnをswapしてやる方法もありそう．この場合O(min(n, m))
- イメージとしては，列で計算してから，ゴールに向かって行でたたんでいく感じか
# step3

- シンプルDP
```py
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
```

- 空間計算量O(min(n, m))のやつ
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # n < mにする
        if m < n:
            m, n = n, m
        num_paths = [0] * n
        num_paths[0] = 1
        for _ in range(m):
            for i in range(1, n):
                num_paths[i] += num_paths[i-1]
        return num_paths[-1]
```

- nCrのやつ
```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        def factorial(n: int) -> int:
            if n == 0:
                return 1
            return n * factorial(n-1)
        return factorial(n+m-2) // (factorial(n-1) * factorial(m-1))
```
