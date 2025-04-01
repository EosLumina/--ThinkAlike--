
from backend.agents.base_agent import BaseAgent
import time

class CodeDeveloperAgent(BaseAgent):
    def __init__(self, agent_id, message_queue):
        super().__init__(agent_id=agent_id, message_queue=message_queue)
        self.logger.info(f"CodeDeveloperAgent {agent_id} initialized.")

    def run(self):
        self.logger.info(f"CodeDeveloperAgent ({self.agent_id}) started...")
        while self.running:
            message = self.receive_message(timeout=5) # Check for messages every 5 seconds
            if message:
                self.process_message(message)
            else:
                # Agent can perform other tasks when no messages are in queue (optional)
                self.logger.debug(f"CodeDeveloperAgent ({self.agent_id}) - No tasks, idling...")
                time.sleep(2) # Sleep for a bit if queue is empty
        self.logger.info(f"CodeDeveloperAgent ({self.agent_id}) stopped.")


    def process_message(self, message):
        message_type = message.get("message_type")
        payload = message.get("payload")

        if message_type == "task_request":
            task_description = payload.get("task_description")
            component_name = payload.get("component_name")
            self.logger.info(f"CodeDeveloperAgent ({self.agent_id}) - Received task request: {task_description} for component: {component_name}")

            # --- Placeholder: Implement actual code generation logic here ---
            time.sleep(3) # Simulate code generation time
            generated_code = f"// Generated code for {component_name} component...\n// ... (code content) ..."
            code_file_path = f"ui/src/components/{component_name}.jsx" # Example path

            # --- Send "task_completed" message back to TaskAllocatorAgent ---
            self.send_message(
                recipient_id="task_allocator_agent",
                message_type="task_completed",
                payload={
                    "task_id": payload.get("task_id"),
                    "component_name": component_name,
                    "code_file_path": code_file_path,
                    "status": "success",
                    "message": f"Code generated for {component_name} component."
                }
            )
            self.logger.info(f"CodeDeveloperAgent ({self.agent_id}) - Task completed, message sent.")

        elif message_type == "some_other_message_type": # Example for handling other message types
            # Handle other message types as needed
            pass # Placeholder for other message handling logic
