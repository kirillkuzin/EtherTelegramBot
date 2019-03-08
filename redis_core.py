import redis
from settings import REDIS_LINK

class Redis():

    def __init__(self):
        self.redisTx = redis.StrictRedis(
            host = REDIS_LINK,
            port = 6379,
            db = 1
        )

    def addTx(self, tx):
        lastTxId = self.redisTx.get('lastTxId')
        self.redisTx.hmset(lastTxId, tx)
        self.redisTx.expire(lastTxId, 900000)
        self.redisTx.incr('lastTxId')
        self.redisTx.bgsave()
        return lastTxId

    def getTx(self, txId):
        tx = self.redisTx.hmget(txId)
        return tx
