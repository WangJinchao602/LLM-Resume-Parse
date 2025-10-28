'''
# -*- coding: utf-8 -*-
简历内容解析类
'''
from zipfile import ZipFile

class ResumeParser:
    def __init__(self, resume_path):
        self.resume_path = "" # 简历路径

    # 解析简历 从docx中提取文本 返回字符串
    def parse_docx(self):
        pass


if __name__ == "__main__":
    resume_path = "D:/resume.docx"
    resume_parser = ResumeParser(resume_path)
    resume_parser.parse_docx()