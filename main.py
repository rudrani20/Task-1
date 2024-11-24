import threading
import queue

class MessageQueue:
    def __init__(self):
        self.queue = queue.Queue()
    
    def enqueue(self, message):
        self.queue.put(message)
        print(f"Message Enqueued: {message}")
    
    def dequeue(self):
        if not self.queue.empty():
            message = self.queue.get()
            print(f"Message Dequeued: {message}")
            return message
        return None
import threading
import time

class Producer(threading.Thread):
    def __init__(self, queue, producer_id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.producer_id = producer_id

    def run(self):
        for i in range(5):  # Produce 5 messages
            message = f"Message-{i} from Producer-{self.producer_id}"
            self.queue.enqueue(message)
            time.sleep(0.5)  # Simulate production time
class Consumer(threading.Thread):
    def __init__(self, queue, consumer_id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.consumer_id = consumer_id

    def run(self):
        while True:
            message = self.queue.dequeue()
            if message:
                print(f"Consumer-{self.consumer_id} processed: {message}")
                time.sleep(1)  # Simulate processing time
if __name__ == "__main__":
    # Create a shared message queue
    message_queue = MessageQueue()

    # Create producers
    producers = [Producer(message_queue, i) for i in range(2)]  # 2 Producers

    # Create consumers
    consumers = [Consumer(message_queue, i) for i in range(3)]  # 3 Consumers

    # Start all threads
    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()

    # Join producers
    for producer in producers:
        producer.join()

    print("All producers have finished.")
