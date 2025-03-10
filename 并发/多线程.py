import threading
import time
import random

# 全局共享资源：订单列表和锁
orders = []
order_lock = threading.Lock()


# 模拟用户提交订单的任务
def user_purchase(user_id):
    global orders
    # 生成随机订单号
    order_id = f"ORDER-{user_id}-{random.randint(1000, 9999)}"

    # 用锁保护共享订单列表,保证数据操作的原子性和一致性
    with order_lock:
        orders.append(order_id)
        print(f"用户 {user_id} 提交订单: {order_id}")

    # 模拟网络延迟（0~1秒随机等待）
    time.sleep(random.random())


if __name__ == "__main__":
    threads = []
    # 创建10个用户线程模拟并发请求
    for user_id in range(1, 11):  # 用户ID从1到10
        t = threading.Thread(target=user_purchase, args=(user_id,))
        threads.append(t)
        t.start()

    # 等待所有用户完成操作
    for t in threads:
        t.join()

    # 输出最终生成的订单
    print("\n所有订单生成完毕：")
    for order in orders:
        print(order)