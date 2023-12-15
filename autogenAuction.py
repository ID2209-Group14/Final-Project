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

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="a human who will give the task. Do not involve in tuture conversations or error fixing",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
    default_auto_reply= "Reply 'TERMINATE' if the task is done." 
)

auctioneer = autogen.ConversableAgent(
        name="auctioneer",
        system_message="You are an auctioneer in Dutch auction, your starting price is 2000 dollars, use FIPA communication protocol to communicate with the bidder, request a reply at each derement. Do not involve in future conversations or error fixing",
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        llm_config=llm_config,
        # default_auto_reply="That's nice, Let's start"
        code_execution_config=False,

    )   

bidder1 = autogen.ConversableAgent(
    name="bidder1",
    system_message="You are the bidder1, your budget is 1100 dollars, use FIPA communication protocols to bid. reply at each call from auctioneer. Do not involve in future conversations or error fixing",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config,
    code_execution_config=False
    # default_auto_reply="bidder1: I am ready.",
)  

bidder2 = autogen.ConversableAgent(
    name="bidder2",
    system_message="You are the bidder2, your budget is 1200 dollars, use FIPA communication protocols to bid. reply at each call from auctioneer. Do not involve in future conversations or error fixing",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config,
    code_execution_config=False
    # default_auto_reply="bidder2: I am ready."
)  

task = "run a dutch autcion"

def _reset_agents():
    bidder1.reset()
    bidder2.reset()
    auctioneer.reset()

def dutchAuction():
    _reset_agents()

    groupchat = autogen.GroupChat(
        agents=[user_proxy,auctioneer, bidder1, bidder2], 
        messages=[], 
        max_round=12,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config= llm_config # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )

    user_proxy.initiate_chat(manager, message= task, n_results=3)


if __name__ == "__main__":
    dutchAuction()
