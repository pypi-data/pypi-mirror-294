"""
解释器文件名：
    Windows - python.exe
    Linux   - python3
    MacOS   - python3

重点：
    对 Python 来说 Linux 或 MacOS 似乎是一样的，系统类型都被识别为 "Linux"。

"""

import os
import sys
import base64
import pickle
import re
import platform


def get_pythonpaths():
    """兼容Linux与Windows，Linux未测试"""
    # 获取系统类型
    system_type = platform.system()
    # 获取 PATH 环境变量
    path_variable = os.environ.get('PATH', '')
    # 根据系统类型确定路径分隔符
    pathsep = os.pathsep if system_type == 'Windows' else ':'
    # 将 PATH 环境变量分割为列表
    path_list = path_variable.split(pathsep)
    # 创建一个空字典来存储 Python 路径
    python_paths_dict = {}
    # 根据系统类型设置不同的正则表达式
    if system_type == 'Windows':
        regex_pattern = r'Python(\d+)[/\\]$'
    else:
        regex_pattern = r'(Python(\d+\.\d+)|python(\d+\.\d+))[/\\]$'
    
    # 正则表达式匹配路径
    for path in path_list:
        match = re.search(regex_pattern, path)
        if match:
            version = match.group(1) if system_type == 'Windows' else (match.group(2) or match.group(3))
            python_paths_dict[version] = path
    return python_paths_dict

def transfer_obj_to_base64(obj):
    serialized_data = pickle.dumps(obj)
    encoded_data = base64.b64encode(serialized_data).decode('utf-8')
    return encoded_data

def transfer_base64_to_obj(obj_string):
    decoded_bytes = base64.b64decode(obj_string.encode('utf-8'))
    original_data = pickle.loads(decoded_bytes)
    return original_data

def call_python(python_path, script_path, params):
    """
    # 构建命令，例如 'python38/Scripts/python.exe your_script.py arg1 arg2'
    # 传的参数必须是 Python 标准数据类型（数字、字符串、列表、字典等），不能是自定义对象。
    """
    system_type = platform.system()
    
    args = []
    for param in params:
        obj_string = transfer_obj_to_base64(param)
        args.append(obj_string)

    if system_type == 'Windows':
        command = '%s\Scripts\python.exe %s %s' % (python_path, script_path, ' '.join(args))

    elif system_type == 'Linux':
        command = '%s/Scripts/python3 %s %s' % (python_path, script_path, ' '.join(args))

    # 使用 os.popen 执行命令
    process = os.popen(command)
    output = process.read()
    process.close()

    return transfer_base64_to_obj(output)

def call_version(version, script_path, params):
    # version 目前windwos下是 3xx, Linux 下是 3.xx
    system_type = platform.system()
    
    version = str(version)
    # version = ''.join(filter(str.isdigit, version))
    args = []
    for param in params:
        obj_string = transfer_obj_to_base64(param)
        args.append(obj_string)

    pathon_paths = get_pythonpaths()

    if system_type == 'Windows':
        command = '%spython.exe %s %s' % (pathon_paths[version], script_path, ' '.join(args))
    elif system_type == 'Linux':
        command = '%spython.exe %s %s' % (pathon_paths[version], script_path, ' '.join(args))

    # 使用 os.popen 执行命令
    process = os.popen(command)
    output = process.read()
    process.close()

    return transfer_base64_to_obj(output)


def get_params():
    """被外部解释器调用的 python 文件通过该函数获取外部解释器传入的参数。"""
    args = sys.argv[1:]

    objs = []
    for arg in args:
        obj = transfer_base64_to_obj(arg)
        objs.append(obj)

    return objs

def return_data(data):
    result = transfer_obj_to_base64(data)
    print(result) 









