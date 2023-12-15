import autogen


def conduct_auction(auctioneer, bidders, starting_price, decrement, minimum_price):
    winningBidder = bidders[0];
    current_price = starting_price
    for bidder in bidders: 
        auctioneer.send(recipient=bidder, message="Are you ready to start the auction?")


    for bidder in bidders: 
        message = bidder.last_message(auctioneer)
        reply = bidder.generate_reply(messages=[message], sender=auctioneer)
        bidder.send(message=reply, recipient=auctioneer)

    
    while current_price >= minimum_price:
        for bidder in bidders:
            auctioneer.send(recipient=bidder, message=f"Selling clothes for ${current_price}.") 

        any_bid_accepted = False
        for bidder in bidders:
            message = bidder.last_message(auctioneer)
            reply = bidder.generate_reply(messages=[message], sender=auctioneer)
            bidder.send(message=reply, recipient=auctioneer)
            if "I accept" in reply:
                any_bid_accepted = True
                winningBidder = bidder;
                break

        if any_bid_accepted:
            auctioneer.send(message="Congratulations, you won the auction. Please provide some feedback on how you experienced the auction.", recipient=winningBidder, request_reply=True)
            return
        else:
            current_price -= decrement
    
    reply = auctioneer.generate_reply(messages=[{"content": "Inform in one sentence to all bidders that the auction for clothes has ended without a sale."}])
    
    for bidder in bidders:
        auctioneer.send(message=reply, recipient=bidder)
     




def main():
    config_list = [
        {"model": "palm/chat-bison", "base_url": "http://localhost:8000", "api_key": "NULL"}
    ]
    llm_config = {"timeout": 600, "config_list": config_list, "temperature": 1}

    starting_price = 1500
    
    decrement = 100
    minimum_price = 1400

    auctioneer = autogen.ConversableAgent(
            "auctioneer",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message=f"You are an auctioneer in a Dutch auction. You starting price is ${starting_price} dollars, and you will decrease the price by ${decrement} dollars in each round.",
    )    
    

    bidders = [
        autogen.ConversableAgent(f"bidder{i}", llm_config=llm_config, max_consecutive_auto_reply=10,
            human_input_mode="NEVER", system_message=f"You are a bidder in a Dutch auction. Your budget is ${budget} dollars. The price will be accepted only if it is equal or less than your budget. In that case you will reply 'I accept the price'.")
        for i, budget in enumerate([900, 1100, 1300, 400])
    ]


  


    conduct_auction(auctioneer, bidders, starting_price, decrement, minimum_price)

if __name__ == "__main__":
    main()
