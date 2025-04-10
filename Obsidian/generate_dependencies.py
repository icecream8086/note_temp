import re
import json

def parse_mermaid(graph_path):
    nodes = {}  # 存储所有节点ID到名称的映射
    deps = {}   # 存储依赖关系 {from_id: [to_ids]}

    # 增强型正则表达式（同时解析箭头两侧的节点定义）
    node_pattern = re.compile(r'(\w+)(?:\["(.+?)"\])?')  # 匹配节点ID和可选描述
    arrow_pattern = re.compile(r'(\w+)(?:\[".+?"\])?\s*-->\s*(\w+)(?:\["(.+?)"\])?')

    with open(graph_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('%%'):
                continue

            # 处理所有节点定义（包括箭头行中的定义）
            for node_id, node_name in re.findall(node_pattern, line):
                if node_id not in nodes and node_name:  # 仅当有描述时记录名称
                    nodes[node_id] = node_name
                elif node_id not in nodes:
                    nodes[node_id] = ""  # 保留未命名节点

            # 解析箭头关系
            if arrow_match := arrow_pattern.search(line):
                from_id, to_id, to_name = arrow_match.groups()
                
                # 更新右侧节点名称（如果存在描述）
                if to_name:
                    nodes[to_id] = to_name
                
                # 记录依赖关系
                if from_id in nodes:
                    deps.setdefault(from_id, []).append(to_id)

    # 构建最终结构（仅保留有名称的节点）
    output = {"nodes": {}}
    for node_id, node_name in nodes.items():
        if not node_name:
            continue  # 跳过未命名节点
        
        output["nodes"][node_name] = {
            "post": [nodes[t] for t in deps.get(node_id, []) if t in nodes and nodes[t]]
        }

    return output

if __name__ == "__main__":
    result = parse_mermaid("graph.ini")
    
    with open('md_dependencies.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("解析完成，结果已保存到 md_dependencies.json")