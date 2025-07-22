import random
import pygame
import sys
import time
from agent import Agent
import os




CELL_SIZE = 100
GRID_SIZE = 4
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE + 100, CELL_SIZE * GRID_SIZE + 200
import os
import pygame

script_dir = os.path.dirname(__file__)  # Gets the folder where this script is located
wumpus_img = pygame.image.load(os.path.join(script_dir, "assets", "wumpus.png"))

wumpus_img = pygame.transform.scale(wumpus_img, (CELL_SIZE, CELL_SIZE))

agent_img = pygame.image.load(os.path.join(script_dir, "assets", "agent.png"))
agent_img = pygame.transform.scale(agent_img, (CELL_SIZE, CELL_SIZE))



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World Visualization")
clock = pygame.time.Clock()


class WumpusWorld:
    def __init__(self):
        self.grid_size = 4
        self.agent_pos = (0, 0)  # Starting at (1,1) in grid notation
        self.agent_dir = "right"  # Initial direction
        self.has_gold = False
        self.has_arrow = True
        self.wumpus_alive = True
        self.world = self.generate_world()
        self.percepts = self.get_percepts()
        self.agent_alive = True

    def generate_world(self):
        # Initialize empty grid
        world = [[{"pit": False, "wumpus": False, "gold": False} for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Place pits (20% chance per cell, except start)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) != (0, 0) and random.random() < 0.2:
                    world[i][j]["pit"] = True
        
        # Place Wumpus (random, not at start)
        wumpus_pos = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        while wumpus_pos == (0, 0):
            wumpus_pos = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        world[wumpus_pos[0]][wumpus_pos[1]]["wumpus"] = True
        
        # Place gold (random, not at start)
        gold_pos = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        while gold_pos == (0, 0):
            gold_pos = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        world[gold_pos[0]][gold_pos[1]]["gold"] = True
        
        return world

    def get_percepts(self):
        x, y = self.agent_pos
        cell = self.world[x][y]
        percepts = {
            "stench": False,
            "breeze": False,
            "glitter": False,
            "bump": False,
            "scream": False
        }
        
        # Check adjacent cells for Wumpus (stench) and pits (breeze)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if self.world[nx][ny]["wumpus"] and self.wumpus_alive:
                    percepts["stench"] = True
                if self.world[nx][ny]["pit"]:
                    percepts["breeze"] = True
        
        # Current cell percepts
        if cell["gold"]:
            percepts["glitter"] = True
        
        return percepts

    def move_forward(self):
        x, y = self.agent_pos
        new_x, new_y = x, y
        
        if self.agent_dir == "up":
            new_x -= 1
        elif self.agent_dir == "down":
            new_x += 1
        elif self.agent_dir == "left":
            new_y -= 1
        elif self.agent_dir == "right":
            new_y += 1
        
        # Check if move is valid
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.agent_pos = (new_x, new_y)
            self.percepts = self.get_percepts()
            return True
        else:
            self.percepts["bump"] = True
            return False

    def turn_left(self):
        dirs = ["up", "left", "down", "right"]
        idx = dirs.index(self.agent_dir)
        self.agent_dir = dirs[(idx + 1) % 4]
        self.percepts = self.get_percepts()

    def turn_right(self):
        dirs = ["up", "right", "down", "left"]
        idx = dirs.index(self.agent_dir)
        self.agent_dir = dirs[(idx + 1) % 4]
        self.percepts = self.get_percepts()

    def shoot_arrow(self):
        if not self.has_arrow:
            return False
        
        self.has_arrow = False
        x, y = self.agent_pos
        wumpus_killed = False
        
        # Arrow travels in a straight line in the current direction
        if self.agent_dir == "up":
            for i in range(x - 1, -1, -1):
                if self.world[i][y]["wumpus"]:
                    wumpus_killed = True
                    break
        elif self.agent_dir == "down":
            for i in range(x + 1, self.grid_size):
                if self.world[i][y]["wumpus"]:
                    wumpus_killed = True
                    break
        elif self.agent_dir == "left":
            for j in range(y - 1, -1, -1):
                if self.world[x][j]["wumpus"]:
                    wumpus_killed = True
                    break
        elif self.agent_dir == "right":
            for j in range(y + 1, self.grid_size):
                if self.world[x][j]["wumpus"]:
                    wumpus_killed = True
                    break
        
        if wumpus_killed:
            self.wumpus_alive = False
            self.percepts["scream"] = True
            
        return wumpus_killed

    def grab_gold(self):
        x, y = self.agent_pos
        if self.world[x][y]["gold"]:
            self.has_gold = True
            self.world[x][y]["gold"] = False
            self.percepts["glitter"] = False
            return True
        return False

    def is_game_over(self):
        x, y = self.agent_pos
        cell = self.world[x][y]
        if (cell["pit"] or (cell["wumpus"] and self.wumpus_alive)):
            return "lose"
        if self.has_gold and self.agent_pos == (0, 0):
            return "win"
        return "continue"
    
def draw_world(env, agent, step_count):
        screen.fill((0, 0, 0))  # black background

        font = pygame.font.SysFont(None, 24)

        for i in range(env.grid_size):
            for j in range(env.grid_size):
               x = j * CELL_SIZE
               y = i * CELL_SIZE
               rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Draw white cell
               pygame.draw.rect(screen, (255, 255, 255), rect)

            # Pit
               if env.world[i][j]["pit"]:
                 pygame.draw.circle(screen, (100, 100, 100), rect.center, 20)

            # Wumpus
               if env.world[i][j]["wumpus"] and env.wumpus_alive:
                 screen.blit(wumpus_img, (x, y))

            # Gold
               if env.world[i][j]["gold"]:
                 pygame.draw.circle(screen, (255, 255, 0), rect.center, 15)

            # Grid lines
               pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    # Agent
        ax, ay = env.agent_pos
        cell_size = 100
        top_x = ay * cell_size
        top_y = ax * cell_size

        screen.blit(agent_img, (top_x, top_y))

        # Triangle size
        triangle_height = 20
        triangle_base = 14

        if env.agent_dir == "up":
            points = [
                 (top_x + cell_size // 2, top_y + 5),  # tip near top center with 5px padding from top edge
                 (top_x + (cell_size // 2) - triangle_base // 2, top_y + 5 + triangle_height),
                 (top_x + (cell_size // 2) + triangle_base // 2, top_y + 5 + triangle_height),
    ]
        elif env.agent_dir == "down":
            points = [
                 (top_x + cell_size // 2, top_y + cell_size - 5),  # tip near bottom center with 5px padding
                (top_x + (cell_size // 2) - triangle_base // 2, top_y + cell_size - 5 - triangle_height),
                (top_x + (cell_size // 2) + triangle_base // 2, top_y + cell_size - 5 - triangle_height),
    ]
        elif env.agent_dir == "left":
            points = [
                (top_x + 5, top_y + cell_size // 2),  # tip near left center with 5px padding
                (top_x + 5 + triangle_height, top_y + (cell_size // 2) - triangle_base // 2),
                (top_x + 5 + triangle_height, top_y + (cell_size // 2) + triangle_base // 2),
    ]
        elif env.agent_dir == "right":
            points = [
               (top_x + cell_size - 5, top_y + cell_size // 2),  # tip near right center with 5px padding
               (top_x + cell_size - 5 - triangle_height, top_y + (cell_size // 2) - triangle_base // 2),
               (top_x + cell_size - 5 - triangle_height, top_y + (cell_size // 2) + triangle_base // 2),
    ]
       

        pygame.draw.polygon(screen, (255,0, 0), points)


    # Display percepts at top-left
        base_y = CELL_SIZE * GRID_SIZE + 30
        

    # Display step count and agent state
        state_text = f"Step: {step_count} | Gold: {env.has_gold} | Arrow: {env.has_arrow} | Wumpus alive: {env.wumpus_alive}"
        state_surface = font.render(state_text, True, (173, 216, 230))
        screen.blit(state_surface, (10, base_y))

        percept_texts = [f"{key.capitalize()}: {value}" for key, value in env.percepts.items()]
       
        for idx, ptext in enumerate(percept_texts):
           text_surface = font.render(ptext, True, (255, 255, 255))
           screen.blit(text_surface, (10, base_y + 30 + idx * 30))

        pygame.display.flip()
