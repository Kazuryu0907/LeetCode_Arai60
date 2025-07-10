
# step1
`nums[i] > 0`だから，貪欲法でいけそうじゃない？
左から見ていって，二つを比べる．左を取るなら，次は右とその右を比べるし，右を取るならその右二つとる．
つまり，取ったindexに対して，index+1, index+2を比較していけばいい．
時間計算量はO(N)になるし，空間計算量もoutputだけでいいのでO(1)になるはず．

ここまで5分.
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        i = 0
        num_sum = 0
        while i+1 < len(nums):
            better_num = max(nums[i], nums[i+1])
            i = nums.index(better_num) + 1
            print(i - 1)
            num_sum += better_num
        return num_sum
```
こうしようとしたけど，indexでO(N)が発生して，O(N^2)になる.
でも`nums.length <= 100`なので，N^2なら全然ありかも

隣り合わないnumを取っていって最大値を求めるので，偶数indexと奇数indexのものをそれぞれ足していって，でっかいほうを取ればいいじゃん．
=> [2, 1, 1, 2]の時に対応できないじゃん．
隣り合わないっていう条件を頭でうまく定式化できていない

ほかの人のコード見る

- https://github.com/hayashi-ay/leetcode/pull/48/files
DPか　部分構造最適性があるもんな
`i`を取る(`nums[i-2]+nums[i]`)と`i`を取らない(`nums[i-1]`)で緩和していけばいいのか．
見ずに書いてみる．
初期化処理(dp[0],dp[1])の取り方で躓いた．ここはハードコーディングするしかないのか．
len(nums)が2以下だとindex out of rangeになるわ．そろそろこれぐらいはコードを見てわかるようにしたい．
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums)
        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        return dp[-1]
```

# step2
- https://github.com/Mike0121/LeetCode/pull/47/files
numsが空だった時の挙動は確かにわからない
- https://docs.python.org/3/library/functions.html#func-memoryview
> If the iterable is empty and default is not provided, a ValueError is raised.
default引数与えないとValueErrorが出るらしい　知らなかったてっきり0でも返ってくると思っていた．

- 配列を用いる場合
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        # i番目まで用いたときの最大値
        dp = [0 for _ in range(len(nums))]
        dp[0] = nums[0]
        dp[1] = max(nums[:2])
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        return dp[-1]
```
- https://github.com/Mike0121/LeetCode/pull/47/files
必要なのは二個前までのデータなので，O(1)にもできる
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        one_previous_max = 0
        two_previous_max = 0
        for num in nums:
            target_max = max(two_previous_max + num, one_previous_max)
            two_previous_max = one_previous_max
            one_previous_max = target_max
        return target_max
```
- https://github.com/tokuhirat/LeetCode/pull/35/files
再帰でもできる
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        @functools.lru_cache
        def max_gain_from_index(i: int) -> int:
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[:2])
            return max(max_gain_from_index(i - 1), max_gain_from_index(i - 2) + nums[i])

        return max_gain_from_index(len(nums) - 1)
```
この時，lru_cacheのmaxsizeはデフォルト128になる(https://docs.python.org/ja/3.13/library/functools.html)．`nums.length <= 100`なので，これより大きくはなるけど，空間計算量はO(N)になる．
cacheとlru_cacheの違いは，cacheはlru_cacheのmaxsizeが無限大版．別にN大きくないし，差ないかも
個人的にはdpで配列を持たせるやり方がシンプルでわかりやすいかな.

# step3
```py
class solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        dp = [0 for _ in range(len(nums))]
        dp[0] = nums[0]
        dp[1] = max(nums[:2])
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        return dp[-1]

```
