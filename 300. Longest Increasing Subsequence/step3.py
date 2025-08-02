class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # lis[i]はlisの長さがiになるときの末尾の最小値
        lis = []
        for n in nums:
            i = bisect.bisect_left(lis, n)
            if i == len(lis):
                lis.append(n)
            else:
                lis[i] = n
        return len(lis)
