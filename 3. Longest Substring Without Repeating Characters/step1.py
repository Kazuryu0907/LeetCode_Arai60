class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        def is_unique_substring():
            for count in char_to_count.values():
                # 重複があった場合
                if count > 1:
                    return False
            return True
        char_to_count = defaultdict(int)
        # [l, r] 閉区間
        l = 0
        max_substring_len = 0
        for r, char in enumerate(s):
            char_to_count[char] += 1
            # 重複があった時、範囲を狭める
            while not is_unique_substring():
                remove_char = s[l]
                char_to_count[remove_char] -= 1
                l += 1
            max_substring_len = max(max_substring_len, r - l + 1)
        return max_substring_len