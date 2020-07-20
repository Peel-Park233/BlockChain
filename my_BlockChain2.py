#   第二部分这部分主要模拟比特币挖矿的过程，工作量证明机制来说明，篡改比挖矿的成本大得多得多来防止篡改。

#   data
#   之前区块的哈希值
#   子的哈希值，它是由存储在区块里的信息，算出来的（data + 之前区块的哈希值）
import hashlib as hasher


class Block:
    def __init__(self, data, previousHash):             # python这个就相当于java的构造器
        self.data = data
        self.previousHash = previousHash
        self.nonce = 1
        self.hash = self.computeHash()

    def computeHash(self):
        sha = hasher.sha256()
        sha.update((self.data + self.previousHash + str(self.nonce)).encode("utf8"))      # 通过这个区块的数据和上个区块的哈希就可以生成这个区块的哈希
        return sha.hexdigest()                                         # 这样就可以再次创建这个区块的哈希来验证这个区块的数据有没有被篡改过

    def getAnswer(self, difficulty):
        #   开头的前n位为0的hash
        answer = ''
        for i in range(0, difficulty):
            answer += '0'
        return answer

#   计算符合区块链难度的hash
#   工作就是改变随机数的值来计算结果，一次一次得去试这个值去满足那个条件（比如说前5位为0）
    def mine(self, difficulty):
        while(True):
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
        self.difficulty = 4         # 通过动态调整这个难度，比特币可以保证平均一个区块生成的时间是10分钟，哇哦！！

    def bigBang(self):
        genesisBlock = Block('我是祖先', '')
        return genesisBlock

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

# findsheepChain = Chain()
# # print(findsheepChain.chain[0].hash)
# block1 = Block("转账10元", "")
# findsheepChain.addBlockToChain(block1)
# # print(block1.hash)
# # print(block1.previousHash)
# # print(block1.data)
# # print(findsheepChain.chain[1].hash)
# # print(findsheepChain.chain)
# # print(i for i in findsheepChain.chain)
# block2 = Block("转账10个10元", "")
# findsheepChain.addBlockToChain(block2)
#
# print(findsheepChain.validateChain())
# # print(findsheepChain.chain)
# findsheepChain.chain[1].data = "转账100元"
# print(findsheepChain.validateChain())
# findsheepChain.chain[1].hash = findsheepChain.chain[1].computeHash()
# print(findsheepChain.validateChain())
# print(len(findsheepChain.chain))


FindSheep = Chain()
block1 = Block("转账10元", "")
FindSheep.addBlockToChain(block1)
block2 = Block("转账100元", "")
FindSheep.addBlockToChain(block2)
FindSheep.chain[1].data = "转账1000元"
FindSheep.chain[1].mine(4)
print(FindSheep.validateChain())    # 所以说你要篡改一个区块还不如挖一个区块