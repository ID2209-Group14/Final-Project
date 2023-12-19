import autogen
import random
import threading

def bidderInterest(auctioneer, genre, bidders):
    bidder_interests = {bidder: False for bidder in bidders}
    for bidder in bidders: 
        auctioneer.send(recipient=bidder, message=f"Are you ready to start the {genre} auction?")


    for bidder in bidders: 
        message = bidder.last_message(auctioneer)
        reply = bidder.generate_reply(messages=[message], sender=auctioneer)
        bidder.send(message=reply, recipient=auctioneer)
        if "Yes" in reply:
            bidder_interests[bidder] = True

    return bidder_interests


def conduct_auction(auctioneer, bidders, bidder_interests, genre, starting_price, decrement, minimum_price):
    winningBidder = None
    current_price = starting_price
    

    
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
    minimum_price = random.randint(500, 1500)

    genres = ["CDs", "Clothes", "Arts"]

    auctioneers = [
        autogen.ConversableAgent(
            f"auctioneer{i}",
            max_consecutive_auto_reply=10,
            human_input_mode="NEVER",
            llm_config=llm_config,
            system_message=f"You are an auctioneer in a Dutch auction. You are selling {genre}, You starting price is ${starting_price} dollars, and you will decrease the price by ${decrement} dollars in each round.")
            for i, genre in enumerate(genres)
    ]
    

    bidders = [
        autogen.ConversableAgent(f"bidder{i}", llm_config=llm_config, max_consecutive_auto_reply=10,
            human_input_mode="NEVER", system_message=f"You are a bidder in a Dutch auction. You are and only ready for your {genre} auction. Your budget is ${budget} dollars. The price will be accepted only if it is equal or less than your budget. In that case you will reply 'I accept the price'.")
        for i in range(6)
        for budget in [random.randint(1000, 2000)]
        for genre in [random.choice(genres)]
    ]

    threads = []

    for auctioneer in auctioneers:
        genre = auctioneer.system_message.split("You are selling ")[1].split(",")[0]
        bidder_interests = bidderInterest(auctioneer, genre, bidders)
        print(genre)
        print(bidder_interests)
        starting_price = random.randint(2000, 3000)
        decrement = random.randint(500, 1000)
        minimum_price = random.randint(500, 1500)

        auction_thread = threading.Thread(target=conduct_auction, args=(auctioneer, bidders, bidder_interests, genre, starting_price, decrement, minimum_price))
        threads.append(auction_thread)

    
    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
