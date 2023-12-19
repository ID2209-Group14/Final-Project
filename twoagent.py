from autogen import AssistantAgent, UserProxyAgent


config_list = [
     {
        "model": "palm/chat-bison",
        "base_url": "http://localhost:8000",
        "api_key": "NULL",
    }

]
llm_config = {"timeout": 600, "config_list": config_list, "temperature": 0.5}


assistant = AssistantAgent("assistant", llm_config=llm_config, system_message="you are an AI assistant", human_input_mode="NEVER")
BOSS = AssistantAgent("boss", llm_config=llm_config, system_message="a boss, to be served with daily issue",human_input_mode="NEVER")

assistant.send(recipient=BOSS, message="what can i do for you?", request_reply=True)
message = BOSS.last_message(assistant)
# print(message)
BOSS.generate_reply(sender=assistant, messages=[message])
# print(reply)
# BOSS.send(recipient=assistant, message=reply)
