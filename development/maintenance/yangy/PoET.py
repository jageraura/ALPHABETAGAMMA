import requests
import time
import random

def mine_poet_block(server_url):
    try:
        # Simulate the process of waiting for a random period of time
        elapsed_time = random.uniform(1, 3)
        print(f"Waiting for {elapsed_time:.2f} seconds to simulate PoET...")
        time.sleep(elapsed_time)

        # Send a request to mine the block
        response = requests.get(f"{server_url}/chain4/mine_block")
        if response.status_code == 200:
            print("Successfully mined a block with PoET!")
            print(response.json())
        else:
            print("Failed to mine a block. Server response:")
            print(response.text)
    except Exception as e:
        print("An error occurred while trying to mine a block:")
        print(str(e))

if __name__ == "__main__":
    # Replace with the actual URL of the blockchain server and chain
    server_url = "http://34.127.7.172:80"
    mine_poet_block(server_url)
