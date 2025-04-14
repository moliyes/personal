from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class vaspkit_input(BaseModel):
    """Input schema for MyCustomTool."""
    Code: str = Field("SR",description="vaspkit计算类型代号,计算类型代号列表如下：ST) Static-Calculation,SR) Standard Relaxation,LR) Lattice Relaxation,MG) Magnetic Properties,D3) DFT-D3 no-damping Correction,默认为SR,可以选择其中的一个或多个选项，例如LRD3")


class VaspkitTool(BaseTool):
    name: str = "vaspkit计算参数生成器"
    description: str = ("接受特定的计算类型代号作为参数，该工具被调用后自动在指定文件夹根据PSCAR生成用于结构优化的INCAR和KPOINTS" )
    args_schema: Type[BaseModel] = vaspkit_input

    def _run(self, Code: str) -> str:
        # Implementation goes here
        




        return "this is an example of a tool output, ignore it and move along."
