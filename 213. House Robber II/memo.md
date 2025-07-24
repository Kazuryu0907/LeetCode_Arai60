# step1
House Robber 1との違いは家が循環して円形になっていること．
1では泥棒が各家の前に立って，取った場合と取らない場合をResponseすればよかった
条件を一つつけたらいけそう
- ~~ずらしたもの2個解く？~~
- 左右にpaddingさせる？
- 最初を取るか取らないかの1つがあれば，最後の要素と整合性取れそうだけど

=>これってただのDPじゃない？
一番最後にindex 0の要素入れて，集計するときは加算させないようにする？
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        dp = [0] * (len(nums) + 1)
        if len(nums) <= 2:
            return max(nums, default=0)
        dp[0] = nums[0]
        dp[1] = max(nums)
        arranged_nums = nums + [nums[0]]
        for i in range(2, len(arranged_nums)):
            dp[i] = max(dp[i - 1], dp[i - 2] + arranged_nums[i])
        print(dp)
        return dp[-2]

``` 
index 0が取られた，取られなかったかの情報があれば，いけそう
ここまで15分
0を取るか取らないかで変数を分けている手法
=> 考え方としてはあってたのね
https://github.com/hayashi-ay/leetcode/pull/50/files
これを参考に実装
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        max_amount_rob_first = [0] * len(nums)
        max_amount_rob_not_first = [0] * len(nums)

        max_amount_rob_first[0] = nums[0]
        max_amount_rob_first[1] = nums[0]
        max_amount_rob_not_first[1] = nums[1]

        for i in range(2, len(nums)):
            max_amount_rob_first[i] = max(max_amount_rob_first[i - 1], max_amount_rob_first[i - 2] + nums[i])
            max_amount_rob_not_first[i] = max(max_amount_rob_not_first[i - 1], max_amount_rob_not_first[i - 2] + nums[i])
        # 最初を取るので，最後は取らない
        return max(max_amount_rob_first[-2], max_amount_rob_not_first[-1])
```
これの時間計算量はdpのfor文よりO(n)，空間計算量はdp用の長さnの配列が2つよりO(n)

# step2
https://github.com/hayashi-ay/leetcode/pull/50/files#r1527186695
ここで指摘されてるように，空間計算量O(1)は`i-2`までの値しか使わないので，配列から変数に変えれば使える．

DPの緩和の処理が二回繰り返されているので，DRY原則に抵触している．
与えられた配列の0番目を固定でとる形にすれば一般化できる．
https://github.com/hayashi-ay/leetcode/blob/97118c66c80db71aadc46b1a32fb7b19ca526486/213.%20House%20Robber%20II.md?plain=1#L63
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        return max(self.max_amount_rob_first_house(nums[:-1]), self.max_amount_rob_first_house(nums[1:]))
        
    def max_amount_rob_first_house(self, nums: List[int]):
        max_amount = [0] * len(nums)
        max_amount[0] = nums[0]
        max_amount[1] = max(nums[:2])
        for i in range(2, len(nums)):
            max_amount[i] = max(max_amount[i - 1], max_amount[i - 2] + nums[i])
        return max_amount[-1] 
```
https://github.com/ryosuketc/leetcode_arai60/pull/49/files#r2217263665
ここで，Listのsliceはコピーされると指摘されている．調べてみると
https://docs.python.org/3/tutorial/datastructures.html#more-on-lists:~:text=Return%20a%20shallow%20copy%20of%20the%20list.%20Similar%20to%20a%5B%3A%5D.
ここより
>list.copy()
>Return a shallow copy of the list. Similar to a[:].

と確かにかかれている．知らなかった．Rustみたいに&参照してくれたらいいのに．
これを修正したものがこれ
ここまで60分
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        return max(self.max_amount_rob_start_house(nums, 0, len(nums) - 1), self.max_amount_rob_start_house(nums, 1, len(nums)))
        
    def max_amount_rob_start_house(self, nums: List[int], start: int, end: int):
        len_nums = end - start
        max_amount = [0] * len_nums
        max_amount[0] = nums[start]
        max_amount[1] = max(nums[start:start + 2])
        for i in range(2, len_nums):
            max_amount[i] = max(max_amount[i - 1], max_amount[i - 2] + nums[start + i])
        return max_amount[-1]
```
でも制約が`1 <= nums.length <= 100`だから，費用対効果的にsliceのほうがいいかも．
step2はsliceのほうで提出

# step3
特に引っかかることなく終了
