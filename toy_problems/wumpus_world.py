"""
Wumpus World - Knowledge-Based Agent Simulation
4x4 grid with Wumpus, Pits, Gold and an Agent
"""
import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[{'pit': False, 'wumpus': False, 'gold': False, 'visited': False} 
                       for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)
        self.agent_dir = 'right'
        self.alive = True
        self.has_gold = False
        self.arrow = True
        self.score = 0
        self._setup_world()

    def _setup_world(self):
        # Place Wumpus
        wx, wy = random.randint(0, self.size-1), random.randint(1, self.size-1)
        self.grid[wx][wy]['wumpus'] = True
        self.wumpus_pos = (wx, wy)
        # Place Pits (20% chance each cell except start)
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) != (0, 0) and (i, j) != (wx, wy):
                    if random.random() < 0.2:
                        self.grid[i][j]['pit'] = True
        # Place Gold
        gx, gy = random.randint(0, self.size-1), random.randint(1, self.size-1)
        self.grid[gx][gy]['gold'] = True
        self.gold_pos = (gx, gy)
        self.grid[0][0]['visited'] = True

    def get_percepts(self, x, y):
        percepts = {'stench': False, 'breeze': False, 'glitter': False, 'bump': False, 'scream': False}
        if self.grid[x][y]['gold']:
            percepts['glitter'] = True
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[nx][ny]['wumpus']:
                    percepts['stench'] = True
                if self.grid[nx][ny]['pit']:
                    percepts['breeze'] = True
        return percepts

    def move_agent(self, action):
        x, y = self.agent_pos
        self.score -= 1
        if action == 'forward':
            dirs = {'right':(0,1),'left':(0,-1),'up':(-1,0),'down':(1,0)}
            dx, dy = dirs[self.agent_dir]
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                self.agent_pos = (nx, ny)
                self.grid[nx][ny]['visited'] = True
                if self.grid[nx][ny]['wumpus']:
                    print("Agent eaten by Wumpus! Game Over.")
                    self.alive = False; self.score -= 1000
                elif self.grid[nx][ny]['pit']:
                    print("Agent fell into a pit! Game Over.")
                    self.alive = False; self.score -= 1000
            else:
                print("Bump! Hit a wall.")
        elif action == 'grab' and self.grid[x][y]['gold']:
            self.has_gold = True
            self.grid[x][y]['gold'] = False
            self.score += 1000
            print("Gold grabbed! +1000 points")
        elif action == 'shoot' and self.arrow:
            self.arrow = False; self.score -= 10
            dirs = {'right':(0,1),'left':(0,-1),'up':(-1,0),'down':(1,0)}
            dx, dy = dirs[self.agent_dir]
            ax, ay = x+dx, y+dy
            while 0 <= ax < self.size and 0 <= ay < self.size:
                if self.grid[ax][ay]['wumpus']:
                    self.grid[ax][ay]['wumpus'] = False
                    print("Wumpus killed! Scream heard."); break
                ax, ay = ax+dx, ay+dy
        elif action == 'climb' and self.agent_pos == (0,0):
            if self.has_gold:
                self.score += 500
                print(f"Escaped with gold! Final score: {self.score}")
            else:
                print(f"Escaped without gold. Score: {self.score}")

    def display(self):
        print("\n  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            row = str(i) + " "
            for j in range(self.size):
                cell = self.grid[i][j]
                if (i, j) == self.agent_pos:
                    row += "A "
                elif cell['wumpus']:
                    row += "W "
                elif cell['pit']:
                    row += "P "
                elif cell['gold']:
                    row += "G "
                elif cell['visited']:
                    row += ". "
                else:
                    row += "? "
            print(row)
        print(f"Agent at: {self.agent_pos} | Score: {self.score} | Has Gold: {self.has_gold}")

if __name__ == "__main__":
    print("=== Wumpus World Simulation ===")
    world = WumpusWorld(4)
    world.display()
    percepts = world.get_percepts(*world.agent_pos)
    print(f"\nPercepts at start: {percepts}")
    print(f"\nGold is at: {world.gold_pos}, Wumpus is at: {world.wumpus_pos}")

    actions = ['forward', 'forward', 'grab', 'climb']
    for act in actions:
        if world.alive:
            print(f"\nAction: {act}")
            world.move_agent(act)
            if world.alive:
                world.display()
                print("Percepts:", world.get_percepts(*world.agent_pos))
