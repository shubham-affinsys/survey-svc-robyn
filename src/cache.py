import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Test the connection
redis_client.set('test_key', 'Hello, Redis!')
print(redis_client.get('test_key'))  # Output: Hello, Redis!
