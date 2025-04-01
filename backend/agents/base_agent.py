import multiprocessing
import queue
import logging

class BaseAgent(multiprocessing.Process):
    def __init__(self, agent_id, message_queue):
        super().__init__()
        self.agent_id = agent_id
        self.message_queue = message_queue
        self.running = True
        self.logger = logging.getLogger(self.__class__.__name__) # Logger per agent class
        self.setup_logging()

    def setup_logging(self):
        # Configure basic logging (you can customize this further)
        logging.basicConfig(level=logging.INFO,
                            format=f'%(asctime)s - %(levelname)s - %(name)s - %(message)s') # Include agent name in log format

    def run(self):
        raise NotImplementedError("Subclasses must implement the run method.")

    def stop(self):
        self.running = False
        self.logger.info(f"Agent {self.agent_id} stopping...")

    def send_message(self, recipient_id, message_type, payload):
        message = {
            "sender_id": self.agent_id,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "payload": payload
        }
        self.message_queue.put(message)
        self.logger.info(f"Agent {self.agent_id} sent message: {message}")

    def receive_message(self, timeout=1): # Added timeout for non-blocking check
        try:
            message = self.message_queue.get(timeout=timeout) # Non-blocking get with timeout
            self.logger.info(f"Agent {self.agent_id} received message: {message}")
            return message
        except queue.Empty:
            return None # Return None if queue is empty after timeout

    def process_message(self, message):
        raise NotImplementedError("Subclasses should implement process_message to handle received messages.")
