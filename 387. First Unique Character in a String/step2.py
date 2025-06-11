class Solution:
    def firstUniqChar(self, s: str) -> int:
        seen = set()
        char_to_index = collections.OrderedDict()
        for i, c in enumerate(s):
            if c in seen:
                # 出現が2回目以降なら
                char_to_index.pop(c, None)
                continue
            seen.add(c)
            char_to_index[c] = i
        if not char_to_index:
            return -1
        _, index = char_to_index.popitem(last=False)
        return index
