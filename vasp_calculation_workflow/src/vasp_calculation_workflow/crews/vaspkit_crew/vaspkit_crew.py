from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from vasp_calculation_workflow.tools.vaspkit_tool import VaspkitTool


@CrewBase
class VaspkitCrew():
    """VaspkitCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def vaspkit_operator(self) -> Agent:
        return Agent(
            config=self.agents_config['vaspkit_operator'],
            tools = [VaspkitTool()],
            llm = LLM(model="deepseek/deepseek-chat",base_url="https://vip.apiyi.com/v1"),
            verbose=True
        )

    @task
    def vaspkit_task(self) -> Task:
        return Task(
            config=self.tasks_config['vaspkit_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VaspkitCrew crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
