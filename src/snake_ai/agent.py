import os
import torch
import random
import numpy as np

from collections import deque
from datetime import datetime

from src.snake_ai.constants import *
from src.snake_ai.model import QNet
from src.snake_ai.trainer import QTrainer

class Agent:
    def __init__(self):
        # Number of games played
        self.n_games = 0
        # Exploration rate (for epsilon-greedy strategy)
        self.epsilon = 0
        # Discount factor for future rewards
        self.gamma = 0.9
        # Replay memory with a maximum size
        self.memory = deque(maxlen=MAX_MEMORY)
        # Neural network model (input_size=11, hidden_size=256, output_size=3)
        self.model = QNet(11, 256, 3)
        # Trainer for the model
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
    def get_state(self, game):
        # Get the current state of the game
        # Snake's head position
        head = game.snake[0] 
        # Point to the left of the head
        point_l = [head[0] - BLOCK_SIZE, head[1]]
        # Point to the right of the head
        point_r = [head[0] + BLOCK_SIZE, head[1]]
        # Point above the head
        point_u = [head[0], head[1] - BLOCK_SIZE]
        # Point below the head
        point_d = [head[0], head[1] + BLOCK_SIZE]
        
        # Current direction of the snake
        dir_l = game.direction == 'LEFT'
        dir_r = game.direction == 'RIGHT'
        dir_u = game.direction == 'UP'
        dir_d = game.direction == 'DOWN'
        
        # Define the state vector
        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
            
            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),
            
            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),
            
            # Current direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location relative to the head
            game.food[0] < game.head[0], # Food is to the left
            game.food[0] > game.head[0], # Food is to the right
            game.food[1] < game.head[1], # Food is above
            game.food[1] > game.head[1] # Food is below
        ]
        
        # Convert state to a numpy array
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        # Store the experience in memory
        self.memory.append((state, action, reward, next_state, done))
        
    def train_long_memory(self):
        # Train the model using a batch of experiences from memory
        if len(self.memory) > BATCH_SIZE:
            # Randomly sample a batch
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            # Use all memories if fewer than BATCH_SIZE
            mini_sample = self.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        # Train the model
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        # Train the model on a single experience
        self.trainer.train_step(state, action, reward, next_state, done)
        
    def get_action(self, state):
        # Choose an action using epsilon-greedy strategy
        # Decrease exploration rate over time
        self.epsilon = 80 - self.n_games
        # Initialize action vector
        final_move = [0, 0, 0]

        # Explore: choose a random action
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            # Exploit: choose the best action based on the model's prediction
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move

    def save_model(self, score):
            # Save the model's state to a file
            # Folder the save models
            model_folder_path = 'models'
            file_name = os.path.join(model_folder_path, f'model_{score}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pth')
            # save the model
            torch.save(self.model.state_dict(), file_name)