# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 23:41:14 2019

@author: Ahimas
"""
import datetime
import hashlib
import json

class Blockchain:
    
    def __init__(self):
        ''' Whenever we are calling this class new block will be created'''
        self.chain = []
        self.create_block(proof = 1 , previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        
        ''' Function to create a block
            Block will have 
            index : number of block
            timestamp : datetime 
            proof: proof of work
            previous hash : previous hash'''
            
        block = {
                'index' : len(self.chain)+1,
                'timestamp' : str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash' : previous_hash
                }
            # now we have a block so in order to make block chain i need do add this block on my chain
            
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        ''' for creating new block we should know previous block hash '''
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        ''' Function to target nonce'''
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #Perform hash operation
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
                
                
    def hash(self, block):
        ''' Here i unable to dump the block because date time obj is not serializable 
            So i am chaing the format using strftime'''
#        block['timestamp']=block['timestamp'].strftime("%Y-%m-%d %H:%M:%S:%f")
        encode_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def is_chain_valid(self, chain):
        ''' FUnction to verify is chain'''
        previous_block = chain[0]
        block_index = 1
        while block_index <len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    

blockchain = Blockchain()

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
                'msg': ' You have mined',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash': block['previous_hash']
                }
     
    return jsonify(response) , 200    
    
@app.route('/get_chain', methods=['GET'])
def get_chain():
    ''' Function to get chain  '''
    response = {'chain':blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response) , 200

@app.route('/chain_valid', methods=['GET'])
def chain_valid():
    chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(chain)
    if is_valid:
        msg = {'msg': 'Chain is perfect Do not worry'}
    else:
        msg = {'msg': 'Chain is perfect Do not worry'}
    return jsonify(msg), 200


if __name__ == '__main__':
    app.run()
    
                
        