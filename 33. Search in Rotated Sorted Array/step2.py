class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def priority(num: int) -> tuple:
            return (num <= nums[-1], num >= target)
        index = bisect_left(nums, priority(target), key=priority)
        if nums[index] == target:
            return index
        else:
            return -1