# step1
[前回](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)の問題は最小値を求める問題だが、
今回は任意のtargetをO(log n)で求める必要がある。
制約は`1 <= len(nums) <= 5000`
targetが崖を越えているか、越えていないかの二択が存在しそう
これの条件分けでやってみればいける？
不変条件として、`left <= mid <= right`とする。
例で考えてみる
`nums = [4,5,6,7,0,1,2], target = 0`の時
`nums[mid] = 7`崖を越える前で、`nums[mid] > target`なので右に範囲を狭めればいいことがわかる。

`nums=[FFFFTTT]`にしたい
```py
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # Targetがnums[-1]にある時はTrueとする
            isTargetOverCliff = target <= nums[-1]
            isMidOverCliff = nums[mid] < nums[-1]
            if isTargetOverCliff == isMidOverCliff:
                if nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid
            else:
                if nums[mid] > target:
                    left = mid + 1
                else:
                    right = mid
        # 一致したらindexを返す
        if nums[left] == target:
            return left
        else:
            return -1
```
targetとmidそれぞれが崖を越えているかどうかでどっちに範囲を狭めるべきか変わる

一応ACした
時間計算量: O(log n)
空間計算量: O(1)

1. 用いた区間の種類に対し、適切な初期値を、理由を理解したうえで、設定できるか？
初期値は解の範囲である[0, len(nums) - 1]
2. 用いた区間の種類に対し、適切なループ不変条件を、理由を理解したうえで、設定できるか？
- ループ不変条件
  - 0 <= left <= mid <= right <= len(nums) - 1
- 停止性
  - right == left
  - midで切り上げていて左寄りに、left = mid + 1で一度の探索で必ず範囲が1狭まることが保証される。
1. 用いた区間の種類に対し、範囲を狭めるためのロジックを、理由を理解したうえで、適切に記述できるか？
- [3, 4, 0, 1, 2]でnums[mid] = 0, target = 1なら、左には存在しないので、右に範囲を狭める必要がある。
- [2, 3, 4, 0, 1]でnums[mid] = 4, target = 1なら、左には存在しないので、右に範囲を狭める必要がある。
- このように、最小値で配列を分けた時(minは右の部分集合になるとする)targetとmidが同じ集合に属していたら、通常の二分探索に、そうでないなら、同じ部分集合になるように範囲を狭める必要がある。
- 
# step2
人の見てみる
- https://github.com/hayashi-ay/leetcode/pull/49/files
binary searchを一回行い、崖のindexを見つけてから、その範囲に対してbinary searchを行うもの
確かにこれはシンプルでわかりやすいと思う。
- https://github.com/olsen-blue/Arai60/blob/05f634b61d0878da6a042891a436ad5f6cb84518/33.%20Search%20in%20Rotated%20Sorted%20Array.md?plain=1#L135
>```py
>class Solution:
>    def search(self, nums: List[int], target: int) -> int:
>        def priority(num) -> int:
>            return (num <= nums[-1], target <= num)
>        index = bisect_left(nums, priority(target), key=priority)
>        if nums[index] != target:
>            return -1
>        return index
>```
でた　つよつよ系だ
bisect_leftのkey functionがよくわらかなかったけど、内部でbinary searchを行う際に比較する値を出力するものか
(https://docs.python.org/ja/3.13/glossary.html#term-key-function)
tuple(A, B)の比較は、A->Bという順番になる。
>   - タプル(A,B)は、BよりもA優先でソートされることを利用している。
>   - Aが1次序列、Bが2次序列。
>   - A : 崖の前/後が F/T つまり 0/1 で表されている。この時点で、この後Bでいくら頑張っても挽回できない絶対的な格付け序列が作られてしまうイメージ。
なるほどな、崖がある配列のindexを担保したまま、targetをbisect_leftできるようにしているのか
わかれば面白い。初見は珍紛漢紛すぎるけど
でもこれ、keyで全てのnumsに対してpriorityを実行してるはずだから、O(n + log n)になりそうじゃない...?

一回こっちで書いてみる
```py
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def priority(num: int) -> tuple:
            return (num <= nums[-1], num >= target)
        index = bisect_left(nums, priority(target), key=priority)
        if nums[index] == target:
            return index
        else:
            return -1
```

# step3
せっかくなのでbisectになれるためにもsmartな方でやってみる
```py
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def priority(num: int) -> tuple:
            # (A, B)
            # A: 崖の前か後か
            # B: 部分集合の中で[FFFTTT]を作る
            return (num <= nums[-1], num >= target)
        index = bisect_left(nums, priority(target), key=priority)
        if nums[index] == target:
            return index
        else:
            return -1
```
なんか色々応用できそうで面白い