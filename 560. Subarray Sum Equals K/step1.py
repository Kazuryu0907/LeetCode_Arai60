class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        tall = 0 # 標高
        tall_to_count: Dict[int, int] = defaultdict(int)
        # 初期地点の登録
        tall_to_count[tall] = 1
        n_sub_array = 0
        for n in nums:
            tall += n
            comp = tall - k
            if comp in tall_to_count:
                n_sub_array += tall_to_count[comp]
            # 通った標高の登録
            tall_to_count[tall] += 1
        return n_sub_array
