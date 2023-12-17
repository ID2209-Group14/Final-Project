import autogen
import random


def conduct_auction(auctioneer, bidders, genre, starting_price, decrement, minimum_price):
    winningBidder = bidders[0]
    current_price = starting_price
    bidder_interests = {bidder: False for bidder in bidders}

    for bidder in bidders: 
        auctioneer.send(recipient=bidder, message=f"Are you ready to start the {genre} auction?")


    for bidder in bidders: 
        message = bidder.last_message(auctioneer)
        reply = bidder.generate_reply(messages=[message], sender=auctioneer)
        bidder.send(message=reply, recipient=auctioneer)
        if "Yes" in reply:
            bidder_interests[bidder] = True

    
    while current_price >= minimum_price:
        for bidder in bidders:
            if bidder_interests[bidder]:
                auctioneer.send(recipient=bidder, message=f"Selling {genre} for ${current_price}.") 

        any_bid_accepted = False
        for bidder in bidders:
            if bidder_interests[bidder]:
                message = bidder.last_message(auctioneer)
                reply = bidder.generate_reply(messages=[message], sender=auctioneer)
                bidder.send(message=reply, recipient=auctioneer)
                if "I accept" in reply:
                    any_bid_accepted = True
                    winningBidder = bidder
                    break

        if any_bid_accepted:
            auctioneer.send(message="Congratulations, you won the auction. Please provide some feedback on how you experienced the auction.", recipient=winningBidder, request_reply=True)
            return
        else:
            current_price -= decrement
    
    reply = auctioneer.generate_reply(messages=[{"content": "Inform in one sentence to all bidders that the auction for clothes has ended without a sale."}])

    for bidder in bidders:
        if bidder_interests[bidder]:
            auctioneer.send(message=reply, recipient=bidder)
     




def main():
    config_list = [
        {"model": "palm/chat-bison", "base_url": "http://localhost:8000", "api_key": "NULL"}
    ]
    llm_config = {"timeout": 600, "config_list": config_list, "temperature": 0.5}

    starting_price = random.randint(2000, 3000)
    decrement = random.randint(500,1000)
    minimum_price = random.randint(1000, 2000)

    genres = ["CDs", "Clothes", "Arts"]

    auctioneer = autogen.ConversableAgent(
            "auctioneer",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message=f"You are an auctioneer in a Dutch auction. You starting price is ${starting_price} dollars, and you will decrease the price by ${decrement} dollars in each round."
            )
            # for i in range(3)
            # for genre in [random.choice(genres)]
        
    

    bidders = [
        autogen.ConversableAgent(f"bidder{i}", llm_config=llm_config, max_consecutive_auto_reply=10,
            human_input_mode="NEVER", system_message=f"You are a bidder in a Dutch auction. Your genre is {genre}, you only participate in your genre auction. Your budget is ${budget} dollars. The price will be accepted only if it is equal or less than your budget. In that case you will reply 'I accept the price'.")
        for i in range(6)
        for budget in [random.randint(1000, 2000)]
        for genre in [random.choice(genres)]
    ]


  


    conduct_auction(auctioneer, bidders, random.choice(genres), starting_price, decrement, minimum_price)

if __name__ == "__main__":
    main()
