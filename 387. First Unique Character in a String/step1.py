class Solution:
    def firstUniqChar(self, s: str) -> int:
        str_to_count: Dict[str, int] = {}
        for char in s:
            if char not in str_to_count:
                # 初回登録
                str_to_count[char] = 0
            str_to_count[char] += 1
        for (char, count) in str_to_count.items():
            # first con-repeating char
            if count == 1:
                return s.index(char)
        # does not exist
        return -1
