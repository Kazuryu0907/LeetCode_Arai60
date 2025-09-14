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