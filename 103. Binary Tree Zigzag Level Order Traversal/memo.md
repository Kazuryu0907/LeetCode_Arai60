# step1
binary treeのrootが与えられて、level Orderをジグザグ(左->右の次は右->左)で返す
## 制約、要件
サンプルケース: [1] output [[1]]
最小ケース: [] output []
node数は2000なので、levelは最大11になる(2^11=2048より)
nodeのvalueは-100~100の間

前回のものが大部分使えそう
BFSのappend順を制御すれば、思っているものができそう
rootのlevelが1として、
制御
1. levelが偶数 -> 右->左
2. levelが奇数 -> 左->右

実装してみる
↓動きません(DFS)
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def getZigzagLevelOrder(node: Optional[TreeNode], level: int) -> None:
            # 新しいLevelに行ったとき、それ用の配列を用意する
            while len(level_order_values) < level:
                level_order_values.append([])
            level_order_values[level - 1].append(node.val)
            first_node = node.left
            second_node = node.right
            # right to left
            if (level + 1) % 2 == 0:
                first_node, second_node = second_node, first_node
            if first_node:
                getZigzagLevelOrder(first_node, level + 1)
            if second_node:
                getZigzagLevelOrder(second_node, level + 1)
        
        if not root:
            return []
        level_order_values = []
        getZigzagLevelOrder(root, 1)
        return level_order_values
```
nodeの子要素に対して
[1, 2, 3, 4, 5, 6, 7]に対して、3 -> 2の順番にqueueに積まれ、[6, 7] -> [4, 5]の子要素が得られる
ここから[4, 5, 6, 7]を得るにはreverseしてflattenにするのが正解？
ここをうまく実装、論理立てれなかった
- https://github.com/hroc135/leetcode/pull/26/files
普通にreverseすればいいだけだな...
自分の考えたやり方に視野が狭くなっていって、もっと大切なところが見えてない
ものを考える順番がおかしい気がするから、ここを次から気をつけてみる
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        nodes_in_level = [root]
        values_level_order = []
        level = 1
        while nodes_in_level:
            values_in_level = []
            nodes_in_next_level = []
            for node in nodes_in_level:
                values_in_level.append(node.val)
                if node.left:
                    nodes_in_next_level.append(node.left)
                if node.right:
                    nodes_in_next_level.append(node.right)
            # right to left
            if level % 2 == 0:
                values_in_level.reverse()
            values_level_order.append(values_in_level)
            nodes_in_level = nodes_in_next_level
            level += 1
        return values_level_order
```
空間計算量: O(n) 結果を格納するのに、全てのnodeのvalueが必要なので
時間計算量: O(n) 全てのnodeを通る。でも`reverse()`はO(n')かかるから、どうなんだろう
`reverse()`に入る最大の要素数は、levelが最大11になることを踏まえると、`level=10`の時、要素数$2^{10}=1024$になる。そんなにデカくはない。

# step2
- https://github.com/goto-untrapped/Arai60/pull/51/files
DFS stackで解いてる例
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        level_order_values = []
        stack_nodes = [(root, 1)]
        while stack_nodes:
            node, level = stack_nodes.pop()
            if not node:
                continue
            print(node.val)
            while len(level_order_values) < level:
                level_order_values.append([])
            # リストに逆順で追加していく
            if level % 2 == 0:
                level_order_values[level - 1].insert(0, node.val)
            else:
                level_order_values[level - 1].append(node.val)
            
            stack_nodes.append((node.right, level + 1))
            stack_nodes.append((node.left, level + 1))
        
        return level_order_values
```
でも`insert`でO(1)になっているから、stackのメリットを活かせていない

というか、前回の処理をそのままに、最後に偶数indexのlistをreverseすればいいだけなのでは。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def getLevelOrder(node: Optional[TreeNode], level: int) -> None:
            if not node:
                return
            # 新しいlevelに達した時、配列に初期値を追加する
            while len(values_level_order) < level:
                values_level_order.append([])
            values_level_order[level - 1].append(node.val)
            getLevelOrder(node.left, level + 1)
            getLevelOrder(node.right, level + 1)
            
        values_level_order = []
        getLevelOrder(root, 1)
        # 偶数levelの配列をrevereseする
        for i, values_in_level in enumerate(values_level_order):
            if i % 2 == 1:
                values_in_level.reverse()
            
        return values_level_order
```
うん。こっちの方が保持する変数も少なくて、見やすくていい気がする。
一度binary treeのlevel毎の値をとってから`reverse`しているので、処理自体が一般化されて、utilityとして使いやすそうだと感じた。

でも、一旦levelごとに処理していく方式でいくことにする。


# step3
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        nodes_in_level = [root]
        values_level_order = []
        level = 1
        while nodes_in_level:
            values_in_level = []
            nodes_in_next_level = []
            for node in nodes_in_level:
                values_in_level.append(node.val)
                if node.left:
                    nodes_in_next_level.append(node.left)
                if node.right:
                    nodes_in_next_level.append(node.right)
            if level % 2 == 0:
                values_in_level.reverse()
            values_level_order.append(values_in_level)
            nodes_in_level = nodes_in_next_level
            level += 1
        return values_level_order
```