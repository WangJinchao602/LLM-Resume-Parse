'''
中文简历OCR识别
Author: wangjinchao
Date: 2025/08/14
'''
import os

from numpy.f2py.crackfortran import endifs


# 1. Paddle OCR https://blog.csdn.net/bugang4663/article/details/131569669?spm=1001.2014.3001.5501
# https://github.com/PaddlePaddle/PaddleOCR/blob/main/readme/README_cn.md
#  ch_pp-ocrv3
def paddle_ocr_v3(img_path):
    import paddlehub as hub
    import cv2

    ocr = hub.Module(name="l", enable_mkldnn=True)  # mkldnn加速仅在CPU下有效
    result = ocr.recognize_text(images=[cv2.imread(img_path)])

    # 使用列表推导式和join方法
    texts = [i['text'] for i in result[0]['data']]
    return '\n'.join(texts)

# def paddle_ocr_v3(img_path):
#     from paddleocr import PaddleOCR
#     import cv2
#     ocr = PaddleOCR(use_angle_cls=True, lang='ch')
#     result = ocr.ocr(img_path)
#     # 使用列表推导式和join方法
#     texts = [i['text'] for i in result[0]['data']]
#     return '\n'.join(texts)


# pp-ocrv5
# def paddle_ocr_v5(img_path):
#     from paddleocr import PaddleOCR
#
#     # 初始化 PaddleOCR 实例
#     ocr = PaddleOCR(
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False,
#         use_textline_orientation=False,
#         ocr_version='PP-OCRv4')
#
#     # 对示例图像执行 OCR 推理
#     result = ocr.predict(img_path)
#
#     for res in result:
#         res.print()
#         res.save_to_img("output")
#         res.save_to_json("output")
#
#     # 提取文本内容
#     text_results = []
#     if result is not None and result[0] is not None:
#         for line in result[0]:
#             # line[1][0] 是识别的文本内容
#             text_results.append(line[1][0])
#
#     # 将所有文本连接成一个字符串，用换行符分隔
#     final_text = '\n'.join(text_results)
#
#     return final_text

# PP-StructureV3
# def paddle_ocr_structuere_v3(img_path):
#     from pathlib import Path
#     from paddleocr import PPStructureV3
#
#     pipeline = PPStructureV3(
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False
#     )
#
#     # For Image
#     output = pipeline.predict(
#         input=img_path,
#     )
#
#     # 可视化结果并保存 json 结果
#     for res in output:
#         res.print()
#         res.save_to_json(save_path="output")
#         res.save_to_markdown(save_path="output")

# 2. CnOCR
# 项目地址：https://github.com/breezedeus/cnocr
# 介绍文档：https://cnocr.readthedocs.io/zh/latest/
def cn_ocr(img_path):
    from cnocr import CnOcr
    ocr = CnOcr()
    out = ocr.ocr(img_path)
    all_text = []
    for line in out:
        all_text.append((line["text"]))
    return '\n'.join(all_text)

# 3. chinese_lite OCR 需要API调用
# https://github.com/DayBreak-u/chineseocr_lite

# 4. EasyOCR
# https://www.jaided.ai/easyocr/install/
def easy_ocr(img_path):
    import easyocr

    # 创建 Reader 对象，指定语言为简体中文和英文
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

    # 读取图像并进行文字识别
    result = reader.readtext(img_path, detail = 0)

    # 输出识别结果
    return '\n'.join(result)

if __name__ == '__main__':
    import time
    from request_llm import request_llm
    image_path = 'data\\png'
    # 遍历文件夹下的所有文件
    for file in os.listdir(image_path):
        # 拼接文件路径
        file_path = os.path.join(image_path, file)
        # paddle_ocr_v3
        # start = time.time()
        ocr_result = cn_ocr(file_path)
        # end = time.time()
        # print(f'paddle_ocr_v3, {end - start}s\n{result}\n\n')
        print(ocr_result)
        # prompt = f'{ocr_result}'
        # result = request_llm(prompt)
        # # 将识别结果存到文件,追加
        # with open('data\\png\\easy-ocr-result.txt', 'a+', encoding='utf-8') as f:
        #     f.write(ocr_result)
        #     f.write('\n')
        #     f.write(result)
        #     print(result)
        #     f.write('\n')
        #     f.write('=' * 20)
        # f.close()

    # cn_ocr
    # start = time.time()
    # result = cn_ocr(image_path)
    # end = time.time()
    # print(f'cn_ocr, {end - start}s\n{result}\n\n')

    # easy_ocr
    # start = time.time()
    # result = easy_ocr(image_path)
    # end = time.time()
    # print(f'easy_ocr, {end - start}s\n{result}\n\n')