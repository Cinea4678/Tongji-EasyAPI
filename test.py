import re

with open("sample/herf.html","r") as f:
    text = f.read()

print(re.match(r"^window\.location\.href=\'.*\'$",text))
print(re.findall(r"window\.location\.href=\'(.*?)\'",text))