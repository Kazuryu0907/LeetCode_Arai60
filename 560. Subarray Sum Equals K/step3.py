class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        total = 0
        total_to_count = defaultdict(int)
        # 0地点の登録
        total_to_count[total] = 1
        n_sub_array = 0
        for n in nums:
            total += n
            comp = total - k
            if comp in total_to_count:
                n_sub_array += total_to_count[comp]
            # 登録
            total_to_count[total] += 1 
        return n_sub_array
