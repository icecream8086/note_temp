import tiktoken
import argparse

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    计算字符串的 token 数量。

    :param text: 输入的字符串
    :param model_name: 使用的模型名称，默认为 "gpt-4"
    :return: token 数量
    """
    # 获取指定模型的分词器
    encoding = tiktoken.encoding_for_model(model_name)
    
    # 将文本编码为 token
    tokens = encoding.encode(text)
    
    # 返回 token 数量
    return len(tokens)

def count_tokens_in_file(file_path: str, model_name: str = "gpt-4") -> int:
    """
    计算文件中文本的 token 数量。

    :param file_path: 文件路径
    :param model_name: 使用的模型名称，默认为 "gpt-4"
    :return: token 数量
    """
    try:
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        
        # 计算 token 数量
        return count_tokens(text, model_name)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。")
        return 0
    except Exception as e:
        print(f"错误: 读取文件时发生错误 - {e}")
        return 0

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="计算文件中文本的 token 数量。")
    parser.add_argument("file_path", type=str, help="要计算 token 数量的文件路径")
    parser.add_argument("--model", type=str, default="gpt-4", help="使用的模型名称（默认为 'gpt-4'）")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 计算 token 数量
    token_count = count_tokens_in_file(args.file_path, args.model)
    print(f"文件 '{args.file_path}' 中的 Token 数量: {token_count}")

if __name__ == "__main__":
    main()