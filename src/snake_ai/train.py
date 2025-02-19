from src.snake_ai.agent import Agent
from src.snake_ai.game import SnakeGame

def train():
    # Initialize lists to track scores and mean scores for plotting
    plot_scores = []
    plot_mean_scores = []
    total_score = 0 # Total score across all games
    record = 0 # Best score achieved
    agent = Agent() # Initialize the agent
    game = SnakeGame() # Initialize the game
    
    # Main training loop
    while True:
        # Get the current state of the game
        state_old = agent.get_state(game)
        
        # Choose an action based on the current state
        final_move = agent.get_action(state_old)
        
        # Execute the action and get the reward, game status and score
        reward, done, score = game.play_step(final_move)
        # Get the new state after the action
        state_new = agent.get_state(game)
        
        # Train the agent on the short-term memory (single step)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
        # Store the experience in the agent's memory
        agent.remember(state_old, final_move, reward, state_new, done)
        
        # If the game is over
        if done:
            # Reset the game
            game.reset()
            # Increment tthe number of games played
            agent.n_games += 1
            # Update the game count
            game.game_count = agent.n_games
            # Update the total score
            game.total_score += score
            # Train the agent on the long-term memory (batch of experiences)
            agent.train_long_memory()
            
            # Update the record if a new high score is achieved
            if score > record:
                record = score
                # Save the model with the new record score
                agent.save_model(score)
                
            # Print game statistics
            print('Game:', agent.n_games, 'Score:', score, 'Record:', record)