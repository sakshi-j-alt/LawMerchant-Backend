import pymongo
url = 'mongodb://localhost:27017'
client =pymongo.MongoClient(url)
db = client['db1_regulations_pdf']
ppd= db['previouslyProcessedData']