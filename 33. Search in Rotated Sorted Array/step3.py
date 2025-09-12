class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def priority(num: int) -> tuple:
            # (A, B)
            # A: 崖の前か後か
            # B: 部分集合の中で[FFFTTT]を作る
            return (num <= nums[-1], num >= target)
        index = bisect_left(nums, priority(target), key=priority)
        if nums[index] == target:
            return index
        else:
            return -1