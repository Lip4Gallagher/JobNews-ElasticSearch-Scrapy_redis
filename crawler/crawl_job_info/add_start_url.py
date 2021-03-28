import redis


client = redis.Redis(host='localhost', password='Mjolnir', port=6379)
# client.lpush('chitone:start_urls', 'https://www.job5156.com')
client.sadd('chitone:start_urls', 'https://www.job5156.com')
