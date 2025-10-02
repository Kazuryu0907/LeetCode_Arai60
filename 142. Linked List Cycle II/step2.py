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