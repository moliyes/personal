from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from vasp_calculation_workflow.tools.RagTool import rag_tool

@CrewBase
class VASPRAG():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def vasp_expert(self) -> Agent:
        '''pw
        This agent uses the RagTool to answer questions about the knowledge base.
        '''
        return Agent(
            config=self.agents_config["vasp_expert"],
            allow_delegation=False,
            tools=[rag_tool]
        )


    @task
    def vasp_rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['vasp_rag_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the rag crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # 加载 .env 文件
    load_dotenv()

    # 获取环境变量
    openai_api_key = os.getenv('OPENAI_API_KEY')
    database_url = os.getenv('OPENAI_API_BASE')
    # Example usage
    vasp_rag = VASPRAG()
    rag_crew = vasp_rag.crew()
    rag_crew.kickoff(inputs={
  "query": "What are the keys?"})    