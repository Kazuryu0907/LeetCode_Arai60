# step1
## 方針
アナグラムってことは，set()の構成要素で判定すればいいはず．
どうやって判定する？~~どうやら`Dict`もHashableらしい~~違った
~~HashMapに突っ込みます~~
ここまで3分半

`set`だと重複がつぶれてしまうので意味がない
`Counter`を使おうとしたが，Hashableにできなかったため断念

### 動きません↓
```py
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        set_to_indexes = {}
        for i, s in enumerate(strs):
            char_set = tuple(collections.Counter(s))
            print(char_set)
            if char_set not in set_to_indexes:
                set_to_indexes[char_set] = []
            set_to_indexes[char_set].append(i)
        
        out = [[]]
        for indexes in set_to_indexes.values():
            out.append([strs[i] for i in indexes])
        return out
```
一度LeetCodeのSolutionsを参考にしてみることに．
`defaultdict`でKeyがないときはdefault値を勝手に設定してくれる．

- 計算時間: 11ms
- メモリ: 20.66MB

計算量は`for`のlinerと，`sorted`．
`sorted`にはTimSortが採用されているらしい(https://tech.preferred.jp/ja/blog/tim-sort/)
最悪計算量が$O(n\log n)$で，クイックソートやバブルソートの$O(n^2)$より早い．
空間量は`dict`と，`sorted`．
`dict`は`hash`の範囲と`list`のポインタで決まるはずなので，$O(n)$．TimSortも$O(n)$．
以上より，
- Time: $O(n \log n)$
- Space: $O(n)$

# step2
変数名が気持ち悪すぎる
`key`は情報量が少ないし，`ans`は答えという情報しか入っていなくて，実際に何を格納するのかわからない


### 参考にした方々
- https://github.com/garunitule/coding_practice/pull/12/commits/5c69ce27134e09c306105473fa70cf400fcb0c4c
alphabet26文字文のList作って，出現回数をCount, => TupleにしてHashableにするというもの．
alphabet以外の入力が入った場合に死ぬ．その点，`sorted`は一意性と柔軟性を兼ね備えている．
でもこっちはsortする必要がないため，計算量が$O(n)$で済むメリットがある．
Tupleに変換せずにHashableにする方法はないものか
- https://github.com/fuga-98/arai60/pull/13/commits/98c060cacd001a530b6eadcd0f004eb94f2297d5
`s`をsortして，一意性を確保して`str`にキャストしてDictのkeyにしている
`str`にキャストするより，`"".join(strs)`にしたほうが自然だと思うのは，後者はlist to stringを実現するという狭い使い方になっているからだろうか？

もし，入力がstrに限らず，intなどがはいるとしたら，`sorted`に入れる前に`str`でキャストすることで対応できそう．

# step3
例外や，別の解法(`frozenset`などを用いた)なども考えたがこれ以上浮かばなかった．

`chars_to_strs`を`chars_set_to_strs`にしようかとも考えたが，`_`が増え，keyとvalueの対応が取りにくいと感じたため変更しなかった．


