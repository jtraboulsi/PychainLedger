# %%
# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# %%
#Record Data Class
#Let's first create an object that will help us store transactional information data. This object will serve as a blueprint to store our data.

# %%
@dataclass
class Record:
    Sender: str
    Receiver: str
    Amount: float


# %%
#Block Data Class
#Our Block object will allow us to group the information that constitutes a block on our ledger. 
# Note that it's first attribute is a Record object based on the class we have just created 
# which contains the transaction's specific information. 
# We also build a method to 'secure hash' our block's information using SHA256 algo.

# %%
@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()



# %%
#PyChain Data  Class
#PyChain object will allow us to build our chain of blocks

# %%

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True



# %%
# Streamlit Code
# Adds the cache decorator for Streamlit

# %%
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# %%
# Step 3:
# Adding relevant User Inputs to the Streamlit Interface

# %%
# Adding an input area where you can get a value for `sender` from the user.
sender = st.text_input("Sender")

# Adding an input area where you can get a value for `receiver` from the user.
receiver = st.text_input("Receiver")

# Adding an input area where you can get a value for `amount` from the user.
amount = st.text_input("Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    
    # Updating `new_block` so that `Block` consists of an attribute named `record`
    # which is set equal to a `Record` that contains the `sender`, `receiver`,
    # and `amount` values
    new_block = Block(
        record= Record(sender, receiver, amount),
        creator_id=10,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code (continues)

#we will showcase our blocks using a dataframe from pandas library

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())



# %%
# Step 4:
# Test the PyChain Ledger by Storing Records



