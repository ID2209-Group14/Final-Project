import autogen

config_list = [
    {
        "model": "palm/chat-bison",
        "base_url": "http://localhost:8000",
        "api_key": "NULL",
    }
]
llm_config = {
    "timeout": 6000,
    "config_list":config_list,
    "temperature": 0
}



auctioneer = autogen.AssistantAgent(
    name="auctioneer",
    system_message="You are an auctioneer, ask guests to participate, then start the acution.",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    function_map=callable,
    code_execution_config={"work_dir": "auction"},
    llm_config=llm_config,
    default_auto_reply="That's nice, Let's start"
)   

guest1 = autogen.AssistantAgent(
    name="guest1",
    system_message="You are a bidder, shout and printout general feedback to auctioneer.",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    function_map=callable,
    code_execution_config={"work_dir": "auction"},
    llm_config=llm_config,
    default_auto_reply="guest1: I am ready."
)  

guest2 = autogen.AssistantAgent(
    name="guest2",
    system_message="You are a bidder, give general feedback to auctioneer.",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    function_map=callable,
    code_execution_config={"work_dir": "auction"},
    llm_config=llm_config,
    default_auto_reply="guest2: I am ready."
)  

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="a human who will give the idea. Do not involve in tuture conversations or error fixing",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages":2,
        "work_dir": "groupchat",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)

groupchat = autogen.GroupChat(
    agents=[auctioneer, guest2, guest1], messages=[]
)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={
    "timeout": 600,
    "cache_seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
    )

user_proxy.initiate_chat(manager, message= "simulate a dutch auction")
