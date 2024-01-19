# Dutch Auction System with LLM-based Agents

## Overview

This project implements a Dutch auction system using Language Model (LLM)-based agents within the AutoGen framework. The system is designed to showcase the application of language models in real-time auction environments, with LLM-based agents acting as bidders and auctioneers.

## Prerequisites

- Python 3.11.5
- PALM API Key (Note: VPN required in certain regions including Europe)

## Installation

1. **Install Python**

   - Ensure Python 3.11.5 is installed on your system.

2. **Clone the Repository**

   - Clone this repository to your local machine.

3. **Install Required Packages**

   - Navigate to the project directory and run the following command in the terminal:
     ```
     pip install -r requirements.txt
     ```

4. **Retrieve PALM API Key**

   - Obtain a PALM API key from [Google MakerSuite](https://makersuite.google.com/).
   - Note: The PALM API is not accessible in some regions, including Europe. A VPN may be required.

5. **Set Up PALM API Key**

   - Run the following command in Git Bash or another Linux-based terminal:
     ```
     export PALM_API_KEY=<Your_API_Key>
     ```
   - Replace `<Your_API_Key>` with your actual API key.

6. **Run LLM Model Setup**
   - Execute the following command:
     ```
     litellm –model palm/chat-bison
     ```

## Running the Auction Simulation

1. **Single Dutch Auction Simulation**

   - Run the following command in a new terminal:
     ```
     python dutchAuction_basic.py
     ```
   - This will simulate a single Dutch auction.

2. **Multiple Dutch Auctions Simulation**
   - To simulate multiple Dutch auctions simultaneously, where bidders join only if interested in the genre, run:
     ```
     python dutchAuction_Challenge1.py
     ```

## Contributing

Feel free to fork this project and submit pull requests for any improvements or fixes.

## License

This project is licensed under the [MIT License](LICENSE).
