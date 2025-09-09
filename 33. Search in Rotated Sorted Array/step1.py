class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left != right:
            mid = (left + right) // 2
            # Targetがnums[-1]にある時はTrueとする
            isTargetOverCliff = target <= nums[-1]
            isMidOverCliff = nums[mid] < nums[-1]
            if isTargetOverCliff == isMidOverCliff:
                if nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid
            else:
                if nums[mid] > target:
                    left = mid + 1
                else:
                    right = mid
        # 一致したらindexを返す
        if nums[left] == target:
            return left
        else:
            return -1