class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        chars_to_strs = defaultdict(list)
        for s in strs:
            chars_set = "".join(sorted(s))
            chars_to_strs[chars_set].append(s)
        
        return list(chars_to_strs.values())