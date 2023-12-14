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
    "temperature": 0.5
}

def main():
     
    agent1 = autogen.ConversableAgent(
            "bidder1",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message="You are a bidder in a Dutch auction. Your budget is 1000 dollars. You will accept the price only if it meets your budget"
        )
    agent2 = autogen.ConversableAgent(
            "bidder2",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message="You are a bidder in a Dutch auction. Your budget is 1100 dollars.  You will accept the price only if it meets your budget"
        )
    auctioneer = autogen.ConversableAgent(
            "auctioneer",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message="You are an auctioneer in a Dutch auction. You starting price is 2000 dollars, and you will decrease the price by 100 dollars in each round, if no one buys. You will not sell the item for less than 900 dollars.",
        )
    groupchat = autogen.GroupChat(
        agents=[auctioneer, agent1, agent2],
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False
    )
    group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    auctioneer.initiate_chat(group_chat_manager, message="Hello everyone, the starting price is 2000 dollars.")

if __name__ == "__main__":
    main()