from autogen_agentchat.agents import AssistantAgent

PLANNING_AGENT_SYSTEM_MESSAGE='''

You are a planning agent.
Your job is to break down complex tasks into smaller, manageable subtasks.
Your team members are:
    somResumeProcessingAgent: processes resume and gives score
    somJDProcessingAgent: processes job description and compares against resume

You only plan and delegate tasks - you do not execute them yourself.

When assigning tasks, use this format:
    1. <agent> : <task>

After all tasks are complete, if visualization agent gave good visualization end with "STOP".
'''


def getPlanningAgent(model_client):
    planning_agent = AssistantAgent(
        name='PlanningAgent',
        model_client=model_client,
        description = 'An agent for planning tasks, this agent should be the first to engage when given a new task.',
        system_message=PLANNING_AGENT_SYSTEM_MESSAGE
    )
    return planning_agent