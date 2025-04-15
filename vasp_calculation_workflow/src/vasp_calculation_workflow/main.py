#!/usr/bin/env python
import os,re,subprocess
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start,router
from vasp_calculation_workflow.crews.pos_validator.pos_validator import PosValidator
from vasp_calculation_workflow.crews.parameter_configurator.parameter_configurator import ParameterConfigurator
from vasp_calculation_workflow.crews.vaspkit_crew.vaspkit_crew import VaspkitCrew
# 定义流程状态模型
class VaspState(BaseModel):
    poscar: str = ""
    incar: str = ""
    kpoints: str = ""

class VaspCalculationFlow(Flow[VaspState]):
    """vasp计算工作流"""
    def _get_poscar_path(self):
        """动态解析POSCAR文件路径"""
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        return os.path.join(project_root, 'vasp', 'POSCAR')

    def _read_car(self, path: str) -> str:
        """安全读取POSCAR文件内容"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"POSCAR文件不存在于路径: {path}")
        except UnicodeDecodeError:
            raise RuntimeError("文件编码错误，请确保使用UTF-8格式")
    @start()
    def getposcar(self):
        print("\n正在获取结构文件\n")
                # 获取解析后的路径
        poscar_path = self._get_poscar_path()
        print(f"解析到POSCAR路径: {poscar_path}")
        
        # 读取并验证文件内容
        try:
            self.state.poscar = self._read_car(poscar_path)
            print("成功加载POSCAR内容")
            print(f"\n{self.state.poscar}")
        except RuntimeError as e:
            print(f"错误: {str(e)}")

        return self.state
    
    
    @router(getposcar)
    def validator(self,state):
        val_result = PosValidator().crew().kickoff(inputs={"poscar": state.poscar})
        print(f"\nPOSCAR的验证结果为：\n{val_result.raw}\n ")
        
        while True:
            answer = input("是否维持原POSCAR提交?(y/n)")
            if answer in ["y","Y","N","n"]: break      
            print("请输入y,Y,n或N:")
        
        if answer in ["Y","y"]:
            return "continue"
        else:
            return "stop"
        
    @listen("stop")
    def finish(self,state):
        print("----------工作结束，请修改POSCAR文件--------\n")
        return

    @listen("continue")
    @router(validator)
    def llm_or_vaspkit(self,state):             #路由分支，使用vaspkit或是gpt-o1
        while True:
            answer = input("是否使用Vaspkit?(y/n)，若否则调用gpt-o1生成参数:")
            if answer in ["y","Y","N","n"]: break      
            print("请输入y,Y,n或N:")
        
        if answer in ["Y","y"]:
            return "vaspkit"
        else:
            return "llm"
        

    @listen("vaspkit")
    def vaspkit_agent_generate(self,state):
        parameter_result = VaspkitCrew().crew().kickoff(inputs={"poscar": state.poscar}) #调用生成参数代理
        print(f"\nVaspkit调用说明：\n{parameter_result.raw}\n ")
        ###更新状态
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        incar_path = os.path.join(project_root, 'vasp', 'INCAR')
        kpoints_path = os.path.join(project_root, 'vasp', 'KPOINTS')
        self.state.incar = self._read_car(incar_path)
        self.state.kpoints = self._read_car(kpoints_path)

        return "vaspkit over"


        
    @listen("llm")
    def parameter_generate(self,state):

        parameter_result = ParameterConfigurator().crew().kickoff(inputs={"poscar": state.poscar}) #调用生成参数代理
        parameter_content = parameter_result.raw
        print(f"\n生成参数内容为:\n{parameter_content}\n")
        # 使用正则表达式匹配内容
        pattern = r'KPOINTS:\s*```(.*?)```.*?INCAR:\s*```(.*?)```'
        match = re.search(pattern, parameter_content, re.DOTALL)

        #存储kpoints和incar到state
        kpoints = match.group(1).strip() if match else ''
        incar = match.group(2).strip() if match else ''
        self.state.kpoints = kpoints
        self.state.incar = incar

        print(f"\nKPOINTS:\n{kpoints}\nINCAR:\n{incar}\n")

        #参数写入文件中
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        with open(os.path.join(project_root, 'vasp', 'KPOINTS'), 'w', encoding='utf-8', newline='\n') as f: 
            f.write(self.state.kpoints)
        with open(os.path.join(project_root, 'vasp', 'INCAR'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(self.state.incar)

        print("\n已将参数写入KPOINTS和INCAR中")




        vasproot = os.path.join(project_root,'vasp')
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
            

def kickoff():
    """Run the guide creator flow"""
    VaspCalculationFlow().kickoff()
    print("\n=== 工作流结束 ===")
    print("计算已提交，请到bohrium平台等待结果.")

def plot():
    """Generate a visualization of the flow"""
    flow = VaspCalculationFlow()
    flow.plot("VaspCalculationFlow")
    print("可视化工作流保存至 VaspCalculationFlow.html")




if __name__ == "__main__":
    kickoff()
