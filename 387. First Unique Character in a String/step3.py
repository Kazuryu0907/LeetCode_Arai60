class Solution:
    def firstUniqChar(self, s: str) -> int:
        char_to_index = collections.OrderedDict()
        seen = set()
        for i, c in enumerate(s):
            if c in seen:
                # 2回目以降
                # Key ErrorにならないようにNone
                char_to_index.pop(c, None)
                continue
            char_to_index[c] = i
            seen.add(c)
        if not char_to_index:
            # 空だったら
            return -1
        _, index = char_to_index.popitem(last=False)
        return index
