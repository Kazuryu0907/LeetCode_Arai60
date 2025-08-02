# step1
- numsが与えられ，増加し続けてるsubspaceの長さを返す
- 普通にdpとして配列n番目までの最長のsubspaceの長さとpre_numsを格納していって，増加していたら1足す，してなかったら足さないでいい？
- 現状の数字が増加中なのか，今までの中で最長なのか判断できない．
- dpの次元を増やして，増加flagを導入する？<=増加中かどうかのflagを用意したらいけそう
- 実装してみる　ここまで4分

- めっちゃ勘違いしてます
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        increase_count = 0
        pre_num = None
        max_subspace_length = 0
        for i, n in enumerate(nums):
            if pre_num is None:
                pre_num = n
                continue
            if n > pre_num:
                increase_count += 1
                max_subspace_length = max(max_subspace_length, increase_count) 
            else:
                increase_count = 0

            pre_num = n
        return max_subspace_length

```

- subspaceって勝手に配列の連続した要素だと思ってた
- 普通にorderを保った部分空間の意味なのか
- 考えなおします
- 結局nums[i]を取るか取らないかで場合分け出来そう
- 問題はどうやって緩和していくか
- 取った時，subspaceが成り立つには，iまで取った時の最大値の情報があればいけそうだけど，これ以上はわからない
- カンニングします
- https://github.com/olsen-blue/Arai60/pull/31/files
```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        length_at_index = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(0, i):
                if nums[j] < nums[i]:
                    length_at_index[i] = max(length_at_index[i], length_at_index[j] + 1)
        return max(length_at_index)
```
> numsリストのある位置インデックスを i として、iより左のインデックスを j とする。
> nums[j] < nums[i]だったら、jの位置の値に+1できる。その中で最大になるものをiの位置の値として採用すればよい。
- そもそもLISがわからん
- https://qiita.com/kei_tnk/items/ba92ef52c2e2ca57886d
- `length_at_index[i]`はLISの最後の数値を`nums[i]`とする縛りを追加した場合のLISの長さ
- 普通に左から走査して，`nums[j]とnums[i]`を比較して，subspaceの長さが増えるかやってるだけか．
<!-- - 納得できないので数字で見てみる -->
<!-- - `nums = [0,1,0,3,2,3]`として
- `i = 1`のとき`j = {0}`
- `dp[i] = max(dp[i], )` -->
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        max_lengths = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    max_lengths[i] = max(max_lengths[i], max_lengths[j] + 1)
        return max(max_lengths)
```
- これ，`max_lengths[i]`が`max_lengths[j] + 1`よりでかくなるパターンあるの？
- [0,1,0,3]のとき，nums[j] < nums[3]だけど，途中でリセットされるから小さくなっちゃうのか
- 理解理解
- 空間計算量はO(n)
- 時間計算量はO(n^2)


# step2
- https://github.com/olsen-blue/Arai60/pull/31/files
- どうやら二分探索でも解けるらしい
- こっちのほうが直感的でわかりやすい気がする．
- どんどん配列を上書きしていって，伸ばしていく感覚．
- 面白いな
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        lis = []  
        for n in nums:
            index = bisect.bisect_left(lis, n)
            if index == len(lis):
                lis.append(n)
            else:
                lis[index] = n
        return len(lis)
```
- こっちだと空間計算量: O(n)
- 時間計算量: O(n log(n))まで減らせるのか
- 実際1800msから29msまで速くなった
- こういうのはおもろいんだよな～～～
- ちょっとおなかいっぱい
- https://github.com/olsen-blue/Arai60/pull/31/files#r1958585512
- 確かに`lis`の命名がちゃんとできてないかも
- `lis_at_min_num`とか？

# step3
- 二分探索が気に入ったのでこっちで書いてみる
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        lis_at_min_num = []
        for n in nums:
            i = bisect.bisect_left(lis_at_min_num, n)
            if i == len(lis_at_min_num):
                lis_at_min_num.append(n)
            else:
                lis_at_min_num[i] = n
        return len(lis_at_min_num)
```
- 一番使う変数名が長いのはよろしくないので，コメントで補うことにする
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # lis[i]はlisの長さがiになるときの末尾の最小値
        lis = []
        for n in nums:
            i = bisect.bisect_left(lis, n)
            if i == len(lis):
                lis.append(n)
            else:
                lis[i] = n
        return len(lis)
```
- 特に迷わず行けた
- 一応dpでも理解しているか書いてみる
```py
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # max_lengths[i]はiまでのsubspaceで最大のlis長
        max_lengths = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                # lisが伸びる可能性があるとき
                if nums[j] < nums[i]:
                    max_lengths[i] = max(max_lengths[i], max_lengths[j] + 1)
        return max(max_lengths)
```
- 感覚として，天下り的に理解はした感じ．
- 問題やる前に戻って，自分で一人で解けるかって言われたら無理だな
- 普通に全体で1時間40分かかった
- 知らないalgoだとこうなりがちなので，もうちょっと負担を減らしたい
