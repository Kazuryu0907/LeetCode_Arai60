class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        max_lengths = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    max_lengths[i] = max(max_lengths[i], max_lengths[j] + 1)
        return max(max_lengths)
