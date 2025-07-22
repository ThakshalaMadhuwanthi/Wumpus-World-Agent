from wumpus_world import WumpusWorld, draw_world
from agent import Agent
import pygame


def main():
    pygame.init()
    env = WumpusWorld()
    agent = Agent(env)
    clock = pygame.time.Clock()
    step = 0
    running = True

    print("Agent starts at (0, 0). Percepts:", env.percepts)

    while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
              running = False

       draw_world(env, agent, step)

       if env.is_game_over() != "continue":
          print("Game Over:", env.is_game_over())
          pygame.time.wait(5000)
          break

       continue_running = agent.act(env.percepts)
       
       if not continue_running:
             running = False
   
       step += 1
       if step > 20:
            print("Step limit reached.")
            running = False

       clock.tick(0.25)

    pygame.quit()

if __name__ == "__main__":
    main()