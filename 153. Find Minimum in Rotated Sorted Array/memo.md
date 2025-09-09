# step1
円順列になっているsortedの配列の最小値をO(log n)でとるもの
O(log n)ってことはbinary searchなんだろうか
ヒープとかbinary treeは配列全体をinsertするのにO(n)かかるし
昔、binary searchは左は条件を満たさないが、右が条件を満たす場所を探すアルゴリズムだと抽象化できると本で読んだ気がする。
といっても解法出てこないので人のを参照する
- https://github.com/Kaichi-Irie/leetcode-python/pull/7
- https://github.com/ryosuketc/leetcode_arai60/pull/31/files
普通に考え方は間違ってなさそう。条件としてmiddleと比べた値の大小を与えればいける
```py
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # 崖を越える前なら
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid
        return nums[left]
```

# step2
- https://github.com/olsen-blue/Arai60/pull/42/files
>   - 昨日までの引き継ぎによると、どこかに最小値が存在しているらしい、探索対象区間[left, right]に対して、今日のmiddleの調査結果を加えて明日に向けて引き継ぎをする。
>   - middle = (left + right) // 2 が崖を越えた後か？越える前か？を今日調査する
崖を越えたあとっていう考え方だとわかりやすいかも。
>       - 崖越えた後なら、middleは最小値になりうるし、middle - 1 以降の左側にも最小値が存在し得るので、[left, middle]を探索範囲にして引き継ぐ。
>       - 崖越える前なら、 middleは最小値にならないが、middle + 1 以降の右側に最小値が存在し得るので、[middle + 1, right] にして引き継ぐ。
なるほど。越えたあとだと、midを含む範囲で再捜査しないといけないけど、越える前ならmidが最小値になり得ないからmidはいらないのか。
確かに[FFFFTTT]ではじめのTを探す場合、`mid=F`なら、midを含めた左側は必要ないね
つまり、(更新前の)leftはminにならないことが保証された値で、rightはminになる可能性があることが保証された値になるのか
binary search、ここら辺のイメージというか、+1するしないとかがわからなくなるから苦手。
ちゃんとなんでそうなるのか理解したらいけそう
- https://github.com/hroc135/leetcode/pull/40/files#r1959934686
- binary searchの停止性に関する言及
>5. 用いた区間の種類に対し、適切なループ不変条件を、理由を理解したうえで、設定できるか？
    - 終了条件はleft==right==(一番左のtrueのインデックス)
    - なので不変条件はleft<right
    - [left,right]の区間に最小値が存在するので、
    nums[left] >= (最小値), (最小値) <= nums[right]
こうやって理解していけばいいのか
自分の言葉で書いてみる
6. 用いた区間の種類に対し、範囲を狭めるためのロジックを、理由を理解したうえで、適切に記述できるか？
- 閉空間[left, right] = [0, len(nums)-1]を想定
- mid = (left + right) // 2(切り捨て)として
- nums[mid] > nums[-1]のとき(崖を越える前)
  - midはFなので、右側に狭めるためにleft = mid + 1にする(停止性のため、+1になると認識(mid=Fなので、+1にしても問題ない))
- それ以外の時(崖を越えた後)
  - midはTなので、左側に狭めるためにright = midにする
- 停止性
  - left = mid + 1とmid = (left + right) // 2(切り捨て)により、一回の更新で確実に範囲が1以上狭くなる
    - [FT]の時mid = Fで、left=Tになる
    - [TT]の時mid = Tで、right=T(左)になる
閉区間ってちゃんと考えたことないので学習する
- 閉区間: 区切りを含む場合。[]を使う
- 開区間: 区切りを含まない場合。()を使う
- 半開区間: 片方含んで片方含まない場合。

>    - Q. 2で割る処理がありますがこれは切り捨てでも切り上げでも構わないのでしょうか
        - 構う。切り捨てならmiddle<rightが成り立つことから停止性を保証していたが、
        切り上げだとleft=0,right=1の時にmiddle=1となり、right<-middleへの更新によって区間が狭まらず、無限ループに陥る

- https://discord.com/channels/1084280443945353267/1196498607977799853/1269532028819476562
上の質問ここにあった。
自分でもやってみます
1. 二分探索を、 [false, false, false, ..., false, true, true, true, ..., true] と並んだ配列があったとき、 false と true の境界の位置を求める問題、または一番左の true の位置を求める問題と捉えているか？
- これはスタート時にできてたね
2. 位置を求めるにあたり、答えが含まれる範囲を狭めていく問題と捉えているか？
- これも大丈夫
3. 範囲を考えるにあたり、閉区間・開区間・半開区間の違いを理解できているか？
- 上で調べた
4. 用いた区間の種類に対し、適切な初期値を、理由を理解したうえで、設定できるか？
- 用いたのは閉区間。適切な初期値は閉区間なので`[0, len(nums) - 1]`。indexがout of rangeにならない初期値になっている。
- 半開区間だと`[0, len(nums))`になる。こっちだとmid計算するときにout of rangeになる可能性があるから、ちょっと面倒くさいかも
5. 用いた区間の種類に対し、適切なループ不変条件を、理由を理解したうえで、設定できるか？
- ループ不変条件
  - `0 <= left <= mid <= right <= len(nums) - 1`
  - `nums[left] >= 最小値, 最小値 <= nums[right]`([left, right]に最小値が存在するから)
- 停止条件
  - right == left(範囲が１つになったら(最小値が確定したら))
6. 用いた区間の種類に対し、範囲を狭めるためのロジックを、理由を理解したうえで、適切に記述できるか？
- 上で書いた。

理解が深まった気がする。
- https://github.com/hroc135/leetcode/blob/869aafe182f352772ba2f4f22ff2c93b7dba599e/153FindMinimumInRotatedSortedArray.md?plain=1#L107
いろんなケースを考えていられる
> - numsが空
現状`right = -1`になるから壊れてしまう。早期returnする必要あり
> - 要素に重複あり
[1,1,1,0,1,1]とかだと大小の保証ができなくてうまく動かない。
>         - `case nums[middle] == nums[right]:`に入ってしまう
        - [2,2,2,0,0,0,1,1,1]の場合、左端、右端、ランダムな0のうちどれを返すかで変わってくる
        - 左端を返したいなら、`case nums[middle] < nums[right]:`の<を<=に変える
        - 右端を返したいなら、[2,0,0,0,1]を[false,false,false,true,true]と捉える問題へとだいぶ様変わりする。
        middleが右に寄るように取る(切り上げ)などの工夫が必要そう
確かに。最小値がたくさんある可能性もあるのか
```py
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # 崖を越える前
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid
        return nums[left]
```

# step3
ちゃんと理解してからだと、+1とか切り捨てとか、そういうところの必然性がわかってミスしない
```py
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # 崖を越える前
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid
        return nums[left]
```