import os

def convert_incar_to_unix_format():
    # 检查当前目录是否存在INCAR文件

    current_file = os.path.abspath(__file__)
    root = os.path.dirname(current_file)
    incar_path = os.path.join(root, 'INCAR')
    
    if not os.path.exists(incar_path):
        print("错误：未找到INCAR文件！")
        return

    # 读取文件内容（自动处理原始换行符）
    with open(incar_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用Unix换行符重写文件
    with open(incar_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print("INCAR文件已成功转换为Unix换行格式！")

if __name__ == "__main__":
    convert_incar_to_unix_format()