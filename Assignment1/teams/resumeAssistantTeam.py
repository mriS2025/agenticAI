
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination


from agents.somResumeProcessingAgent import getSOMResumeProcessingAgent
from agents.somJDProcessingAgent import getSOMJDProcessingAgent
from agents.planningAgent import getPlanningAgent
from agents.visualizationAgent import getVisualizationAgent 

from teams.jdProcessingteam import getJDProcessingTeam
from teams.resumeProcessingTeam import getResumeProcessingTeam

selector_prompt = '''
Select an agent to perform the task.

{roles}

current conversation history :
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
you will be getting Resume(uploaded_resume) and Job description(uploaded_JD) and both will be available in your working directory 
Please read both files from the filesystem and provide tailored feedback on how to improve the resume.
Make sure that the planning agent has assigned task before other agents start working.
Only select one agent.
'''

def getResumeAssistantTeam(model_client, resume_path, jd_path):

    planning_agent = getPlanningAgent(model_client)
    resumeTeam=getResumeProcessingTeam(model_client,resume_path)

    som_resume_processing = getSOMResumeProcessingAgent(resumeTeam, model_client)

    jdTeam=getJDProcessingTeam(model_client, jd_path)

    som_job_description_processing=getSOMJDProcessingAgent(jdTeam,model_client)

    visualization_agent=getVisualizationAgent(model_client)

    finalText_mention_termination = TextMentionTermination('STOP')
    max_message_termination = MaxMessageTermination(max_messages=20)
    combined_termination = finalText_mention_termination | max_message_termination

    selector_team = SelectorGroupChat(
    participants=[planning_agent, som_resume_processing, som_job_description_processing, visualization_agent],
    model_client=model_client,
    termination_condition=combined_termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=True)

    return selector_team





