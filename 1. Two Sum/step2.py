class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        complements:Dict[int,int] = {}
        for i,n in enumerate(nums):
            complement_number = target-n
            if complements.get(n) is not None:
                return [complements[target-complement_number],i]
            complements[complement_number] = i