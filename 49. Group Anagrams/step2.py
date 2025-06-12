class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        chars_to_strs = collections.defaultdict(list)
        for s in strs:
            sorted_chars = "".join(sorted(s))
            chars_to_strs[sorted_chars].append(s)
        
        return list(chars_to_strs.values())
