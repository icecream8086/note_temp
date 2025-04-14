import os
import glob
from urllib.parse import quote

def create_markdown_index(directory):
    """
    为指定目录创建Markdown索引文件，自动将空格转为%20
    :param directory: 要处理的目录
    """
    # 获取当前目录名称作为标题
    folder_name = os.path.basename(os.path.normpath(directory))
    
    # 查找目录中的所有.md文件（排除可能的索引文件）
    md_files = [f for f in glob.glob(os.path.join(directory, "*.md")) 
               if not f.endswith(f"{folder_name}.md")]
    
    if not md_files:
        print(f"目录 {directory} 中没有找到Markdown文件")
        return
    
    # 准备Markdown内容
    md_content = f"# {folder_name}\n\n## 包含的词类\n\n"
    
    for md_file in md_files:
        # 获取文件名（不带路径和扩展名）
        filename = os.path.splitext(os.path.basename(md_file))[0]
        # URL编码文件名（将空格转为%20）
        encoded_filename = quote(filename)
        # 添加链接（使用编码后的文件名）
        md_content += f"- [{filename}]({encoded_filename}.md)\n"
    
    # 创建索引文件
    index_file = os.path.join(directory, f"{folder_name}.md")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"已创建索引文件: {index_file}")

# 使用当前脚本所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))
create_markdown_index(current_directory)