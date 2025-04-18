import warnings,os
#from crewai_tools import RagTool
from abc import ABC, abstractmethod
from typing import Any,Optional, Dict,Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class Adapter(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def query(self, question: str) -> str:
        """Query the knowledge base with a question and return the answer."""

    @abstractmethod
    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Add content to the knowledge base."""


class RagTool(BaseTool):
    class _AdapterPlaceholder(Adapter):
        def query(self, question: str) -> str:
            raise NotImplementedError

        def add(self, *args: Any, **kwargs: Any) -> None:
            raise NotImplementedError
    
    # 新增参数模型定义
    class InputSchema(BaseModel):
        query: str
        kwargs: Dict[str, Any] = Field(default_factory=dict)

    name: str = "VASP知识库"
    description: str = "一个你可以用于检索以回答问题的VASP知识库"
    summarize: bool = False
    adapter: Adapter = Field(default_factory=_AdapterPlaceholder)
    config: dict[str, Any] | None = None
    args_schema: Type[BaseModel] = InputSchema  # 绑定参数模型

    @model_validator(mode="after")
    def _set_default_adapter(self):
        if isinstance(self.adapter, RagTool._AdapterPlaceholder):
            from embedchain import App

            from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter

            app = App.from_config(config=self.config) if self.config else App()
            self.adapter = EmbedchainAdapter(
                embedchain_app=app, summarize=self.summarize
            )

        return self

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.adapter.add(*args, **kwargs)

    def _run(
        self,
        query: str,
        #**kwargs: Any,
        kwargs: Optional[Dict[str, Any]] = None,  # 修改参数接收方式
    ) -> Any:
        
        # 设置默认空字典
        kwargs = kwargs or {}

        self._before_run(query, **kwargs)
        return f"相关信息:\n{self.adapter.query(query)}"

    def _before_run(self, query, **kwargs):
        pass



config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-2024-11-20",
        }
    },
    "embedding_model": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-ada-002",
        }
    },
    "chunker":{
        "chunk_size" : 500,
        "chunk_overlap" : 100,
        "min_chunk_size" : 120,
    }
}

rag_tool = RagTool(
    config=config,
    summarize=True
)


# 添加数据
#current_file = os.path.abspath(__file__)
#tool_root = os.path.dirname(current_file)
#file_path = os.path.join(tool_root, 'data_source','vasp-wiki.json')

#rag_tool.add(source=file_path, data_type="json")


# # example query
#result = rag_tool.run(query="What are the KPOINTS?")
#print(result)


