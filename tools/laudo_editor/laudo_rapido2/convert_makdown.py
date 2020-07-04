import markdown2

with open("doc\\doc.md", "r") as f:
    text = f.read()

html = markdown2.markdown(text)

with open("doc\\doc.html", "w") as f:
    f.write(html)
