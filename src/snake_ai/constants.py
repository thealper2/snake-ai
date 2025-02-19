# Game Constants
BLOCK_SIZE = 20 # Size of each block in the game
SPEED = 40 # Game speed (steps per second)
MAX_MEMORY = 100_000 # Maximum memory capacity for experience replay
BATCH_SIZE = 1000 # Number of samples to train on in each batch
LR = 0.001 # Learning rate for the neural network optimizer

# Game Window Dimensions
GAME_WIDTH = 480 # Width of the game area
GAME_HEIGHT = 480 # Height of the game area
STATS_WIDTH = 400 # Width of the stats/UI panel
WINDOW_WIDTH = GAME_WIDTH + STATS_WIDTH # Total window width (game + stats)
WINDOW_HEIGHT = GAME_HEIGHT # Total window height

# Color Definitions (RGB values)
WHITE = (255, 255, 255) # White color
RED = (200, 0, 0) # Red color
BLUE1 = (0, 0, 255) # Bright blue color
BLUE2 = (0, 100, 255) # Darker blue color
BLACK = (0, 0, 0) # Black color
GRAY = (80, 80, 80) # Gray color