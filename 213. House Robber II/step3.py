class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        return max(self.max_amount_rob_first_house(nums[:-1]), self.max_amount_rob_first_house(nums[1:]))
    def max_amount_rob_first_house(self, nums: List[int]) -> int:
        max_amount = [0] * len(nums)
        max_amount[0] = nums[0]
        max_amount[1] = max(nums[:2])
        for i in range(2, len(nums)):
            max_amount[i] = max(max_amount[i - 1], max_amount[i - 2] + nums[i])
        return max_amount[-1]
