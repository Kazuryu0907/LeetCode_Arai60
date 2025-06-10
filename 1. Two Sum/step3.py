class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        complements:Dict[int,int] = {}
        for i,n in enumerate(nums):
            complement_number = target - n
            # nを足すとtargetになる数がすでにあったら
            if complements.get(n) is not None:
                return [complements[n],i]
            complements[complement_number] = i