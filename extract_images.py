from pypdf import PdfReader
from PIL import Image
import io
import os

reader = PdfReader("c:/Users/swaya/portfolio_/swayamshreetripathy_resume.pdf")
page = reader.pages[0]
count = 0

if not os.path.exists("c:/Users/swaya/portfolio_/static/images"):
    os.makedirs("c:/Users/swaya/portfolio_/static/images")

for image_file_object in page.images:
    with open(f"c:/Users/swaya/portfolio_/static/images/{image_file_object.name}", "wb") as fp:
        fp.write(image_file_object.data)
        count += 1

print(f"Extracted {count} images.")
