import os
from pathlib import Path
from openai import OpenAI

def request_llm(text):
    '''
    调用API处理
    '''
    import os
    from openai import OpenAI


    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    result_schema = """{
        "基本信息": {
            "姓名": "",
            "性别": "",
            "出生日期": "",
            "籍贯": "",
            "户口所在地": "",
            "现居住地": "",
            "民族": "",
            "婚姻状况": "",
            "政治面貌": "",
            "生源类型": "",
            "紧急联系电话": "",
            "当前薪资": ""
        },
        "教育经历": [
            {
                "起始日期": "",
                "结束日期": "",
                "学历": "",
                "是否在职期间获取": "",
                "学习形式": "提示：全日制、非全日制、在职、脱产、网络教育、自考、成人教育、夜大、电大、函授、业余、其他"",
                "学校名称": "",
                "专业名称": "",
                "学位": "",
                "在校期间成绩排名": "",
                "平均绩点": "",
                "研究方向": "",
            },
            // 可以有多个教育经历
        ]
        "在校期间获奖（包括奖学金）": [
            {
                "获奖名称": "如：奖学金；如：数学建模竞赛",
                "获奖时间": "",
                "获奖级别": "提示：国家级、省级、市级、校级、院级",           
            }
            // 可以有多个获奖经历
        ]
        "工作、实习情况经历": [
            {
                "起始日期": "",
                "结束日期": "",
                "公司名称": "",
                "所在部门": "",
                "工作类型": "提示：正式、非正式、合同、项目、实习、兼职",
                "职位": "",
            },   
            // 可以有多个工作经历   
        ]
        "项目经历": [
            {
                "起始日期": "",
                "结束日期": "",
                "项目名称": "",
                "职责": "提示：前端开发、后端开发、全栈开发、数据分析师、数据科学家、UI/UX设计师、项目管理等",
                "技术栈": "",
            },
            // 可以有多个项目经历
        ]
        "语言水平": [
            {
                "语种": "提示：英语、日语",
                "证书名称": "提示：CET-4、CET-6、托福、雅思、日语等级证书",
                "成绩": ""
            },
            // 可以有多个语言经历
        ]
        "计算机证书": [
            {
                "证书名称": "提示:计算机二级",
                "获得类别": "",
            },
            // 可以有多个计算机证书
        ]
        "其他职业资格证书": [
            {
                "证书名称": "", 
                "证书级别": "提示：初级、中级、高级、技师、高级技师",
            },
            // 可以有多个技能证书
        ]
        }"""

    prompt = f"""假设你是一名简历信息提取专家。现提供一个JSON Schema，要求根据简历文档中的信息填充Schema中的数值字段。
            注意：1.Schema中一级字段"基本信息"、"教育经历"、"工作、实习情况经历"、"获奖情况"、"语言情况"、"计算机证书"、"其他职业资格证书"为必填字段，二级字段为可选字段。
            2.Schema中的二级字段名称和提示信息仅供参考，实际字段名称和提示信息可能和Schema中的不一致（语义相似即可）。
            3.若简历文档中未包含Schema中的二级字段，则该字段的值为空字符串。
            4.计算机证书，不是技能，如熟悉数据库原理、熟悉***
            最终仅需输出合法的JSON格式结果，严格遵守所见即所得原则（输出语言必须与文档内容保持一致），无需任何解释说明。
            请按要求输出结果，简历信息如下{text}, 输出JSON Schema内容如下：{result_schema}。"""

    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen3-4b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        extra_body={"enable_thinking": False},
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content
