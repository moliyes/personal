from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory, ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai import LLM
from vasp_calculation_workflow.tools.RagTool import rag_tool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ParameterConfigurator():
    """ParameterConfigurator crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def parameter_configurator(self) -> Agent:
        return Agent(
            config=self.agents_config['parameter_configurator'],
            tools=[rag_tool],
            verbose=True,
            llm = LLM(model="deepseek/deepseek-v3-0324",base_url="https://vip.apiyi.com/v1")
            #llm = LLM(model="openai/o3-mini-2025-01-31")# call model by provider/model_name

                   
        )


    @task
    def configuration_task(self) -> Task:
        return Task(
            config=self.tasks_config['configuration_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ParameterConfigurator crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = True
        )
