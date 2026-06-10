import threading
import time
import random

class Agent:
    def __init__(self, agent_id, num_agents):
        self.agent_id = agent_id
        self.num_agents = num_agents
        self.message_queue = []
        self.lock = threading.Lock()
        self.is_running = True

    def send_message(self, recipient_id, message):
        # In a real system, this would involve network communication.
        # Here, we simulate by directly adding to the recipient's queue.
        if 0 <= recipient_id < self.num_agents:
            # Simulate potential delays or failures at scale
            if random.random() < 0.01: # 1% chance of message loss at scale
                print(f"Agent {self.agent_id}: Message to {recipient_id} lost (simulated scale issue).")
                return
            # Simulate network latency
            time.sleep(random.uniform(0.001, 0.005))
            # Use lock for thread-safe access to other agent's queue (simulated)
            # In a real distributed system, this would be handled by a message broker.
            # For this single-process simulation, we bypass direct queue access for simplicity
            # and assume a central mechanism would deliver it.
            print(f"Agent {self.agent_id}: Sending message to Agent {recipient_id}: '{message}'")
        else:
            print(f"Agent {self.agent_id}: Invalid recipient ID {recipient_id}.")

    def receive_message(self, sender_id, message):
        with self.lock:
            self.message_queue.append((sender_id, message))
            # print(f"Agent {self.agent_id}: Received message from {sender_id}: '{message}'") # Too noisy for many agents

    def process_messages(self):
        while self.is_running:
            messages_to_process = []
            with self.lock:
                messages_to_process = self.message_queue
                self.message_queue = [] # Clear queue after processing

            if messages_to_process:
                # Simulate processing overhead that increases with message volume
                processing_time = len(messages_to_process) * 0.0005 # Scale-dependent processing
                time.sleep(processing_time)
                # print(f"Agent {self.agent_id}: Processed {len(messages_to_process)} messages.")

            # Simulate agent's own decision-making/action
            if random.random() < 0.05: # Agent decides to send a message occasionally
                recipient = random.randint(0, self.num_agents - 1)
                if recipient != self.agent_id:
                    self.send_message(recipient, f"Hello from {self.agent_id}")

            time.sleep(random.uniform(0.01, 0.05)) # Agent's internal cycle time

    def stop(self):
        self.is_running = False

def simulate_communication(num_agents, duration):
    agents = [Agent(i, num_agents) for i in range(num_agents)]
    threads = []

    # Start message processing threads for each agent
    for agent in agents:
        thread = threading.Thread(target=agent.process_messages)
        threads.append(thread)
        thread.start()

    # Simulate initial messages to kick things off
    for i in range(min(num_agents, 5)): # Send a few initial messages
        agents[i].send_message(random.randint(0, num_agents - 1), f"Initial message {i}")

    print(f"Simulation started with {num_agents} agents for {duration} seconds.")
    time.sleep(duration)

    print("Stopping simulation...")
    for agent in agents:
        agent.stop()

    for thread in threads:
        thread.join()
    print("Simulation finished.")

if __name__ == "__main__":
    # To observe scaling issues, increase num_agents and observe:
    # 1. Increased 'Message lost' messages (simulated network congestion/failure)
    # 2. Longer simulation times (simulated processing bottlenecks)
    # 3. Potential for deadlocks or race conditions in more complex scenarios (not explicitly shown here)
    NUM_AGENTS = 50  # Try increasing this (e.g., 100, 500) to see effects
    SIMULATION_DURATION = 10 # seconds

    simulate_communication(NUM_AGENTS, SIMULATION_DURATION)
