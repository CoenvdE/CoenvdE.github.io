import re

with open('index.html', 'r') as f:
    html = f.read()

# Check get in touch button
matches = re.findall(r'<a href="mailto:.*?>.*?Get in Touch.*?</a>', html, re.DOTALL)
print("Get in Touch button:")
for m in matches:
    print(m)
