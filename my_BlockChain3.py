#   第三部分这部分主要模拟比特币的交易，

#   data
#   之前区块的哈希值
#   子的哈希值，它是由存储在区块里的信息，算出来的（data + 之前区块的哈希值）
import hashlib as hasher
import datetime as date


#   记录交易的模块
class Transaction:
    def __init__(self, from1, to, amount):
        self.from1 = from1
        self.to = to
        self.amount =amount
        # self.timestamp = timestamp

    def print_full(self):
        print(self.from1 + '到' + self.to)
        print('金额:' + str(self.amount))
        # print(self.timestamp)


#   区块
class Block:
    def __init__(self, transactions, previoushash):             # python这个就相当于java的构造器
        #   data之前是字符string ->现在是对象的数组array of objects
        self.transactions = transactions
        self.previousHash = previoushash
        self.nonce = 1
        self.timestamp = date.datetime.now()
        self.hash = self.computeHash()      # 因为这个要调用timestamp, 所以一定要放他后面，边编译，边运算,这个和java不一样

    def computeHash(self):
        sha = hasher.sha256()
        #   这里的data需要变成string
        # 通过这个区块的数据和上个区块的哈希就可以生成这个区块的哈希
        sha.update((str(self.transactions) + self.previousHash + str(self.nonce) + str(self.timestamp)).encode("utf8"))
        return sha.hexdigest()         # 这样就可以再次创建这个区块的哈希来验证这个区块的数据有没有被篡改过

    def getAnswer(self, difficulty):
        #   开头的前n位为0的hash
        answer = ''
        for i in range(0, difficulty):
            answer += '0'
        return answer

#   计算符合区块链难度的hash
#   工作就是改变随机数的值来计算结果，一次一次得去试这个值去满足那个条件（比如说前5位为0）
    def mine(self, difficulty):
        while True:
            self.hash = self.computeHash()
            # print(self.hash[0: 3])
            if self.hash[0: difficulty] != self.getAnswer(difficulty):
                self.nonce = self.nonce + 1
                self.hash = self.computeHash()

            else:
                break
        print('挖矿结束')
        print(self.hash)

# block = Block('转账十元', '123')
# print("\n")
# print("Hash:{}".format(block.hash))
# print(block.data)
# print(block.previousHash)
# print(block.hash)


#   有了区块，来写链，区块的链
class Chain:
    def __init__(self):
        self.chain = [self.bigBang()]
        self.transactionPool = []
        self.difficulty = 4         # 通过动态调整这个难度，比特币可以保证平均一个区块生成的时间是10分钟，哇哦！！
        self.mineReward = 50        # 每挖出一个区块有50个比特币发放到矿工这里

    def bigBang(self):
        genesisBlock = Block('我是祖先', '')
        return genesisBlock

    #   添加transaction 到transactionpool
    def addtransaction(self, transaction):
        self.transactionPool.append(transaction)

    #   找到最近一个block的hash
    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    # 添加区块到区块链上
    def addBlockToChain(self, newblock):
        newblock.previousHash = self.getLatestBlock().hash
        # newblock.hash = newblock.computeHash()
        newblock.mine(self.difficulty)
        #   这个hash需要满足区块链设置的条件
        self.chain.append(newblock)

    #   区块现在不是外部的，发生在链上在挖这个transaction
    def mineTransactionPool(self, mineRewardAdress):
        #  发放矿工奖励, 将发放50元的奖励到挖矿人的账户，from是从链上的所以是""
        minerRewardTransaction = Transaction("", mineRewardAdress, self.mineReward)
        self.transactionPool.append(minerRewardTransaction)
        #   挖矿  把这个库从链里面拿出来
        newBlock = Block(self.transactionPool, self.getLatestBlock().hash)
        newBlock.mine(self.difficulty)
        #   添加区块到区块链，清空transactionPool
        self.chain.append(newBlock)
        self.transactionPool = []

    #  要验证区块的previousHash是否等于previous区块的hash
    def validateChain(self):
        # if len(self.chain) == 3:
        #     if self.chain[0].hash != self.chain[0].computeHash():
        #         return False
        #     else:
        #         return True

        #   self.chain[1] 是第二个区块
        #   我们从第二个区块开始，验证到最后一个区块
        for i in range(1, len(self.chain)):
            blockToValidate = self.chain[i]
            #   首先验证当前区块有没有被篡改
            if blockToValidate.hash != blockToValidate.computeHash():
                print("数据篡改")
                return False
            #   再验证区块的previousHash是否等于previous区块的hash
            previousBlock = self.chain[i - 1]
            if blockToValidate.previousHash != previousBlock.hash:
                print("前后区块链接断裂")
                return False

        return True


# t1 = Transaction('A', 'B', 100)
# # print(t1.from1 + '到' + t1.to)
# # print('金额:' + str(t1.amount))
# # print(t1.timestamp)
# t1.print_full()

ZY = Chain()
print(ZY.chain[0].transactions)
t1 = Transaction('addr1', 'addr2', 10)
t2 = Transaction('addr2', 'addr1', 5)
ZY.addtransaction(t1)
ZY.addtransaction(t2)
# t1.print_full()
# t2.print_full()
# ZY.mineTransactionPool('addr3')
# ZY.mineTransactionPool('addr4')
# print(ZY.chain[0])
# print(ZY.chain[1])
print(ZY.transactionPool[0].print_full())   # 调用方法的时候后面加括号，终于搞定了
# print(ZY.chain[2])
# print(ZY.chain[2])