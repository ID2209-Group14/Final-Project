import autogen

class CustomConversableAgent(autogen.ConversableAgent):
    def __init__(self, name, llm_config, role, budget=None):
        super().__init__(name, llm_config=llm_config)
        self.role = role
        self.budget = budget

    def generate_message(self, current_price):
        if self.role == "auctioneer":
            return f"I am the auctioneer in a Dutch auction. The current price is ${current_price}. Will any bidder accept this price?"
        elif self.role == "bidder":
            decision = "accept" if current_price <= self.budget else "reject"
            return f"As a bidder, I {decision} the current price of ${current_price}."

def conduct_auction(group_chat_manager, auctioneer, bidders, starting_price, decrement, minimum_price):
    auctioneer.send(recipient=group_chat_manager, message="Hello boys")
    current_price = starting_price

    while current_price >= minimum_price:
        auctioneer.send(group_chat_manager, auctioneer)
        print(f"Auctioneer: The current price is ${current_price}. Will any bidder accept this price?")

        any_bid_accepted = False
        for bidder in bidders:
            if bidder.budget >= current_price:
                print(f"{bidder.name}: I accept the price of ${current_price}.")
                any_bid_accepted = True
                break
            else:
                print(f"{bidder.name}: I cannot accept the price of ${current_price}. It's higher than my budget.")

        if any_bid_accepted:
            print(f"Auctioneer: The item is sold at ${current_price}. Auction ends.")
            return
        else:
            print(f"Auctioneer: No bids accepted at ${current_price}. Lowering the price.")
            current_price -= decrement

    print("Auctioneer: The auction ended without any sale.")


def main():
    config_list = [
        {"model": "palm/chat-bison", "base_url": "http://localhost:8000", "api_key": "NULL"}
    ]
    llm_config = {"timeout": 600, "config_list": config_list, "temperature": 0}

    auctioneer = CustomConversableAgent("auctioneer", llm_config=llm_config, role="auctioneer")
    
    bidders = [
        CustomConversableAgent(f"bidder{i}", llm_config=llm_config, role="bidder", budget=budget)
        for i, budget in enumerate([900, 1100, 1300], start=1)
    ]


    groupchat = autogen.GroupChat(
        agents=[auctioneer] + bidders,
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=True
    )
    group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    conduct_auction(group_chat_manager, auctioneer, bidders, starting_price=1500, decrement=100, minimum_price=800)

if __name__ == "__main__":
    main()
