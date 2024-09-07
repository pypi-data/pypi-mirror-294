import hashlib
import json
import typing

import bittensor
import requests

__version__: typing.Final[str] = "0.0.1"
OMRON_NETUID: typing.Final[int] = 2


class Proof_Of_Weights:
    def __init__(self, wallet_name: str, wallet_hotkey: str, omron_validator_ss58: str, netuid: int, network: str = "finney"):
        """
        Initialize the Proof of Weights class with your wallet and a validator's hotkey from the omron subnet.
        """
        self._wallet = bittensor.wallet(wallet_name, wallet_hotkey)
        self._btnetwork = bittensor.subtensor(network=network)
        self._omron_validator_ss58 = omron_validator_ss58
        self._omron_validator_axon = self._btnetwork.get_axon_info(netuid=OMRON_NETUID, hotkey_ss58=self.omron_validator_ss58)
        self._omron_validator_ip = self._omron_validator_axon.ip
        self._netuid = netuid
        self._last_transaction_hash = ""


    def submit_inputs(self, reward_function_inputs: list) -> str:
        """
        Submit reward function inputs from network with netuid to a validator on the omron subnet.
        """
        # serialize the reward function inputs as json bytes
        inputs_bytes = json.dumps(reward_function_inputs).encode()
        # sign the inputs with your hotkey
        signature = self._wallet.hotkey.sign(inputs_bytes)
        # send the reward function inputs and signature to the omron subnet on port 8000
        response = requests.post(f"http://{self._omron_validator_ip}:8000/submit_inputs", data=inputs_bytes, signature=signature, sender=self._wallet.hotkey.ss58_address, netuid=self._netuid)
        if response.status_code != 200:
            return ""
        # get the transaction hash
        self._last_transaction_hash = hashlib.sha256(inputs_bytes + signature).hexdigest()
        return self._last_transaction_hash


    def get_proof(self) -> dict:
        """
        Get the proof of weights from the omron subnet validator.
        """
        response = requests.get(f"http://{self._omron_validator_ip}:8000/get_proof_of_weights/{self._last_transaction_hash}")
        if response.status_code != 200:
            return {}
        return response.json()

