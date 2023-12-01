# Just examples of how the implementation goes
import markdown


# https://www.markdownguide.org/basic-syntax/  - Python Markdown Documentation
# https://python-markdown.github.io/reference/  - A Markdown reference


# Get Markdown From a file and write as html to another file
with open("some_file.txt", "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text)
If you want to write the output to disk, you must encode it yourself:

with open("some_file.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(html)


---
# Take markdown directly and convert to html
import markdown
html = markdown.markdown(#Testing Heading 1!)
    
KeyboardInterrupt
html = markdown.markdown("#Testing Heading 1!")
html
