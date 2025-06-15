class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]
        for n in nums[1:]:
            # n足して，減るのが確定したら，リセットする
            if current_sum < 0:
                current_sum = n
            else:
                current_sum += n
            if max_sum < current_sum:
                max_sum = current_sum
        return max_sum
