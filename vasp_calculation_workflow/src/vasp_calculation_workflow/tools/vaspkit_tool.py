import os,pexpect
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class Vaspkit_input(BaseModel):
    """Input schema for MyCustomTool."""
    Code: str = Field("SR",description="vaspkit计算类型代号,计算类型代号列表如下：ST) Static-Calculation,SR) Standard Relaxation,LR) Lattice Relaxation,MG) Magnetic Properties,D3) DFT-D3 no-damping Correction,默认为SR,可以选择其中的一个或多个选项，例如LRD3")
    is_Hexagonal: str = Field("1",description="是六方晶系结构，则取'2',否则取'1'")

class VaspkitTool(BaseTool):
    name: str = "vaspkit计算参数生成器"
    description: str = ("接受特定的计算类型代号作为参数，该工具被调用后自动在指定文件夹根据PSCAR生成用于结构优化的INCAR和KPOINTS" )
    args_schema: Type[BaseModel] = Vaspkit_input

    def _execute_vaspkit_flow(self, cwd: str, command_flow: list):
        """执行VASPkit交互流程"""
        try:
            child = pexpect.spawn("vaspkit", cwd=cwd, timeout=50, encoding="utf-8")
            
            for prompt, response in command_flow:
                child.expect(r".+")
                child.sendline(response)
            
            child.expect(pexpect.EOF)
            return True
        except Exception as e:
            print(f"执行失败: {str(e)}")
            return False
        
    def _run(self, Code: str, is_Hexagonal:str) -> str:
        current_file = os.path.abspath(__file__)
        work_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
        cwd=os.path.abspath(os.path.join(work_dir, "vasp2"))

                # 验证目录
        if not os.path.isdir(cwd):
            return f"错误：工作目录 {cwd} 不存在"

        # 生成INCAR
        incar_flow = [
            ("主菜单提示", "01"),   # 进入01)VASP Input-Files Generator
            ("子菜单提示", "101"),  # 101) Customize INCAR File
            ("参数输入提示", Code)  # 输入计算类型
        ]
        
        # 生成KPOINTS
        kpoints_flow = [
            ("主菜单提示", "01"),   # VASP Input-Files Generator
            ("子菜单提示", "102"),  # Generate KPOINTS File for SCF Calculation 
            ("晶系选择提示", is_Hexagonal), # 1) Monkhorst-Pack Scheme 2) Gamma Scheme   
            ("精度提示", "0.02")# Accuracy Levels: Gamma-Only: 0;  Low: 0.06~0.04;  Medium: 0.04~0.03; Fine: 0.02-0.01.
        ]

        # 执行流程
        if not self._execute_vaspkit_flow(cwd, incar_flow):
            return "INCAR生成失败"
            
        if not self._execute_vaspkit_flow(cwd, kpoints_flow):
            return "KPOINTS生成失败"

        return f"文件生成成功！目录：{cwd}"
    

if __name__ == "__main__":
    # 创建测试工具实例
    vaspkit_tool = VaspkitTool()
    
    # 定义测试参数（使用默认值）
    test_params = {
        "Code": "SRD3",          # 测试标准弛豫
        "is_Hexagonal": "1"    # 测试立方晶系
    }
    
    # 运行测试
    print("🔄 正在生成VASP输入文件...")
    result = vaspkit_tool._run(**test_params)
    
    # 输出结果
    print("\n" + "="*40)
    if "成功" in result:
        print(f"✅ 测试结果：{result}")
        print(f"请检查 {os.path.abspath('vasp2')} 目录中的 INCAR 和 KPOINTS 文件")
    else:
        print(f"❌ 测试失败：{result}")
        print("可能的问题：")
        print("- 请确保已安装 vaspkit 并添加到环境变量")
        print("- 检查工作目录是否存在：vasp2/")
        print("- 确认晶系参数与结构文件匹配")