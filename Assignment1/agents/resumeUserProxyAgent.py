from autogen_agentchat.agents import UserProxyAgent


RESUME_USER_PROXY_SYSTEM_MESSAGE='''

You are a User Proxy agent for Resume Processing team. you have resume processing agent and resume scoring agent in you team. 
Review the score provided to you and reply with feedback. If all good, reply with APPROVE

Once we have completed all the task, please mention 'STOP' after explaning in depth the final answer.


Stick to these and ensure a smooth collaboration with resume_processing_agent and resume_scoring_agent.
'''


def getResumeUserProxyAgent(input_data):
    resumeUser_proxy_agent = UserProxyAgent(
        name='ResumeUser_proxy_agent',
        description = 'You are a user proxy agent for Resume Processing team',
        input_func=input_data
    )
    return resumeUser_proxy_agent
