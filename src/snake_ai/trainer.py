import torch
import torch.nn as nn
import torch.optim as optim

class QTrainer:
    def __init__(self, model, lr, gamma):
        # Neural network model
        self.model = model
        # Learning rate for optimizer
        self.lr = lr
        # Discount factor for future rewards
        self.gamma = gamma
        # Adam optimizer
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # Mean Squared Error loss function
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Convert inputs to PyTorch tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # Add batch dimension if input is 1D
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predict Q-values for the current state
        pred = self.model(state)
        # Clone predictions to use as target
        target = pred.clone()
        
        # Update Q-values for the actions taken
        for idx in range(len(done)):
            # Immediate reward
            Q_new = reward[idx]
            # If not terminal state, add discounted future reward
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            # Update target Q-value
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Perform optimization step
        # Clear gradients
        self.optimizer.zero_grad()
        # Compute loss between target and prediction
        loss = self.criterion(target, pred)
        # Backpropagate loss
        loss.backward()
        # Update model weights
        self.optimizer.step()