import web3
from web3 import Web3, HTTPProvider
from settings import INFURA_TOKEN

class Ethereum:

    DEFAULT_GAS_PRICE = 10000000000
    DEFAULT_GAS_LIMIT = 100000

    web3 = Web3(HTTPProvider(INFURA_TOKEN))

    def __init__(self):
        pass

    def _getNonce(self, publicKey):
        return self.web3.eth.getTransactionCount(publicKey)

    def sendTransaction(self, tx, privateKey):
        signedTx = self.web3.eth.account.signTransaction(tx, privateKey)
        txHash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
        return txHash

    def buildTransaction(self, fromAddress, toAddress, value, data = None, gasPrice = DEFAULT_GAS_PRICE, gasLimit = DEFAULT_GAS_LIMIT):
        tx = {
            'to': toAddress,
            'value': value,
            'gasPrice': gasPrice,
            'gas': gasLimit,
            'nonce': self._getNonce(fromAddress)
        }
        if data != None:
            tx.update({'data': data})
        return tx

    def checkPublicKey(self, publicKey):
        try:
            publicKey = Web3.toChecksumAddress(publicKey)
            return publicKey
        except Exception as e:
            print(e)
            return False
