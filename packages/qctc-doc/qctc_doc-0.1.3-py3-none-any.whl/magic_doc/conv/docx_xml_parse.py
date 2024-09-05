'''
Author: dbliu shaxunyeman@gmail.com
Date: 2024-09-02 17:55:19
LastEditors: dbliu shaxunyeman@gmail.com
LastEditTime: 2024-09-05 09:02:32
FilePath: /magic-doc/magic_doc/conv/docx_xml_parse.py
Description: 
'''
import io
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from loguru import logger

from magic_doc.contrib.model import Content, Page
from magic_doc.contrib.office.docx_extract import DocxExtractor
from magic_doc.conv.base import BaseConv
from magic_doc.progress.filepupdator import FileBaseProgressUpdator
from magic_doc.progress.pupdator import ConvProgressUpdator


class Docx(BaseConv):
    def __init__(self):
        super().__init__()

    def to_md(self, bits: bytes, pupdator: ConvProgressUpdator, **kwargs) -> str:
        page_list = self.docx_to_pagelist(bits, pupdator)
        md_content_list = []
        for page in page_list:
            page_content_list = page['content_list']
            total = len(page_content_list)
            for index, content in enumerate(page_content_list):
                progress = 50 + int(index / total * 50)
                pupdator.update(progress)
                if content['type'] == 'image':
                    pass
                elif content['type'] in ["text", "md"]:
                    data = content['data']
                    md_content_list.append(data)
        return "\n".join(md_content_list)

    def docx_to_pagelist(self, bits, pupdator: ConvProgressUpdator) -> list[Page]:
        with tempfile.TemporaryDirectory() as temp_path:
            temp_dir = Path(temp_path)
            media_dir = temp_dir / "media"
            media_dir.mkdir()
            file_path = temp_dir / "tmp.docx"
            file_path.write_bytes(bits)
            docx_extractor = DocxExtractor()
            pages = docx_extractor.extract(file_path, "tmp", temp_dir, media_dir, True)
            pupdator.update(50)
            return pages


if __name__ == '__main__':
    pupdator = FileBaseProgressUpdator("/tmp/p.txt")
    docx = Docx()
    if 0:
        logger.info(docx.to_md(open(r"D:\project\20240514magic_doc\doc_ppt\doc\demo\文本+表+图.docx", "rb").read(), pupdator))
    if 1:
        print(docx.to_md(Path("/opt/data/magic_doc/20240605/doc/星际迷航.docx").read_bytes(), pupdator))