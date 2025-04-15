import os
import re
from pathlib import Path

def replace_latex_delimiters_in_file(file_path):
    """替换单个文件中的 LaTeX 分隔符"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 '\\( ' 和 ' \\)' 为 '$'
    content = re.sub(r'\\\(\s', r'$', content)  # 处理 '\\( '
    content = re.sub(r'\s\\\)', r'$', content)  # 处理 ' \\)'
    
    # 替换 '\\[' 和 '\\]' 为 '$$'
    content = re.sub(r'\\\[', r'$$', content)   # 处理 '\\['
    content = re.sub(r'\\\]', r'$$', content)   # 处理 '\\]'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory='.'):
    """处理目录及其子目录下的所有.md文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                print(f"处理文件: {file_path}")
                try:
                    replace_latex_delimiters_in_file(file_path)
                except Exception as e:
                    print(f"处理 {file_path} 时出错: {e}")

if __name__ == '__main__':
    print("开始处理 Markdown 文件中的 LaTeX 分隔符...")
    process_directory()
    print("处理完成！")