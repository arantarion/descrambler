import re
import string

with open("words2.txt", "r", encoding='utf-8') as f:
    text = f.readlines()

pattern = re.compile('[\W_]+')
scr = [pattern.sub('', word) for word in text]

out = []
for word in scr:
    out.append(''.join([i for i in word if not i.isdigit()]))

with open('new_dict3.txt', 'w+', encoding="utf-8") as f:
    for item in out:
        f.write("%s\n" % item)