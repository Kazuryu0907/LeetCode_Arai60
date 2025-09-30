# step1
binary treeのrootが与えられるから、その深さOrderでnodeの値を二次元配列で返す問題
rootは空配列もあり得る
binary treeの配列indexって、log2の値が深さになる。確か
0 ~ 2^1 - 1: root
2^1 ~ 2^2 - 1: L1
...
~~これをfor loopで回せばいいのでは やってみる~~
TreeNodeが与えられるのね
グラフの帰りがけとかの問題か
本で読んだな
どのタイミングでnodeをinsertするかで変わるはず
確か、行きがけは昇順に、帰りがけは降順になるんだっけか
でもこの情報から、どうやって深さOrderの配列を取り出せばいいだろう
↓動きません
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    treeValueList = []
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        treeValueList = self.getTreeValueList(root)
        print(treeValueList)
    
    def getTreeValueList(self, root: Optional[TreeNode]):
        treeValueList = []
        def recursiveTree(node: Optional[TreeNode]):
            if node is None:
                return
            treeValueList.append(node.val)
            recursiveTree(node.left)
            recursiveTree(node.right)
        recursiveTree(root)
        return treeValueList
```

カンニングする
- https://github.com/olsen-blue/Arai60/pull/26
普通にBFSの話だった...帰りがけの話を引っ張りすぎて、こんなことにも気づかない
危機感持った。知識としてのBFSをoutputとして使えてない？

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        node_in_depth = [root]
        level_order_nodes = []
        while node_in_depth:
            node_in_next_depth = []
            node_values_in_depth = []
            # 同一Levelのnode一覧
            for node in node_in_depth:
                node_values_in_depth.append(node.val)
                if node.left:
                    node_in_next_depth.append(node.left)
                if node.right:
                    node_in_next_depth.append(node.right)
            node_in_depth = node_in_next_depth
            level_order_nodes.append(node_values_in_depth)
        return level_order_nodes
```
空間計算量: O(n)
時間計算量: O(n)
# step2
- https://github.com/ryosuketc/leetcode_arai60/blob/a66c82be97ac32a633b8dee3223a115361a51909/102_binary_tree_level_order_traversal/memo.md?plain=1#L10
> *   node 数の制約は 2000 なのでメモリに積んでいって特に問題はないはず
なるほど。そういう問題意識もあるのか
- https://github.com/hayashi-ay/leetcode/pull/32/files
depth付きの再帰BFS
管理する変数が少なくて済む。再帰の深さも log2 2000なので全然問題ない
こっちの書き方の方が好き

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def getNodeValuesOrder(node: Optional[TreeNode], level: int):
            if node is None:
                return
            while len(level_order_nodes) < level:
                level_order_nodes.append([])
            level_order_nodes[level - 1].append(node.val)
            getNodeValuesOrder(node.left, level + 1)
            getNodeValuesOrder(node.right, level + 1)
        
        level_order_nodes = []
        getNodeValuesOrder(root, 1)
        return level_order_nodes
```
これ、`if node is None`と`if not node`だとどっちがいいんだろう
jsとかだったら、絶対`if(!node)`にするけど。`if not node`は`if node is None`を内包していると思う。
でも`node`が`None`なのが重要というよりかは、`node`が`falsy`なのが重要な気がする。
よければご意見ください

# step3
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def getNodeOrderValues(node: Optional[TreeNode], level: int) -> None:
            if not node:
                return
            # 新しいLevelになったら、配列を用意する
            while len(level_order_nodes) < level:
                level_order_nodes.append([])
            level_order_nodes[level - 1].append(node.val)
            getNodeOrderValues(node.left, level + 1)
            getNodeOrderValues(node.right, level + 1)
        
        level_order_nodes = []
        getNodeOrderValues(root, 1)
        return level_order_nodes

```
空間計算量: O(n) `level_order_nodes`の要素数
時間計算量: O(n) 全部のnode通ってるから