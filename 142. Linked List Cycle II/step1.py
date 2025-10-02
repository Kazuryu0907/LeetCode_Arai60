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