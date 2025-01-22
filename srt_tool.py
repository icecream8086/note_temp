# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import concurrent.futures
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

key = read_key_from_file()

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
file_path = 'example.srt'
system_info_wash_srt='''### 提示词：字幕输出专家助手

#### 定位
你是一位智能助手，专注于字幕输出和内容生成。你的目标是帮助用户从视频中提取字幕并进行内容整理、总结和呈现。

#### 能力
- 提取和识别视频中的字幕
- 分析和总结字幕内容
- 生成结构化、易于理解的内容摘要

#### 知识储备
- 深入了解视频字幕提取技术
- 熟悉字幕文件格式和处理方法
- 擅长内容总结和信息整理

#### 提示词示例
用户需求：生成视频字幕的摘要

#### 指令
1. 提取视频中的所有字幕内容。
2. 根据字幕内容，生成结构化的摘要，分为不同的部分，每部分包含时间戳和对应的主题。
3. 确保生成的摘要清晰、精确、易于理解，并尽可能简洁。

#### 输出格式示例
```markdown
### 视频字幕摘要

#### 一、操作系统中的进程和虚拟化概念，以及系统调用的应用
- **00:01** 操作系统课的内容包括系统调用和进程虚拟化
- **01:09** INIT进程创建了计算机系统中的一切，包括硬件和软件
- **02:31** 虚拟化是指进程在虚拟机中运行，每个进程都是虚拟出来的

#### 二、操作系统中的对象概念
- **08:24** 操作系统对象是字节序列，可以通过cat命令查看
- **10:31** 操作系统对象可以通过指针或引用来访问，需要有操作系统指针
- **11:43** 操作系统对象包括硬件、文件、进程地址空间等

#### 三、操作系统对象的概念
- **16:42** 文件描述符指向操作系统对象的一种指针
- **18:31** Windows操作系统中，句柄是handle，表示对文件或对象的引用
- **22:35** 管道是一种操作系统对象，类似于缓冲区

#### 四、如何使用管道和命名管道的概念
- **25:01** 系统调用和UNIX Shell的介绍
- **27:01** 命名管道和匿名管道的区别
- **31:12** 管道是一个进程间的同步机制

#### 五、Unix系统中的管道和匿名管道的使用方法
- **33:20** 管道的快慢和同步问题
- **35:47** 匿名管道的使用方法
- **39:20** 进程状态机和操作系统内部状态的关系

#### 六、操作系统的基本概念和系统调用
- **41:41** 如果成功，将打印消息，并等待子进程结束
- **44:10** 操作系统提供的系统调用可以构建整个UNIX系统
'''

system_info_note='''
# 笔记助手提示词

你是一位笔记助手，专注于从讲课内容和书本信息中提取和组织关键信息。你的能力包括：

- **总结**：简明扼要地概括内容的目的、方法、结果和结论。
- **主题提炼**：突出主要内容和核心方法，添加关键词和问题提示。
- **重点难点识别**：找出并列出关键的重点和难点。
- **结构化记录**：系统地记录知识点，组织内容使其条理清晰。
- **总结与扩展**：提供便于快速回顾的总结，并在此基础上引申考点、重点和难点。

请使用以下模板，根据提供的输入内容生成笔记。

---

# 标题

## 摘要

简述目的、方法、结果和结论。

## 主题

概括主要内容和核心方法，添加关键词和问题提示，文本应简洁明了。

> 重点难点
>
> - 列出重点难点1
> - 列出重点难点2

## 线索区

记录讲课内容或书本信息。

### 知识点1
    适当美化输出内容，可以插入latex (如果有的话)
    
### 知识点2

## 总结区

总结本页信息，便于快速回顾，并引申考点、重点和难点。

---

'''


def chat_completion_response(system_infos, user_inputs, model="deepseek-chat", stream=False):
    """
    生成聊天完成响应。

    参数：
    system_info (str): 系统信息。
    user_input (str): 用户输入。
    model (str): 使用的模型名称，默认为 "deepseek-chat"。
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

def read_srt_file(file_path):
    """
    从磁盘读取SRT文件并返回所有行的列表。

    :param file_path: SRT文件的路径
    :return: 包含SRT文件所有行的列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def split_into_chunks(lines, chunk_size=800, min_chunk_size=100):
    """
    将SRT文件的行列表按照指定大小分割成多个块。

    :param lines: SRT文件的所有行
    :param chunk_size: 每个块的行数，默认为800
    :param min_chunk_size: 最后一个块的最小行数，默认为100
    :return: 包含多个字符数组的列表
    """
    chunks = []
    for i in range(0, len(lines), chunk_size):
        # 如果剩余行数不足min_chunk_size，则并入最后一个块
        if len(lines) - i < min_chunk_size and len(chunks) > 0:
            chunks[-1].extend(lines[i:])
        else:
            chunks.append(lines[i:i + chunk_size])
    return chunks

def process_srt_file(file_path):
    """
    处理SRT文件，将其分割成多个字符数组。

    :param file_path: SRT文件的路径
    :return: 包含多个字符数组的列表
    """
    # 读取SRT文件
    lines = read_srt_file(file_path)
    
    # 将文件内容分割成多个块
    chunks = split_into_chunks(lines)
    
    # 将每个块转换为字符数组
    char_arrays = [''.join(chunk) for chunk in chunks]
    
    return char_arrays


# print(chat_completion_response(system_info, user_input))

# chat_completion_response(system_info, user_input)

def get_responses(system_info, char_arrays, max_threads=3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for i in range(len(char_arrays)):
            user_input = char_arrays[i]
            futures.append(executor.submit(chat_completion_response, system_info, user_input))

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            char_arrays[i] = future.result()

char_arrays = process_srt_file(file_path)

get_responses(system_info_wash_srt, char_arrays)

# print(char_arrays)
def save_to_markdown(content, filenames):
    """
    将输入字符保存为Markdown文件
    :param content: 要保存的字符内容
    :param filename: 保存的文件名，默认为output.md
    """
    with open(filenames, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"文件已保存为 {filenames}")
    
chars = ""
for i, char_array in enumerate(char_arrays):
    print(f"Chunk {i + 1}:\n{char_array}\n")
    chars += ''.join(char_array)

print(f"最终合并的字符串: {chars}")

final_response=chat_completion_response(system_info_note,chars)

filename=""+str(uuid.uuid4())+".md"


save_to_markdown(final_response,filename)
