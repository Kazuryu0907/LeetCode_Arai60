class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @cache
        def get_num_paths(m: int, n: int) -> int:
            if m == 0 or n == 0:
                return 1
            return get_num_paths(m - 1, n) + get_num_paths(m, n - 1)
        return get_num_paths(m - 1, n - 1)
