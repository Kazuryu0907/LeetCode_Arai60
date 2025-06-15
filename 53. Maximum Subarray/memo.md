# step1
## 方針
Subarrayのsumの最大値を出力
- prefixでもできそう...？
でもprefixの最大の差がわからないとだめだから無理か
- 典型的なDP？
n個までを使ったときの最大値をどうにかする？
連続なsubarrayの情報が一切入ってないからダメか

わからないのでカンニング

- https://github.com/tokuhirat/LeetCode/pull/32/files
prefixを左から見ていって最小のprefixからの距離を記録していくことで解けそう

# step2
- https://github.com/Jikuhara/LeetCode/pull/4/files
愚直に，全部の部分和を求めるとO(n^2)になる．
Inputが10^5なので，O(n^2)でCPUが1GHzだと単純計算で10^1になるから余裕でオーバーするのか
(やり方あってますか)

step1の実装だと，計算量O(n)，3つの変数で計算できて，nに依存しないので空間量O(1)．
せっかくならDPで解くやり方もやりたい
- https://github.com/hayashi-ay/leetcode/pull/36/files
いやこれがDPなのか

DPの定義
- https://ja.wikipedia.org/wiki/%E5%8B%95%E7%9A%84%E8%A8%88%E7%94%BB%E6%B3%
> 細かくアルゴリズムが定義されているわけではなく、下記2条件を満たすアルゴリズムの総称である。
帰納的な関係の利用：より小さな問題例の解や計算結果を帰納的な関係を利用してより大きな問題例を解くのに使用する。
計算結果の記録：小さな問題例、計算結果から記録し、同じ計算を何度も行うことを避ける。帰納的な関係での参照を効率よく行うために、計算結果は整数、文字やその組みなどを見出しにして管理される。

この問題の場合，二値を比べる操作を再帰的に行ってるし，最大値やprefixを記録してることで，二重ループを必要としないという認識か．いわゆる表みたいな配列を使ったDPはメモ化してるから記録してるなって直感的にわかりやすい．

- https://github.com/Jikuhara/LeetCode/pull/4/files
とてもスッキリしたコード
```c
int maxSubArray(int* nums, int numsSize) {
    int currentSum = nums[0];
    int maxSum = nums[0];
    for (int i = 1; i < numsSize; i++) {
        if (currentSum < 0)
            currentSum = nums[i];
        else
            currentSum += nums[i];
        
        if (currentSum > maxSum)
            maxSum = currentSum;
    }
    return maxSum;
}
```
`currentSum < 0`の時に`currentSum`をリセットしてる
イメージできないぞ...?
`nums=[-1, 1, 2, 3]`とかだと，1ループ目で`currentSum = 1`になって，そのあと足されていく．`currentSum < 0`が0である必然性が説明できない．
prefixじゃなくてsumか
`currentSum + nums[i] < currentSum`になって，増える可能性がなくなるから捨てる．
確かにstep1の`float("-inf")`はマジックナンバーの印象が大きい気がする．
少し変数名も調整して書いてみる
参考程度に86msから24msになった

# step3
コメントも追記してみた

選択肢を広げるとしたら，`current_sum`のif文を`current_sum = max(n, current_sum+n)`っていう書き方もある．
こっちのほうがコンパクトで美しいけど，コメントで補足は入れないと，`n`と`current_sum+n`を比べている理由がぱっとわからないかも
解き方としてはそんなに自由度ないのかな

