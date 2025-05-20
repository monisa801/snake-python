import pygame
import numpy as np
from collections import deque
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game with BFS")

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if food not in self.body:
                return food
    
    def bfs_path(self):
        start = self.body[0]
        queue = deque([(start, [])])
        visited = {start}
        
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.food:
                return path
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < GRID_COUNT and 0 <= next_y < GRID_COUNT and 
                    (next_x, next_y) not in visited and 
                    (next_x, next_y) not in self.body):
                    visited.add((next_x, next_y))
                    queue.append(((next_x, next_y), path + [(dx, dy)]))
        return None

    def move(self):
        path = self.bfs_path()
        if path and len(path) > 0:
            self.direction = path[0]
        
        new_head = (self.body[0][0] + self.direction[0], 
                   self.body[0][1] + self.direction[1])
        
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= GRID_COUNT or
            new_head in self.body):
            return False
            
        self.body.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.body.pop()
            
        return True

    def draw(self):
        screen.fill(BLACK)
        
        # Draw snake
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                            GRID_SIZE-2, GRID_SIZE-2))
        
        # Draw food
        pygame.draw.rect(screen, RED,
                        (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE,
                         GRID_SIZE-2, GRID_SIZE-2))
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if not snake.move():
            running = False
            
        snake.draw()
        clock.tick(10)  # Control game speed
        
    pygame.quit()

if __name__ == "__main__":
    main() 