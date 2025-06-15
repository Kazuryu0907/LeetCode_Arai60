class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]
        # nums[0]で初期値を入れているので，nums[1]から始める
        for n in nums[1:]:
            # current_sumが増えないと確定したらリセット
            if current_sum < 0:
                current_sum = n
            else:
                current_sum += n
            if max_sum < current_sum:
                max_sum = current_sum
        return max_sum
