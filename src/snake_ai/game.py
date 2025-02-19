import csv
import time
import random
import pygame
import numpy as np

from datetime import datetime

from src.snake_ai.constants import *

class SnakeGame:
    def __init__(self):
        pygame.init()
        # Initialize game window
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Set window title
        pygame.display.set_caption('Snake AI')
        # Initialize clock for controlling game speed
        self.clock = pygame.time.Clock()
        
        # Game statistics
        self.game_count = 0
        self.total_score = 0
        self.record = 0
        self.total_apples = 0
        self.longest_snake = 0
        self.death_reason = ""
        self.total_steps = 0
        # CSV file for saving stats
        self.csv_file = f'stats/snake_stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        # Initialize CSV file with headers
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Game', 'Score', 'Steps', 'Length', 'Time', 'Death_Reason', 
                           'Total_Apples', 'Avg_Score', 'Best_Score', 'Longest_Snake'])
        
        # Reset game state
        self.reset()

    def reset(self):
        # Initialize snake and game state
        self.direction = 'RIGHT'
        # Snake head starting position
        self.head = [GAME_WIDTH/2, GAME_HEIGHT/2]
        # Initialize snake body
        self.snake = [self.head,
                     [self.head[0]-BLOCK_SIZE, self.head[1]],
                     [self.head[0]-2*BLOCK_SIZE, self.head[1]]]
        self.score = 0
        self.food = None
        # Place food randomly
        self._place_food()
        # Step counter
        self.frame_iteration = 0
        # Track game start time
        self.start_time = time.time()
        
    def _place_food(self):
        # RAndomly place food on the grid
        x = random.randint(0, (GAME_WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (GAME_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = [x, y]
        # Ensure food doesn't spawn on the snake
        if self.food in self.snake:
            self._place_food()

    def save_stats(self, game_over=False):
        # Savev game statistics to CSV
        elapsed_time = int(time.time() - self.start_time)
        avg_score = self.total_score / max(1, self.game_count)
        
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.game_count,
                self.score,
                self.frame_iteration,
                len(self.snake),
                elapsed_time,
                self.death_reason if game_over else "In Progress",
                self.total_apples,
                avg_score,
                self.record,
                self.longest_snake
            ])

    def play_step(self, action):
        # Execute one step of the game
        self.frame_iteration += 1
        for event in pygame.event.get():
            # Handle window close event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Move snake based on action
        self._move(action)
        # Add new head to snake
        self.snake.insert(0, list(self.head))
        
        reward = 0
        game_over = False
        # Check for collision or timeout
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            self.death_reason = "Collision" if self.is_collision() else "Timeout"
            self.save_stats(game_over=True)
            return reward, game_over, self.score
            
        # Check if snaek eats food
        if self.head == self.food:
            self.score += 1
            self.total_apples += 1
            reward = 10
            self._place_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
        # Update records
        if self.score > self.record:
            self.record = self.score
        if len(self.snake) > self.longest_snake:
            self.longest_snake = len(self.snake)
            
        # Update game window
        self._update_ui()
        # Control game speed
        self.clock.tick(SPEED)
        
        # Periodically save stats
        if self.frame_iteration % 100 == 0:
            self.save_stats()
        
        return reward, game_over, self.score

    def _update_ui(self):
        # Render game visuals
        # Clear screen
        self.display.fill(BLACK)
        
        # Draw divider
        pygame.draw.line(self.display, WHITE, (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT), 2)

        # Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0]+4, pt[1]+4, 12, 12))
        
        # Draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Render statistics
        font = pygame.font.Font(None, 28)
        stats_x = GAME_WIDTH + 20

        title_font = pygame.font.Font(None, 36)
        title = title_font.render('Statistics', True, WHITE)
        self.display.blit(title, (stats_x, 20))
        
        stats = [
            f'Game: {self.game_count}',
            f'Current Score: {self.score}',
            f'Best Score: {self.record}',
            f'Average Score: {self.total_score/max(1, self.game_count):.1f}',
            f'Steps: {self.frame_iteration}',
            f'Snake Length: {len(self.snake)}',
            f'Total Apples: {self.total_apples}',
            f'Longest Snake: {self.longest_snake}',
            f'Time: {int(time.time() - self.start_time)}s',
            f'Death Reason: {self.death_reason}'
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, WHITE)
            self.display.blit(text, (stats_x, 70 + i * 35))
        
        # Update display
        pygame.display.flip()

    def is_collision(self, pt=None):
        # Check for collisions with walls or self
        if pt is None:
            pt = self.head

        if pt[0] > GAME_WIDTH - BLOCK_SIZE or pt[0] < 0 or pt[1] > GAME_HEIGHT - BLOCK_SIZE or pt[1] < 0:
            self.death_reason = "Wall"
            return True

        if pt in self.snake[1:]:
            self.death_reason = "Self"
            return True
        return False

    def _move(self, action):
        # Update snake direction based on action
        clock_wise = ['RIGHT', 'DOWN', 'LEFT', 'UP']
        idx = clock_wise.index(self.direction)
        
        # Go straight
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        # Turn right
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        # Turn left
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]
            
        self.direction = new_dir
        
        # Update head position based on direction
        x = self.head[0]
        y = self.head[1]
        if self.direction == 'RIGHT':
            x += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE
        elif self.direction == 'UP':
            y -= BLOCK_SIZE
            
        self.head = [x, y]