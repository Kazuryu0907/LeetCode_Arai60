# 進め方
- step1: 5分考えて分からなかったら答えを見る。答えを理解したら、答えを隠して書く。筆が進まず5分立ったら答えを見る。答えを送信して正解するまで。
- step2: コードを読みやすく整える。動くコードになったら終了。
- step3: 時間を計りながら書く。10分以内に3回連続でアクセプトされるまで。

# step1: 10分
## 方針
これGoogleのCoding Interviewでみたやつだ
targetに対して使用するnumは2つと固定されてる．
各numに対して，$target-num$を保存しておいて，その値が出てきた時にindexをreturnすれば時間，空間どちらもO(n)で行ける．

ここまで5分

- 実行時間: 2ms
- メモリ: 19.11MB

`need_number[f"{n}"]`だとKey Errorが発生するので`get(f"{n}")`に変更．
## テストケースを考える
- 解がなかったり，targetに必要なnumの個数が決まっていなかったら，動的計画法とかになる気がする．（DPはちゃんと理解できてないので理解したい）
- これしか思いつかなかった

# step2: 30分
変数名がよろしくない（`need_number`,`other_index`）
`sorted`を導入する必要がない
### 参考にした方々
- [GoogleHow to: Work at Google — Example Coding/Engineering Interview](https://www.youtube.com/watch?v=XKu_SEDAykw)
`need_number`のところは`comp`(complements)になっている．(補完して完璧になるものの意味があるらしい)
- https://github.com/nktr-cp/leetcode/pull/12/files/00cec6dfcd5aa9ecf053069e3403458c30b5153a
`dict`の値を`index`にしてる．絶対この方が賢い
こうすることで`find`する必要ない．
(Pythonの`dict`はHashTableなので，検索の計算量は`O(1)`．)
そもそも`int`はHashableなので，keyを`str`にする必要がない．

`if complements.get(n):`の所で，`dict`にはkeyが存在しているのに，indexが0の時にはじかれてしまうバグが発生．`None`に対してのみはじくように変更．
Ruffでは`!= None`ではなく，`is not None`を推奨しているらしい．(https://docs.astral.sh/ruff/rules/none-comparison/)

### メモ
`==`はオブジェクトの等価性(TruthyかFalsyかみたいな)を評価して，`is`はオブジェクトの同一性(`id`関数を使って判定される)．
シングルトンなものを評価するにはそりゃ`is`の方がいいね


- 実行時間: 0ms
- メモリ: 19.28MB

# step3: 10分
`enumerate`の書き忘れなどが生じた．
Step2では`return [complements[target-complement_number],i]`としていたが，`return [complements[n],i]`でよいことに気づいた．
