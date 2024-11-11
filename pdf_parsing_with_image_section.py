# %%
from docling.backend.pdf_backend import Optional
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling_core.types.doc.base import ImageRefMode
import cv2
import numpy as np
from typing import Optional, Tuple, Dict
from collections import defaultdict

# single_page_pdf = "doc_with_formula_1.pdf"
class StructuredDocument:
    def __init__(self, pdf_file_name, pipeline_options: Optional[PdfPipelineOptions] = None):
        if pipeline_options is None:
            self.pipeline_options = PdfPipelineOptions(do_table_structure=True, generate_page_images=True, do_ocr=True)
            self.pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE  # use more accurate TableFormer model

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=self.pipeline_options)
            }
        )
        self.pdf = pdf_file_name
        self.markdown_text, self.cropped_images = self.parse_pdf()

    def parse_pdf(self) -> Tuple[str, Dict[int, list]]:
        images = defaultdict(list)
        result = self.converter.convert(self.pdf)
        markdown_text = result.document.export_to_markdown()

        for pg_nm, page in enumerate(result.pages):
            image = np.array(page.image)
            for prediction in page.predictions:
                if prediction[0] == "layout":
                    for cell in prediction[1].clusters:
                        if cell.label == "picture":
                            x1, y1, x2, y2 = int(cell.bbox.l), int(cell.bbox.t), int(cell.bbox.r), int(cell.bbox.b)
                            cropped_image = image[y1:y2,  x1:x2]
                            images[int(pg_nm)].append(cropped_image)

        return markdown_text, images
