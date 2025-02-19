import os

from src.snake_ai.train import train

if not os.path.exists('models'):
    os.makedirs('models')
if not os.path.exists('stats'):
    os.makedirs('stats')

if __name__ == '__main__':
    train()