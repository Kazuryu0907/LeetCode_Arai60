class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        lis = []  
        for n in nums:
            index = bisect.bisect_left(lis, n)
            if index == len(lis):
                lis.append(n)
            else:
                lis[index] = n
        return len(lis)
