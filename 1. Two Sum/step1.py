class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        need_number = {}
        for i,n in enumerate(nums):
            if need_number.get(f"{n}"):
                other_index = nums.index(target-n)
                return list(sorted([i,other_index]))
            need_number[f"{target-n}"] = True
    