import redis


rds = redis.Redis(host='localhost', port=6379, decode_responses=True)


for k in rds.keys('akoam*'):
    rds.delete(k)
