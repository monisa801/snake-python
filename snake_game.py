import pygame
import numpy as np
from collections import deque  # Used for BFS queue implementation
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
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.auto_mode = False  # Flag for BFS auto mode
        
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if food not in self.body:
                return food

    def bfs_path(self):
        """
        Breadth-First Search (BFS) implementation to find the shortest path to food.
        Returns a list of directions to reach the food.
        
        BFS Algorithm steps:
        1. Start from snake's head position
        2. Use a queue to explore all possible paths level by level
        3. Keep track of visited positions to avoid cycles
        4. Return the first path that reaches the food (guaranteed to be shortest)
        """
        start = self.body[0]  # Snake's head position
        queue = deque([(start, [])])  # Queue of (position, path) pairs
        visited = {start}  # Set of visited positions
        
        while queue:
            (x, y), path = queue.popleft()  # Get next position and its path
            
            # If we reached the food, return the path
            if (x, y) == self.food:
                return path
                
            # Explore all four possible directions (up, right, down, left)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                
                # Check if the next position is valid:
                # 1. Within grid boundaries
                # 2. Not visited before
                # 3. Not part of snake's body
                if (0 <= next_x < GRID_COUNT and 0 <= next_y < GRID_COUNT and 
                    (next_x, next_y) not in visited and 
                    (next_x, next_y) not in self.body):
                    visited.add((next_x, next_y))
                    queue.append(((next_x, next_y), path + [(dx, dy)]))
        return None  # No path found

    def move(self):
        # If in auto mode, use BFS to find the next move
        if self.auto_mode:
            path = self.bfs_path()
            if path and len(path) > 0:
                self.direction = path[0]  # Take the first step in the path
        
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
            self.score += 1
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
        
        # Draw score and mode
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        mode_text = font.render(f'Mode: {"Auto (BFS)" if self.auto_mode else "Manual"}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(mode_text, (10, 50))
        
        pygame.display.flip()

def show_game_over(score):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Create game over box
    box_width = 400
    box_height = 300
    box_x = (WINDOW_SIZE - box_width) // 2
    box_y = (WINDOW_SIZE - box_height) // 2
    
    # Draw box background
    pygame.draw.rect(screen, DARK_GRAY, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)
    
    # Draw text
    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    
    game_over_text = font_large.render("Game Over!", True, WHITE)
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    
    screen.blit(game_over_text, (box_x + (box_width - game_over_text.get_width()) // 2, box_y + 40))
    screen.blit(score_text, (box_x + (box_width - score_text.get_width()) // 2, box_y + 120))
    
    # Create buttons
    button_width = 150
    button_height = 50
    button_spacing = 20
    total_width = button_width * 2 + button_spacing
    start_x = box_x + (box_width - total_width) // 2
    
    new_game_button = Button(start_x, box_y + 180, button_width, button_height, 
                           "New Game", GRAY, LIGHT_GRAY)
    quit_button = Button(start_x + button_width + button_spacing, box_y + 180, 
                        button_width, button_height, "Quit", GRAY, LIGHT_GRAY)
    
    new_game_button.draw(screen)
    quit_button.draw(screen)
    
    pygame.display.flip()
    
    return new_game_button, quit_button

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:  # Toggle between manual and BFS auto mode
                    snake.auto_mode = not snake.auto_mode
                elif not game_over and not snake.auto_mode:
                    # Handle arrow key controls (only in manual mode)
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            if not snake.move():
                game_over = True
                new_game_button, quit_button = show_game_over(snake.score)
            snake.draw()
        else:
            # Handle button events
            for event in pygame.event.get():
                if new_game_button.handle_event(event):
                    snake = Snake()
                    game_over = False
                elif quit_button.handle_event(event):
                    running = False
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
        clock.tick(10)  # Control game speed
        
    pygame.quit()

if __name__ == "__main__":
    main() 