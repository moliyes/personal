import os,re,subprocess

def get_poscar_path():
    """动态解析POSCAR文件路径"""
        # 获取当前文件绝对路径
    current_file = os.path.abspath(__file__)
        # 计算项目根目录：向上三级到vasp_calculation_workflow
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(current_file)
        )
    )
        # 构建POSCAR完整路径
    return os.path.join(project_root, 'vasp', 'POSCAR')

def read_poscar(path: str) -> str:
    """安全读取POSCAR文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"POSCAR文件不存在于路径: {path}")
    except UnicodeDecodeError:
        raise RuntimeError("文件编码错误，请确保使用UTF-8格式")
    
def getposcar():
    print("\n正在获取结构文件\n")
                # 获取解析后的路径
    poscar_path = get_poscar_path()
    print(f"解析到POSCAR路径: {poscar_path}")
        
        # 读取并验证文件内容
    try:
        poscar = read_poscar(poscar_path)
        print("成功加载POSCAR内容")
        print(f"\n{poscar}")
    except RuntimeError as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    vasproot = os.path.join(project_root,'vasp')

    print(f"{vasproot}")

    # 构建命令参数
    command = [
        "bohr",
        "job",
        "submit",
        "-i", os.path.abspath(os.path.join(vasproot, "job.json")),  # 完整路径
        "-p", os.path.abspath(vasproot)  # 目录绝对路径
    ]

    try:
        # 安全执行命令（推荐使用列表形式避免shell注入）
        result = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("命令执行成功！输出：\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败（状态码 {e.returncode}）:")
        print("错误输出：\n", e.stderr)
    except FileNotFoundError:
        print("错误：未找到 bohr 命令，请确保：")
        print("1. bohr 已正确安装\n2. 已添加到系统PATH环境变量\n3. 当前终端会话可识别bohr")



