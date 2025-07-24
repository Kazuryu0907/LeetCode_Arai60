class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return max(nums, default=0)
        max_amount_rob_first = [0] * len(nums)
        max_amount_rob_not_first = [0] * len(nums)

        max_amount_rob_first[0] = nums[0]
        max_amount_rob_first[1] = nums[0]
        max_amount_rob_not_first[1] = nums[1]

        for i in range(2, len(nums)):
            max_amount_rob_first[i] = max(max_amount_rob_first[i - 1], max_amount_rob_first[i - 2] + nums[i])
            max_amount_rob_not_first[i] = max(max_amount_rob_not_first[i - 1], max_amount_rob_not_first[i - 2] + nums[i])
        # 最初を取るので，最後は取らない
        return max(max_amount_rob_first[-2], max_amount_rob_not_first[-1])
