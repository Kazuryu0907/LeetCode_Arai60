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