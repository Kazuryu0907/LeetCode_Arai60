class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        l = 0
        max_substring_len = 0
        for r, char in enumerate(s):
            while char in seen:
                remove_char = s[l]
                seen.remove(remove_char)
                l += 1
            seen.add(char)
            max_substring_len = max(max_substring_len, r - l + 1)
        return max_substring_len