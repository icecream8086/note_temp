import os
from openai import OpenAI
import uuid

def read_key_from_file(file_path="key.txt"):
    """
    从指定文件读取密钥并返回其内容
    :param file_path: 文件路径，默认为key.txt
    :return: 密钥内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            key = file.read().strip()  # 读取文件内容并去除首尾空白字符
        return key
    except FileNotFoundError:
        return "Error: 文件未找到。请检查文件路径是否正确。"
    except Exception as e:
        return f"Error: 读取文件时发生异常。详细信息: {e}"

# 读取API密钥
key = read_key_from_file()

# 初始化OpenAI客户端
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

# 系统提示信息
system_info_note = '''

'''

def chat_completion_response(system_infos, user_inputs, model="deepseek-reasoner", stream=False):
    """
    生成聊天完成响应。

    参数：
    system_info (str): 系统信息。
    user_input (str): 用户输入。
    model (str): 使用的模型名称，默认为 "deepseek-reasoner"。
    stream (bool): 是否流式传输响应，默认为 False。

    返回值：
    str: 聊天完成响应的内容。
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_infos},
            {"role": "user", "content": user_inputs},
        ],
        stream=stream
    )
    return response.choices[0].message.content

def read_md_file(file_path):
    """
    从磁盘读取Markdown文件并返回其内容。

    :param file_path: Markdown文件的路径
    :return: 文件内容
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def save_to_markdown(content, filename):
    """
    将输入字符保存为Markdown文件
    :param content: 要保存的字符内容
    :param filename: 保存的文件名
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"文件已保存为 {filename}")

def process_all_md_files(md_folder, output_folder):
    """
    处理指定文件夹下的所有Markdown文件，并将结果保存到输出文件夹。

    :param md_folder: 包含Markdown文件的文件夹路径
    :param output_folder: 输出文件的文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历Markdown文件夹中的所有文件
    for filename in os.listdir(md_folder):
        if filename.endswith(".md"):
            md_file_path = os.path.join(md_folder, filename)
            print(f"正在处理文件: {md_file_path}")

            # 读取Markdown文件内容
            content = read_md_file(md_file_path)

            # 调用API处理内容
            final_response = chat_completion_response(system_info_note, content)

            # 保存处理结果到输出文件夹
            output_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.md")
            save_to_markdown(final_response, output_filename)

# 设置Markdown文件夹和输出文件夹路径
md_folder = "mdoc"  # Markdown文件所在的文件夹
output_folder = "output"  # 输出文件的文件夹

# 处理所有Markdown文件
process_all_md_files(md_folder, output_folder)