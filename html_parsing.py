# %%
from docling.document_converter import DocumentConverter
import cv2
import numpy as np

html_report_source = "https://economictimes.indiatimes.com/reliance-industries-ltd/balancesheet/companyid-13215.cms"

converter = DocumentConverter(
    # format_options={
    #     InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    # }
)
result = converter.convert(html_report_source)

# %%
markdown_text = result.document.export_to_markdown()
markdown_text
# image = np.array(result.pages[0].image)
# for i in result.pages[0].predictions:
#     if i[0] == "layout":
#         for j in i[1].clusters:
#             if j.label == "picture":
#                 x1, y1, x2, y2 = int(j.bbox.l), int(j.bbox.t), int(j.bbox.r), int(j.bbox.b)
#                 cropped_image = image[y1:y2,  x1:x2]
#                 cv2.imwrite("image_section.png", cropped_image)
# %%
markdown_text

# %%
json_format_output = result.document.export_to_dict()
json_format_output
