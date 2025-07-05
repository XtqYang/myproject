import redis


class RedisManager:
    def __init__(self, db_conn='redis://:@8.138.154.238:6379/0'):
        """初始化 Redis 连接"""
        self.redis_client = redis.from_url(db_conn)

    def get_all_data(self):
        """获取 Redis 数据库中的所有数据"""
        keys = self.redis_client.keys('*')
        all_data = {}

        for key in keys:
            key = key.decode()  # 解码字节数据
            key_type = self.redis_client.type(key).decode()

            if key_type == 'string':
                all_data[key] = self.redis_client.get(key).decode()

            elif key_type == 'hash':
                all_data[key] = self.redis_client.hgetall(key)
                all_data[key] = {k.decode(): v.decode() for k, v in all_data[key].items()}

            elif key_type == 'list':
                all_data[key] = self.redis_client.lrange(key, 0, -1)
                all_data[key] = [v.decode() for v in all_data[key]]

            elif key_type == 'set':
                all_data[key] = self.redis_client.smembers(key)
                all_data[key] = {v.decode() for v in all_data[key]}

            elif key_type == 'zset':
                all_data[key] = self.redis_client.zrange(key, 0, -1, withscores=True)
                all_data[key] = [(v[0].decode(), v[1]) for v in all_data[key]]

        return all_data

    def delete_key(self, key):
        """删除指定键"""
        self.redis_client.delete(key)

    def flush_db(self):
        """清空当前数据库"""
        self.redis_client.flushdb()

    def flush_all(self):
        """清空所有数据库"""
        self.redis_client.flushall()


# 示例：使用 RedisManager 类
if __name__ == "__main__":
    redis_manager = RedisManager()

    # 获取并打印所有数据
    all_data = redis_manager.get_all_data()
    print("📌 Redis 数据库内容：")
    for key, value in all_data.items():
        print(f"{key}: {value}")

    # 删除某个键
    # redis_manager.delete_key("name")

    # 清空当前数据库
    # redis_manager.flush_db()

    # 清空所有数据库
    # redis_manager.flush_all()
