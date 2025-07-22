from collections import deque

class Agent:
    def __init__(self, env):
        self.env = env
        self.visited = set()
        self.safe = set()
        self.unsafe = set()
        self.frontier = set()
        self.path = []
        self.current_pos = env.agent_pos
        self.has_gold = False
        self.safe.add(self.current_pos)
        self.path.append(self.current_pos)
        self.parent = {(0, 0): None}  # For path backtracking


    def update_knowledge(self, percepts):
        x, y = self.current_pos
        self.visited.add((x, y))
        self.frontier.discard((x, y))

        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if not percepts["breeze"] and not percepts["stench"]:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
                    if (nx, ny) not in self.visited:
                        self.safe.add((nx, ny))
                        self.frontier.add((nx, ny))
        else:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
                    if (nx, ny) not in self.visited and (nx, ny) not in self.safe:
                        self.unsafe.add((nx, ny))

    def choose_next_move(self):
        # Safe and unvisited
        for pos in sorted(self.safe - self.visited):
            return pos

        # Explore frontier
        for pos in sorted(self.frontier - self.visited):
            return pos

        # Backtrack to find new frontiers
        for pos in reversed(self.path):
            neighbors = [(pos[0] + dx, pos[1] + dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]]
            for neighbor in neighbors:
                if neighbor in self.safe and neighbor not in self.visited:
                    return neighbor

        return None

    def face_direction(self, target_dir):
        directions = ["up", "right", "down", "left"]
        while self.env.agent_dir != target_dir:
            self.env.turn_right()

    def move_to(self, pos):
        if pos not in self.visited:
           self.parent[pos] = self.current_pos  # Track parent
        
        x, y = self.current_pos
        nx, ny = pos
        dx, dy = nx - x, ny - y

        if dx == -1:
            self.env.agent_dir = "up"
        elif dx == 1:
            self.env.agent_dir = "down"
        elif dy == -1:
            self.env.agent_dir = "left"
        elif dy == 1:
            self.env.agent_dir = "right"



        self.env.agent_pos = pos
        self.env.percepts = self.env.get_percepts()
        percepts = self.env.percepts

        if percepts.get("bump"):
           print(f"Bump! Hit a wall at {pos}. Reverting to {self.current_pos}")
        # Undo move if bump occurred
           self.env.agent_pos = self.current_pos  # Stay at current pos
           self.unsafe.add(pos)  # Mark as unsafe to avoid future attempts
           return False

        self.current_pos = pos
        self.visited.add(pos)
        if pos in self.frontier:
          self.frontier.remove(pos)
        return True

    def get_backtrack_move(self):
       if self.current_pos == (0, 0):
          return (0, 0)

    # BFS from current position to (0, 0)
       queue = deque()
       queue.append((self.current_pos, []))
       visited_bfs = set()
    
       while queue:
         current, path = queue.popleft()
         if current in visited_bfs:
            continue
         visited_bfs.add(current)

         if current == (0, 0):
            if path:
                return path[0]
            else:
                return (0, 0)

         x, y = current
         neighbors = [(x + dx, y + dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]
         for neighbor in neighbors:
            if (0 <= neighbor[0] < self.env.grid_size and 
                0 <= neighbor[1] < self.env.grid_size and
                neighbor in self.safe):
                queue.append((neighbor, path + [neighbor]))

    # If no path found, stay in place
       return self.current_pos



    
        
    def get_safe_unvisited_neighbors(self):
         x, y = self.current_pos
         neighbors = [(x + dx, y + dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]
         safe_moves = [
           (nx, ny) for (nx, ny) in neighbors
           if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size
           and (nx, ny) in self.safe
           and (nx, ny) not in self.visited
           and (nx, ny) not in self.unsafe  # Avoid bumped cells
    ]
         return safe_moves

    

    


    def try_shoot(self):
        percepts = self.env.percepts
        if percepts["stench"] and self.env.wumpus_alive and self.env.has_arrow:
            print("Agent tries to shoot the Wumpus!")
            success = self.env.shoot_arrow()
            print("Wumpus killed!" if success else "Arrow missed.")
            return success
        return False

    def act(self, percepts): 
        if not self.env.agent_alive:
           print("Agent is dead. Game Over.")
           return False
        
        


        

        if not self.env.wumpus_alive and percepts["stench"]:
          print("Stench lingers, but Wumpus is already dead.")


        if self.has_gold:
           if self.current_pos == (0, 0):
              print("Agent has returned with the gold! WIN!")
              return False
           else:
            next_move = self.get_backtrack_move()
            print(f"Returning to start. Moving to {next_move}")
            self.move_to(next_move)
            return True

        self.update_knowledge(percepts)

    
        if percepts['glitter']:
          self.has_gold = self.env.grab_gold()
          print("Gold grabbed!")
          return True

    
        self.try_shoot()

        safe_moves = self.get_safe_unvisited_neighbors()
        if safe_moves:
          for next_move in safe_moves:
            print(f"Trying to move to safe cell {next_move}")
            if self.move_to(next_move):
               return True
            else:
               print(f"Failed to move to {next_move} due to bump.")

        
        if not safe_moves and self.get_backtrack_move() == self.current_pos:
          print("Agent is stuck and cannot move safely. Terminating.")
          return False

        backtrack_move = self.get_backtrack_move()
        print(f"No safe unvisited cells. Backtracking to {backtrack_move}")
        self.move_to(backtrack_move)
        return True
