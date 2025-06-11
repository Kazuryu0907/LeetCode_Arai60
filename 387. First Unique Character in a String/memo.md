# step1: 7分
## 方針
リピートしない文字列を見つける．
ない場合もある．
=> HashMapでカウントして，一回終わったあと，もう一度Mapのvalueを探索して，始めのcountが1のkeyをreturnする．これだと計算O(N)，空間O(N)でいける．
indexを返さないと行けないから，もう一度文字列でindex()しないといけない？

とりあえずこれで実装してみる
ここまで5分

- 計算時間: 55ms
- メモリ: 17.95MB
  
# step2: 30分
### ほかのアイデア
`Dict[str, Tuple[int, int]]`にして，countとindexを同時に持っておく？
### ありそうなコメント
`str_to_count`より`char_to_count`のほうが直感に合っている気がする．
`char`だとC++言語者から見たら型に見えてしまう可能性がありそう．
### 参考にした方々
- https://github.com/garunitule/coding_practice/pull/15#discussion_r2130547387
`str_to_count`に二回目入ったら，-1を代入して，index保持する方法がある．
- https://github.com/skypenguins/coding-practice/pull/4
- https://discord.com/channels/1084280443945353267/1201211204547383386/1211166072552816680
```python
class Solution:
    def firstUniqChar(self, s: str) -> int:
        seen = set()
        unique = collections.OrderedDict()
        for i, c in enumerate(s):
            if c in seen:
                unique.pop(c, None)
                continue
            unique[c] = i
            seen.add(c)
        if not unique:
            return -1
        _, index = unique.popitem(last=False)
        return index
```
`set`を使用して，今までに表れた文字を保存しておく方法．`set`に入ってる文字は`dict`から`pop()`して，ないときは`dict`にindexを入れる．`set`はHashTableなので`in seen`がO(1)で行える．
`OrderedDict`という順序づけ(stack)されていることを明示的に示せる辞書が`collections`に入っている．`popitem()`でkeyとvalue両方とれる．初めて知った．
- https://docs.python.org/ja/3.13/library/collections.html#collections.OrderedDict
`last=`は，`True`だとLIFO(Stack)になって，`False`だとFIFO(Queue)になる．つまり`last`から取り出すかどうかってことか．
## 1.小田さんを参考にした方
```python
class Solution:
    def firstUniqChar(self, s: str) -> int:
        seen = set()
        char_to_index = collections.OrderedDict()
        for i, c in enumerate(s):
            if c in seen:
                # 出現が2回目以降なら
                char_to_index.pop(c, None)
                continue
            seen.add(c)
            char_to_index[c] = i
        if not char_to_index:
            return -1
        _, index = char_to_index.popitem(last=False)
        return index
```
- 計算時間: 59ms
- メモリ: 18.34MB
逆に数値が悪くなった...
メモリは`set`を使ったので増えるのはわかる．`pop`や`add`を追加したことの処理時間の差か?
## 2.自分のやつを改善したもの 
```python
class Solution:
    def firstUniqChar(self, s: str) -> int:
        char_to_index = collections.OrderedDict()
        for i, c in enumerate(s):
            if c in char_to_index:
                # 2回目以降
                char_to_index[c] = -1
                continue
            char_to_index[c] = i
        
        for index in char_to_index.values():
            if index != -1:
                return index
        return -1

```
- 計算時間: 62ms
- メモリ: 17.9MB

どっちのほうが美しいんでしょうか...
2.は`char_to_index`にindexとflag的な`-1`があって少し意味を持たせすぎな気がする．
少し記述量が増えるが，役割がはっきりしている1.のほうが美しい気がしてきた．

# step3: 15分
```py
if not char_to_index:
    # 空だったら
    return -1
```
これと，
```py
# 空だったら
if not char_to_index:
    return -1
```
どっちが共通認識なんだろう
- https://source.chromium.org/chromium/chromium/tools/depot_tools/+/main:utils.py;l=53?q=%5Cbif%5Cb%20filepath:.*%5C.py$&start=11
```py
# Silently migrate cfg from legacy path if it exists.
if not os.path.isfile(expected_path):
    legacy_path = os.path.join(DEPOT_TOOLS_ROOT, file)
    if os.path.isfile(legacy_path):
        shutil.move(legacy_path, expected_path)
```
Chromium Codeだと`if`の上に書いている．
皆さんの意見聞きたいです．