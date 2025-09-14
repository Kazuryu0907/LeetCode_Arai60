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