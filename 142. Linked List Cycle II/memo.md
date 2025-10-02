# step1
linked listのheadが与えれれるので、サイクルがどこから始まっているかを返す
サイクルがない場合はNoneを返す
入力はListNode classで与えられ、node数は 0 <= len(Node) <= 10^4
普通に、headから辿っていってsetに格納して、訪れたことあったらcycleがある実装にすればいけそう
Acceptされた
```py
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        node = head
        while node is not None:
            if node in seen:
                return node
            seen.add(node)
            node = node.next
        return None
```
時間計算量はO(n) (全てのnodeを探索するから)
空間計算量はO(n) (全てのnodeを保持する必要があるから)
O(10^4)だとして、C++が1秒に1Gステップ実行できるとして、Pythonだとそれより100倍遅いから、10Mステップ実行できるとすると、
1msくらいで処理できそう

でもこれ、nodeのhashがどうなるかって、ListNodeの実装によるくないか...?
問題文ではListNodeをmodifyするなって書いてるし...
なんかもっといい方法ありそう
- https://docs.python.org/3/glossary.html#term-hashable
objectがhashableっていうのは、`__hash__()`methodがあって、比較用に`__eq__()`methodがある必要がある。
- https://docs.python.org/3/reference/datamodel.html#object.__hash__
> User-defined classes have __eq__() and __hash__() methods by default (inherited from the object class); with them, all objects compare unequal (except with themselves) and x.__hash__() returns an appropriate value such that x == y implies both that x is y and hash(x) == hash(y).
つまり、明示的に`__hash__()`が定義されていない場合、自身と同じポインタを指してる場合、hashが一致するということか
だから、今回みたいな、インスタンスを新しく作る必要がない場合はうまく動いたのね

# step2
人の見てみる
- https://discord.com/channels/1084280443945353267/1246383603122966570/1252209488815984710
> はい。2歩ずつ走るうさぎと1歩ずつ歩くかめが、ある地点でぶつかったとします。そこを衝突点と呼びましょう。衝突点が見つかったあとに、衝突点とスタート地点から1歩ずつうさぎとかめを歩かせて、衝突するところが、合流地点である、ということを理解したいということですね。
> うさぎとかめは、衝突点で出会った後に、うさぎとかめは、いま来た道を戻るように言われました。うさぎもかめも同じ速さで1歩ずつ歩いて戻ります。このとき、うさぎは一周してから戻りますが、かめはそのまま戻ります。
> かめがスタート地点に戻った時、うさぎはどこにいるでしょうか。実は、うさぎは衝突点にいます。なぜかというと、うさぎは倍速で走っているからです。スタート地点から衝突点を通って衝突点に到達するうさぎルートの長さは、スタートから衝突点に到達するかめルートの2倍だからです。
> ところで、この戻っていく時、うさぎとかめは、衝突点から同じ速さで歩いて戻っているので、合流点までは一緒にいましたね。
> さて、ここまでの話を動画にして逆回しにしてみましょう。
> うさぎとかめは、それぞれ衝突点とスタート地点から同じ速さで後ろ向きに歩き始めます。そして、合流地点から一緒に後ろ向きに歩き始め、そして衝突点に到達します。

フロイドの循環検出アルゴリズムの説明
なんとなくイメージはできた
実装自体は簡単だけど、なんでこれで動作するのかって言われたら答えれる自信はない...
手を動かしてみる
```py
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head
        exist_cycle = False
        while fast is not None and fast.next is not None:
            # 二倍進む
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                exist_cycle = True
                break
        if not exist_cycle:
            return None
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow
```
空間計算量がO(1)になるのはとてもメリット
- https://github.com/olsen-blue/Arai60/blob/c24f4107670683034c2fc5e967bb5c75f698e815/142_LinkedListCycleII.md
fastをheadに戻して、使い回すの、ちょっとナンセンスかも
originを使っている。いいかも
- https://discord.com/channels/1084280443945353267/1322513618217996338/1322841650162303008
while-else文とかあるのか
- https://docs.python.org/ja/3/reference/compound_stmts.html#the-while-statement
while文で、評価式がFalseだったらelse文を実行する。breakされて場合はこの限りじゃない。
これなら、`exist_cycle`変数使わなくて済みそう
```py
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head
        while fast is not None and fast.next is not None:
            # 二倍進む
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                exist_cycle = True
                break
        else:
            return None
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow
```
できた

# step3
```py
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = head
        slow = head
        while fast is not None and fast.next is not None:
            # 二倍進める
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                break
        else:
            return None
        # exist_cycle
        origin = head
        while origin != fast:
            origin = origin.next
            fast = fast.next
        return origin
```