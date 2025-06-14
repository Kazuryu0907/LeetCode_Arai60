# 560. Subarray Sum Equals K

# step1
## 方針

intの配列の`nums`とintの`k`が与えられる．
合計が`k`になるsubArrayの総数を答える．
subarrayは連続し，0じゃない
contiguous => 連続した

kがnumsに所属してたら[k]としてカウントかつnumsからpopできる．
二重ループで回して，iからkまで足して，kになったら`out += 1`して，超えたら`break`する．これだと計算量O(n^2)．空間量はint二つでいいのでO(1)．

↓WAになります
```py
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        out = 0
        for i, n in enumerate(nums):
            # nの初期値
            n_sum = n
            if n_sum == k:
                out += 1
                continue
            for j in range(i+1, len(nums)):
                n_sum += nums[j]
                print(n_sum)
                if n_sum == k:
                    out += 1
                if n_sum >= k:
                    break
        return out
```
入力が負を取ることを考えていなかった．こういう想像力が足りない．
本当にO(n^2)になってしまう. 

ここまで15分

答え見ます．
- https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.bp0g0ai41eln
> 「鉄道があって、各駅間ごとの標高差が与えられます。標高差が ちょうど K であるようなすべての駅の組み合わせを列挙してください。」
>
イメージする．
k = 2, 標高差=[1, 1, 1]
元の問題との差異が見えてこない...
- https://github.com/ryosuketc/leetcode_arai60/pull/16/files#r2109771699

> 標高差が ABCDE の5つの駅があって、それぞれの標高差がすべて 1 m です。([1, 1, 1, 1])
高さが 3 m 違う駅の区間を見つけてください。
A の標高を 1000 m としましょう。電車に乗るときに、標高とその駅を書き込んだ手帳を用意します。
1000 m A
B 駅につきます。はて、ここの標高は 1001 m である。ということは、標高が 998 m の駅があればいいんだな。うーん。ないな。じゃあ、B 駅の情報を手帳に書き込むか。
1000 m A
1001 m B
C 駅につきます。はて、ここの標高は 1002 m である。ということは、標高が 999 m の駅があればいいんだな。うーん。ないな。じゃあ、C 駅の情報を手帳に書き込むか。
D 駅につきます。はて、ここの標高は 1003 m である。ということは、標高が 1000 m の駅があればいいんだな。A 駅か。じゃあ、A と D は条件を満たすな。じゃあ、D 駅の情報を手帳に書き込むか。

そうか標高差って行っているからdiffか．
numsの左から走査していって，差がkになる標高を検索．(走査している標高が今一番高い．高さ-kの標高を探す．)
~~**問題では，subarrayの具体的な値は聞かれていない．**~~　さして問題ではない．(indexとれるし)
つまり，先がわからない配列の右へ足していくのではなく，端が決まっている左から走査する？
numsを差として解釈することで，右へ足し合わせるのではなく， nums[i]でkになる山を左から探す．
コードに起こす(↓動きません)
```py
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        tall_set = set()
        tall = 0 # 標高
        n_sub_array = 0
        for n in nums:
            comp = tall - k
            print(comp, tall_set)
            if comp in tall_set:
                n_sub_array += 1
            tall_set.add(tall)
            tall += n 
        return n_sub_array
```

うまく言語化できなくてもどかしい．
あくまで各駅の差なので，forループはn+1回回さないと行けない.
最初に絶対高さを作って，forループで回せばいい．
```py
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # num_to_k: Dict[int, int] = {}
        tall_set = set()
        talls = [0]
        tall = 0 # 標高
        for n in nums:
            tall += n
            talls.append(tall)
        # len(talls) == len(nums) + 1
        n_sub_array = 0
        for tall in talls:
            comp = tall - k
            if comp in tall_set:
                n_sub_array += 1
            tall_set.add(tall)
        return n_sub_array

```
以下でWA
> nums = [1, -1, 0]
> k = 0
> output = 2
> expected = 3

~~なんでexpected = 3なの~~
全部足してもkになった
~~なんでこれで動かない？~~
k = 0のとき，setになにも入っていないので判定できていなかった．

- https://discord.com/channels/1084280443945353267/1300342682769686600/1357376133695541480
> 答えを見てみて、ロジックは理解できた。（マップのキーにnumsの各地点における累積和を格納し、バリューにその累積和の出現回数を対応させる。sumAtJ - k という値がキーに含まれていれば、J地点からそのsumAtJ-k地点まで戻った部分配列の和がｋということになるので、＋１カウントする。　＋１カウントはマップ内バリューに行い、かつ、return するべきint countに対しても、sumAtJ - kがキーに見つかった段階でようやくプラスする。　これによって、たとえばnums ={0,0,0,2,5}, k = 7のような場合でも、numsの各ポイント地点でマップのバリューに＋１カウントしてきたものを最後に一気にcountに足せる。）
何もみずに３回繰り返しをしようとすると少し手が止まる（すらすら書けない）ので、もう３回くらいやってみようと思う。（おそらく、ロジックがすっと頭に入っていないんだろう。）
```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        int count = 0;

        Map<Integer, Integer> prefixSumToCount = new HashMap<>();

        int sumAtJ = 0;

        prefixSumToCount.put(0, 1);//Key:prefixSum, Value:count

        for (int i = 0 ; i < nums.length ; i++) {
            
            sumAtJ += nums[i];
            
            prefixSumToCount.put(sumAtJ, prefixSumToCount.getOrDefault(sumAtJ, 0) + 1);

            if (prefixSumToCount.containsKey(sumAtJ - k)) {
                count = count + prefixSumToCount.get(sumAtJ - k);//Value: countを取り出してる
            }
        }
        return count;
    }
}
```
`set`だと過去の地点の標高が同じ場合，正しく数をカウントできない．
`defaultdict`で実装
計算量: O(n)
空間量: dictとcountのみなのでO(n)

1時間ぐらいかかった
Runtime: 37ms
Memory: 20.4MB

# step2
`tall`など，駅の話になっているので，問題に適した変数名に変更する．
`prefix_`は累積和を意味する.
step1の内容がほぼstep2だったかもしれない...
```py
if count := total_to_count[comp] != 0:
    n_sub_array += count
```
にしようともしたが，if文の条件が直感的にわからなくなるので却下した．
Runtime: 35ms
Memory: 20.3MB 
# step3
三回連続でかけた．
この問題に対するコーディングの理解(必要な変数や操作)は頭に入ったが，
類似の問題が出題された際に，累積和を使ってこの問題同様の手法で解くという思考につなげられるかの自信がない．
まだ`nums`の数値を直接使うのではなく，累積和を使う合理性の言語化ができない．
- https://qiita.com/drken/items/56a6b68edef8fc605821
累積和は総和を求めるアルゴリズム
確かに累積和って言ってるんだから，subarrayの和を処理しやすいのはあたりまえか．
