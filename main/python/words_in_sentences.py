import re
sentence = 'Hello, what are doing. hello, it is what you are doing?'
sentence = re.sub(r'[^\s\w]','', sentence)
from collections import Counter
words = sentence.lower().split()
count = Counter(words)
print(dict(count))












# words = re.split(' ',sentence)
# print(words)
# dict1 = {}
# for w in words:
#     if w.lower() in dict1:
#         dict1[w.lower()] += 1
#     else:
#         dict1.update({w.lower():1})
#
# print(dict)



