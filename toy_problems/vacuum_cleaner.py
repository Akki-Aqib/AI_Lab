"""
Vacuum Cleaner Problem - Reflex Agent Simulation
Rooms: A and B — agent cleans dirty rooms and moves between them
"""

class VacuumWorld:
    def __init__(self, room_a='Dirty', room_b='Dirty', position='A'):
        self.rooms = {'A': room_a, 'B': room_b}
        self.position = position
        self.performance = 0
        self.steps = 0

    def perceive(self):
        return (self.position, self.rooms[self.position])

    def act(self):
        location, status = self.perceive()
        if status == 'Dirty':
            action = 'Suck'
            self.rooms[location] = 'Clean'
            self.performance += 10
        elif location == 'A':
            action = 'Move Right'
            self.position = 'B'
        else:
            action = 'Move Left'
            self.position = 'A'
        self.steps += 1
        return action

    def is_clean(self):
        return all(s == 'Clean' for s in self.rooms.values())

    def display(self, action=""):
        print(f"Step {self.steps:2d} | Pos: {self.position} | "
              f"A:{self.rooms['A']:5s} | B:{self.rooms['B']:5s} | "
              f"Action: {action:12s} | Score: {self.performance}")

def run_simulation(room_a, room_b, start_pos, max_steps=10):
    print(f"\n=== Vacuum Cleaner Agent ===")
    print(f"Initial: Room A={room_a}, Room B={room_b}, Agent at={start_pos}")
    print("-" * 70)
    agent = VacuumWorld(room_a, room_b, start_pos)
    agent.display("Start")
    for _ in range(max_steps):
        if agent.is_clean():
            print("\nAll rooms are clean! Task complete.")
            break
        action = agent.act()
        agent.display(action)
    print(f"\nFinal Performance Score: {agent.performance}")

if __name__ == "__main__":
    # Test all 4 initial states
    configs = [
        ('Dirty', 'Dirty', 'A'),
        ('Dirty', 'Clean', 'A'),
        ('Clean', 'Dirty', 'B'),
        ('Clean', 'Clean', 'A'),
    ]
    for ra, rb, pos in configs:
        run_simulation(ra, rb, pos, max_steps=6)
        print()
