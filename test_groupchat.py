import autogen

config_list = [
    {
        "model": "palm/chat-bison",
        "base_url": "http://localhost:8000",
        "api_key": "NULL",
    }
]
llm_config = {
    "timeout": 600,
    "config_list":config_list,
    "temperature": 0
}

def test_groupchat(method):
      
    agent1 = autogen.ConversableAgent(
            "alice",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
        )
    agent2 = autogen.ConversableAgent(
            "bob",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
        )
    agent3 = autogen.ConversableAgent(
            "charlie",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
        )

    groupchat = autogen.GroupChat(
            agents=[agent1, agent2, agent3],
            messages=[],
            max_round=6,
            speaker_selection_method=method,
            allow_repeat_speaker=False if method == "manual" else True,
        )
    group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=False)

    if method == "round_robin":
            agent1.initiate_chat(group_chat_manager, message="This is alice speaking.")
            assert len(agent1.chat_messages[group_chat_manager]) == 6
            assert len(groupchat.messages) == 6
            assert [msg["content"] for msg in agent1.chat_messages[group_chat_manager]] == [
                "This is alice speaking.",
                "This is bob speaking.",
                "This is charlie speaking.",
            ] * 2
    elif method == "auto":
        agent1.initiate_chat(group_chat_manager, message="This is alice speaking.")
        assert len(agent1.chat_messages[group_chat_manager]) == 6
        assert len(groupchat.messages) == 6
    elif method == "random":
        agent1.initiate_chat(group_chat_manager, message="This is alice speaking.")
        assert len(agent1.chat_messages[group_chat_manager]) == 6
        assert len(groupchat.messages) == 6


if __name__ == "__main__":
    test_groupchat("round_robin")