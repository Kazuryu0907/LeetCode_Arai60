# step1
文字列sが与えられ、その中で最大長の重複なしの部分文字列を探すもの
0 <= len(s) <= 5 * 10^4
sは英文字、数字、symbolと空白が含まれている
ASCII文字ということにしよう
となると、最大文字Byte数は50kBか

sliding windowなんだろうな
l, r = 0を用意して、rをインクリメントしていく。
lからrまでの範囲で重複がない文字列が見つかったら、lを重複がない範囲まで狭める。
そしてrを増やしていけば、全探索できる。

重複のチェックは、charに対して、defaultdict(int)をもたして、カウント数を保持していけば、sliding windowに対応しつつできそう
ここまで6分
実装してみる

でもこれはじめは確実に重複なしになるな
どのタイミングでlを縮めていけばいいんだろう。
重複があったタイミングで狭めればいいのか
以下でAccepted
```py
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
```
空間計算量はO(1) (ASCII文字と仮定すると定数)
時間計算量はO(n) (r, lは最大でもN回の移動なので。ASCII文字とすると判定も定数になる)

30分弱かかってしまった
# step2
人のを見てみる。
- https://github.com/ryosuketc/leetcode_arai60/blob/d6c547f63ab0789644325a147afffafaf1108525/3_longest_substring_without_repeating_characters/step2.py
```py
class Solution1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_len = 0
        seen = set()
        left = 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            max_len = max(max_len, right - left + 1)
        return max_len
```
defaultdictじゃなくて、setを使った例。
確かに、先頭の文字(r)がuniqueかだけをみれば、帰納法的に検証できるのか
alphabetが何個でたかに関心はないから、setでいいのか。0 or otherwiseが大切。

- https://github.com/Kaichi-Irie/leetcode-python/pull/9/files#r2157770058
```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        char_to_last_index = {}
        max_length = 0
        for i, c in enumerate(s):
            start = max(start, char_to_last_index.get(c, -1) + 1)
            max_length = max(max_length, i - start + 1)
            char_to_last_index[c] = i
        return max_length
```
test case: "abbcdda"
charが最後に出てきたindexを保持しておいて、そこの距離を求めるもの。
ダブったタイミングでlを更新するべつの方法か

setを使ったやり方でやってみる
```py
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
```

というか、step1で解いたやつ、`not is_unique_substring()`じゃなくて、`char_to_count[char] > 1`でよかったな

# step3
```py
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
```