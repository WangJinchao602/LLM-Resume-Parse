'''
PDF文字提取
Author: WangJinchao
Date: 2025/08/14
'''
import io
import logging

from numpy.f2py.crackfortran import endifs
from playa.ascii85 import end_re


# 1. 使用kreuzberg直接提取
# https://gitee.com/mirrors/Kreuzberg
def pdf_extract(pdf_path):
    from kreuzberg import extract_file_sync
    result = extract_file_sync(pdf_path)
    return result.content

# 2. 使用PyMuPDF转图片 OCR识别
import fitz  # PyMuPDF
import os
import shutil
from image_ocr import cn_ocr as ocr

def pdf_ocr(pdf_path):
    # 定义临时cache文件夹路径
    cache_folder = "./cache"

    # 确保cache文件夹存在
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    try:
        # 打开PDF文件
        doc = fitz.open(pdf_path)

        # 存储所有页面的OCR结果
        all_text = []

        # 存储生成的图片路径，用于后续删除
        image_paths = []

        # 遍历PDF的每一页
        for page_num in range(len(doc)):
            # 获取当前页
            page = doc[page_num]

            # 定义PNG文件的名称
            png_filename = os.path.join(cache_folder, f"page_{page_num}.png")

            # 将当前页转换为PNG并保存到临时文件
            pix = page.get_pixmap()
            pix.save(png_filename)

            # 记录图片路径
            image_paths.append(png_filename)

            # 对图片进行OCR识别
            page_text = ocr(png_filename)
            all_text.append(f"{page_text}\n")

        # 关闭PDF文件
        doc.close()

        # 将所有页面的文本合并为一个字符串
        complete_text = "\n".join(all_text)

        return complete_text

    finally:
        # 处理完成后删除临时文件和文件夹
        try:
            if os.path.exists(cache_folder):
                shutil.rmtree(cache_folder)
                logging.info(f"临时文件夹 {cache_folder} 已删除")
        except Exception as e:
            logging.info(f"删除临时文件夹时出错: {e}")

# 3.免费版Free Spire.PDF for Python
def spire_pdf_ocr(pdf_path):
    from spire.pdf import PdfDocument
    from spire.pdf import PdfTextExtractOptions
    from spire.pdf import PdfTextExtractor

    # 创建PdfDocument类的对象并加载PDF文件
    pdf = PdfDocument()
    pdf.LoadFromFile(pdf_path)

    # 创建一个字符串对象来存储文本
    extracted_text = ""

    # 创建PdfExtractor对象
    extract_options = PdfTextExtractOptions()
    # 设置使用简单提取方法
    extract_options.IsSimpleExtraction = True

    # 循环遍历文档中的页面
    for i in range(pdf.Pages.Count):
        # 获取页面
        page = pdf.Pages.get_Item(i)
        # 创建PdfTextExtractor对象，并将页面作为参数传递
        text_extractor = PdfTextExtractor(page)
        # 从页面中提取文本
        text = text_extractor.ExtractText(extract_options)
        # 将提取的文本添加到字符串对象中
        extracted_text += text
    pdf.Close()

    return extracted_text.strip()


# 使用示例
if __name__ == '__main__':
    import time
    from request_llm import request_llm

    image_path = 'data\\pdf'
    # 遍历文件夹下的所有文件
    for file in os.listdir(image_path):
        # 拼接文件路径
        file_path = os.path.join(image_path, file)
        print(file_path)
        # 直接提取
        stat_time = time.time()
        text = spire_pdf_ocr(file_path)
        end_time = time.time()
        print(f"耗时{end_time - stat_time}秒\n{text}")
        # 调用LLM
        prompt = f'{text}'
        break
        result = request_llm(prompt)
        # 将识别结果存到文件,追加
        with open('data\\pdf\\pdf-ocr-result.txt', 'a+', encoding='utf-8') as f:
            f.write(text)
            f.write('\n')
            f.write(result)
            f.write('\n')
            f.write('=' * 20)
        f.close()

    # pdf_orc识别
    # stat_time = time.time()
    # text = pdf_ocr(pdf_path)
    # end_time = time.time()
    # print(f"耗时{end_time - stat_time}秒\n{text}")