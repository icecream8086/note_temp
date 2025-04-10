import json
import os

def append_post_links():
    # 读取JSON文件
    with open('md_dependencies.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nodes = data['nodes']
    
    # 遍历当前目录下所有.md文件
    for filename in os.listdir('.'):
        if not filename.endswith('.md'):
            continue
        
        # 提取不带扩展名的文件名作为键
        file_key = os.path.splitext(filename)[0]
        
        # 查找对应的post条目
        if file_key not in nodes:
            continue
        
        post_items = nodes[file_key].get('post', [])
        if not post_items:
            continue
        
        # 生成要追加的链接内容
        links = []
        for item in post_items:
            # 将路径中的空格替换为%20
            encoded_item = item.replace(' ', '%20')
            md_link = f"[{item}]({encoded_item}.md)"
            links.append('\n'+md_link + '\n')  # 每个链接占一行
        
        # 追加内容到文件末尾
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n')  # 添加空行分隔原有内容
            f.writelines(links)

if __name__ == '__main__':
    append_post_links()