import pymongo
client = pymongo.MongoClient('localhost', 27017)
#client = pymongo.MongoClient('217.12.38.37', 27017)
db = client.usersDB #Misha
users = db['Users']
const = db['Ad']
order = db['order']
temp  = db['temporary']
