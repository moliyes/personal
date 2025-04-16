import warnings,os
from crewai_tools import RagTool

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4",
        }
    },
    "embedding_model": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
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
current_file = os.path.abspath(__file__)
tool_root = os.path.dirname(current_file)
file_path = os.path.join(tool_root, 'data_source','vasp-wiki.json')


rag_tool.add(source=file_path, data_type="json")


# # example query
#result = rag_tool.run(query="What are the key findings?", num_results=5, verbose=True)
#print(result)


