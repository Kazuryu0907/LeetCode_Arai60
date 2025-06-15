class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        prefix_sum = 0
        min_prefix = 0
        max_sum = float("-inf")
        for n in nums:
            prefix_sum += n
            max_sum = max(max_sum, prefix_sum-min_prefix)
            min_prefix = min(min_prefix, prefix_sum)
        return max_sum
