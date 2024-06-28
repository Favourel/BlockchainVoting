from hashlib import sha256
import datetime
import random
from .models import Block, Vote, Candidate


class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_vote = Vote.objects.create(user=None, candidate=None)
        genesis = Block.objects.create(timestamp=datetime.datetime.now(), vote=genesis_vote, previous_hash="0", nonce=0)
        genesis.hash = genesis.calculate_hash()
        genesis.save()
        return genesis

    def add_vote(self, vote):
        previous_block = self.chain[-1]
        new_block = Block(timestamp=datetime.datetime.now(), vote=vote, previous_hash=previous_block.hash, nonce=0)
        new_block.hash = new_block.calculate_hash()
        while not new_block.hash.startswith('0' * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        new_block.save()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_vote_counts(self):
        vote_counts = {}
        for block in self.chain[1:]:
            candidate_name = block.vote.candidate.name
            if candidate_name in vote_counts:
                vote_counts[candidate_name] += 1
            else:
                vote_counts[candidate_name] = 1
        return vote_counts
