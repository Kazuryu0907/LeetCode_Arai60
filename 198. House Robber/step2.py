
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        one_previous_max = 0
        two_previous_max = 0
        for num in nums:
            target_max = max(two_previous_max + num, one_previous_max)
            two_previous_max = one_previous_max
            one_previous_max = target_max
        return target_max
