import datetime
import json
import hashlib
import io
import time
import random
from flask import Flask, jsonify, request, render_template, send_file
import matplotlib.pyplot as plt

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_blockchain(proof=1, previous_hash='0')

    def create_blockchain(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': []
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    # PoET Algorithm
    def proof_of_elapsed_time(self, previous_proof):
        # Simulate the process of waiting for a random period of time
        time.sleep(random.uniform(1, 3))  # Wait for 1 to 3 seconds
        # Generate a random number as the proof
        new_proof = random.randint(1, 10000)
        return new_proof

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain, chain_name):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            current_proof = block['proof']
            # Validate the proof using a simple criteria
            if chain_name == 'chain4':
                if not (1 <= current_proof <= 10000):
                    return False
            else:
                hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
                if hash_operation[:4] != '0000':
                    return False
            previous_block = block
            block_index += 1
        return True

    def add_external_input(self, data, chain_name):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_elapsed_time(previous_proof) if chain_name == 'chain4' else self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data
        }
        self.chain.append(block)
        return block

app = Flask(__name__)

# Initialize four different blockchain instances
blockchain1 = Blockchain()
blockchain2 = Blockchain()
blockchain3 = Blockchain()
blockchain4 = Blockchain()

def create_blockchain_routes(app, blockchain, chain_name):
    @app.route(f'/{chain_name}/mine_block', methods=['GET'], endpoint=f'mine_block_{chain_name}')
    def mine_block():
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_elapsed_time(previous_proof) if chain_name == 'chain4' else blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_blockchain(proof, previous_hash)
        response = {
            'message': 'BLOCK MINED',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200

    @app.route(f'/{chain_name}/get_chain', methods=['GET'], endpoint=f'get_chain_{chain_name}')
    def get_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response), 200

    @app.route(f'/{chain_name}/valid', methods=['GET'], endpoint=f'valid_{chain_name}')
    def valid():
        valid = blockchain.is_chain_valid(blockchain.chain, chain_name)
        response = {'message': 'The Blockchain is valid' if valid else 'The Blockchain is not valid'}
        return jsonify(response), 200

    @app.route(f'/{chain_name}/add_input', methods=['POST'], endpoint=f'add_input_{chain_name}')
    def add_input():
        json_input = request.get_json()
        required_fields = ['data']
        if not all(field in json_input for field in required_fields):
            return 'Invalid input', 400

        data = json_input['data']
        block = blockchain.add_external_input(data, chain_name)
        response = {
            'message': 'BLOCK MINED with External Input',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'data': block['data']
        }
        return jsonify(response), 201

    @app.route(f'/{chain_name}/chart.png', endpoint=f'chart_{chain_name}')
    def chart():
        if chain_name == 'chain1':
            chain_lengths = [len(blockchain2.chain), len(blockchain3.chain), len(blockchain4.chain)]
            labels = ['Chain 2', 'Chain 3', 'Chain 4']

            plt.figure(figsize=(10, 6))
            plt.bar(labels, chain_lengths, color=['#007bff', '#ff6f61', '#28a745'])
            plt.xlabel('Chains')
            plt.ylabel('Number of Blocks')
            plt.title('Progress of Other Chains')

        else:
            chain_length = len(blockchain.chain)
            indices = list(range(1, chain_length + 1))
            proofs = [block['proof'] for block in blockchain.chain]

            plt.figure(figsize=(10, 6))
            plt.plot(indices, proofs, marker='o', color='#007bff')
            plt.xlabel('Block Index')
            plt.ylabel('Proof')
            plt.title(f'Progress of {chain_name.capitalize()}')

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return send_file(img, mimetype='image/png')

    @app.route(f'/{chain_name}/dashboard', endpoint=f'dashboard_{chain_name}')
    def dashboard():
        return render_template('dashboard.html', chain_name=chain_name)

create_blockchain_routes(app, blockchain1, 'chain1')
create_blockchain_routes(app, blockchain2, 'chain2')
create_blockchain_routes(app, blockchain3, 'chain3')
create_blockchain_routes(app, blockchain4, 'chain4')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
