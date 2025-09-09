class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # 崖を越える前なら
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid
        return nums[left]