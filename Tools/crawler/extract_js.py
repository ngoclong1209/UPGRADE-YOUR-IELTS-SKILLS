import re

path = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/practicepteonline/reading/Test_1/Test_1.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'(async function grantAccess\(\) \{.*?\n        \})', content, re.DOTALL)
if match:
    with open("grantAccess.txt", "w") as f:
        f.write(match.group(1))
    print("Extracted JS")
else:
    print("NO JS")
