import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask,jsonify,request

class Blockchain(object):
##    current_transactions = []
##    chain = []
##    nodes = set()
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.new_block(proof=100, previous_hash='1')
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            })
        return self.last_block['index'] + 1
    
    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        consensus algorithm resolve conflict
        use the longest chain in net
        :return: <bool> True if chain replaced, else False
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
    
"""
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "42343ffe232add55ee0",
            'recipient': "a77fdcde23213c7cda5",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf234212321acde77fe7c7909889977acce77fd"
}
"""

###############
# create node #
###############

# install our node
app = Flask(__name__)


# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

# instantiate the blockchain
blockchain = Blockchain()


@app.route('/mine',methods=['GET'])
def mine():

#   pp = pprint.PrettyPrinter(indent=4)
#   pp.pprint(blockchain.chain)
    
    # we run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #give the reward to work proof node
    #if sender is "0" ,dedicate the new chain
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        )

    # forge the new block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message':"New Block Forged",
        'index':block['index'],
        'transactions':block['transactions'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
        }
    
    return jsonify(response),200

"""
transaction object
{
"sender":"my address",
"recipient":"someone else's address",
"amount":5
}
"""
@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that required fields are in the posted data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values',400

    # create a new transaction
    index = blockchain.new_transation(values['sender'],values['recipient'],values['amount'])

    response = {'message':f'Transaction will be added to Block {index}'}
    return jsonify(response),201

@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
        }
    return jsonify(response),200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)


