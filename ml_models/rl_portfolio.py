"""
Reinforcement Learning (PPO) for Dynamic Portfolio Allocation
Optimizes asset allocation based on risk profile and market conditions
"""
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from typing import Dict, List, Tuple
import os


class PortfolioEnv(gym.Env):
    """
    Custom Gymnasium environment for portfolio optimization
    """
    
    def __init__(self, initial_amount: float, risk_level: int = 1):
        """
        Initialize environment
        
        Args:
            initial_amount: Initial investment amount
            risk_level: 0 (Low), 1 (Medium), 2 (High)
        """
        super(PortfolioEnv, self).__init__()
        
        self.initial_amount = initial_amount
        self.risk_level = risk_level
        
        # Asset classes: [SIP, Mutual Funds, Stocks, FD, Savings, Insurance]
        self.n_assets = 6
        
        # Action space: allocation percentages (must sum to 100)
        self.action_space = spaces.Box(
            low=0, high=1, shape=(self.n_assets,), dtype=np.float32
        )
        
        # Observation space: [amount, risk_level, market_state, portfolio_value, time_step]
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(5,), dtype=np.float32
        )
        
        # Expected returns and risks for each asset class (annual %)
        self.asset_returns = {
            0: {'low': 8, 'medium': 10, 'high': 12},    # SIP
            1: {'low': 7, 'medium': 9, 'high': 11},     # Mutual Funds
            2: {'low': 6, 'medium': 12, 'high': 18},    # Stocks
            3: {'low': 6.5, 'medium': 6.5, 'high': 6.5}, # FD
            4: {'low': 4, 'medium': 4, 'high': 4},      # Savings
            5: {'low': 0, 'medium': 0, 'high': 0}       # Insurance (protection)
        }
        
        self.asset_risks = [0.05, 0.08, 0.20, 0.01, 0.00, 0.00]  # Volatility
        
        self.reset()
    
    def reset(self, seed=None, options=None):
        """Reset environment"""
        super().reset(seed=seed)
        
        self.portfolio_value = self.initial_amount
        self.time_step = 0
        self.market_state = 0  # -1: bearish, 0: neutral, 1: bullish
        
        return self._get_observation(), {}
    
    def _get_observation(self):
        """Get current observation"""
        return np.array([
            self.initial_amount,
            self.risk_level,
            self.market_state,
            self.portfolio_value,
            self.time_step
        ], dtype=np.float32)
    
    def step(self, action):
        """
        Execute one step
        
        Args:
            action: Allocation percentages for each asset
        
        Returns:
            observation, reward, done, truncated, info
        """
        # Normalize action to ensure sum = 1
        action = action / (np.sum(action) + 1e-8)
        
        # Calculate allocation amounts
        allocations = action * self.portfolio_value
        
        # Simulate returns for each asset class
        risk_levels = ['low', 'medium', 'high']
        risk_key = risk_levels[self.risk_level]
        
        total_return = 0
        total_risk = 0
        
        for i in range(self.n_assets):
            if allocations[i] > 0:
                # Get expected return
                expected_return = self.asset_returns[i][risk_key] / 100
                
                # Add market randomness
                actual_return = np.random.normal(expected_return, self.asset_risks[i])
                
                # Calculate return
                asset_gain = allocations[i] * actual_return
                total_return += asset_gain
                
                # Calculate risk contribution
                total_risk += allocations[i] * self.asset_risks[i]
        
        # Update portfolio value
        self.portfolio_value += total_return
        
        # Calculate reward
        reward = self._calculate_reward(total_return, total_risk, action)
        
        # Update time step
        self.time_step += 1
        
        # Episode ends after 12 steps (12 months)
        done = self.time_step >= 12
        truncated = False
        
        # Update market state randomly
        self.market_state = np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])
        
        info = {
            'portfolio_value': self.portfolio_value,
            'total_return': total_return,
            'allocation': action
        }
        
        return self._get_observation(), reward, done, truncated, info
    
    def _calculate_reward(self, returns: float, risk: float, action: np.ndarray) -> float:
        """
        Calculate reward based on returns, risk, and constraints
        
        Args:
            returns: Total returns
            risk: Total risk
            action: Allocation action
        
        Returns:
            Reward value
        """
        # Base reward: returns
        reward = returns
        
        # Penalize risk based on risk level
        risk_penalties = {0: 2.0, 1: 1.0, 2: 0.5}  # Low risk = high penalty for risk
        reward -= risk * risk_penalties[self.risk_level]
        
        # Penalize extreme allocations (encourage diversification)
        diversification_penalty = np.sum(np.square(action - 1/self.n_assets)) * 100
        reward -= diversification_penalty
        
        # Ensure minimum allocation to insurance (safety)
        min_insurance = {0: 0.10, 1: 0.05, 2: 0.02}  # Low risk needs more insurance
        if action[5] < min_insurance[self.risk_level]:
            reward -= 50
        
        # Ensure minimum allocation to savings (emergency fund)
        min_savings = {0: 0.15, 1: 0.10, 2: 0.05}
        if action[4] < min_savings[self.risk_level]:
            reward -= 50
        
        return reward


class PortfolioOptimizer:
    """RL-based portfolio optimizer using PPO"""
    
    def __init__(self):
        """Initialize optimizer"""
        self.model = None
        self.is_trained = False
    
    def train(self, initial_amount: float = 100000, risk_level: int = 1, timesteps: int = 10000):
        """
        Train PPO agent
        
        Args:
            initial_amount: Initial investment amount
            risk_level: Risk level (0: Low, 1: Medium, 2: High)
            timesteps: Number of training timesteps
        """
        # Create environment
        env = make_vec_env(
            lambda: PortfolioEnv(initial_amount, risk_level),
            n_envs=4
        )
        
        # Create PPO model
        self.model = PPO(
            "MlpPolicy",
            env,
            verbose=0,
            learning_rate=0.0003,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95
        )
        
        # Train
        print(f"🤖 Training RL agent for risk level {risk_level}...")
        self.model.learn(total_timesteps=timesteps)
        
        self.is_trained = True
        print("✅ RL agent trained!")
    
    def optimize_allocation(
        self,
        amount: float,
        risk_level: int,
        current_state: Dict = None
    ) -> Dict[str, float]:
        """
        Get optimal portfolio allocation
        
        Args:
            amount: Amount to allocate
            risk_level: Risk level (0: Low, 1: Medium, 2: High)
            current_state: Current market/portfolio state
        
        Returns:
            Dictionary with allocation percentages
        """
        if not self.is_trained or self.model is None:
            # Fallback to rule-based allocation
            return self._rule_based_allocation(amount, risk_level)
        
        # Create environment
        env = PortfolioEnv(amount, risk_level)
        obs, _ = env.reset()
        
        # Get action from trained agent
        action, _ = self.model.predict(obs, deterministic=True)
        
        # Normalize action
        action = action / (np.sum(action) + 1e-8)
        
        asset_names = ["SIP", "Mutual Funds", "Stocks", "FD", "Savings", "Insurance"]
        allocation = {name: round(float(pct * 100), 2) for name, pct in zip(asset_names, action)}
        
        return allocation
    
    def _rule_based_allocation(self, amount: float, risk_level: int) -> Dict[str, float]:
        """
        Rule-based allocation (fallback)
        
        Args:
            amount: Amount to allocate
            risk_level: Risk level
        
        Returns:
            Allocation dictionary
        """
        # Conservative allocation strategies for Indian market
        allocations = {
            0: {  # Low Risk
                "SIP": 30.0,
                "Mutual Funds": 20.0,
                "Stocks": 5.0,
                "FD": 20.0,
                "Savings": 15.0,
                "Insurance": 10.0
            },
            1: {  # Medium Risk
                "SIP": 35.0,
                "Mutual Funds": 25.0,
                "Stocks": 15.0,
                "FD": 10.0,
                "Savings": 10.0,
                "Insurance": 5.0
            },
            2: {  # High Risk
                "SIP": 30.0,
                "Mutual Funds": 25.0,
                "Stocks": 30.0,
                "FD": 5.0,
                "Savings": 5.0,
                "Insurance": 5.0
            }
        }
        
        return allocations.get(risk_level, allocations[1])
    
    def save_model(self, path: str = "ml_models/saved_models/"):
        """Save trained model"""
        os.makedirs(path, exist_ok=True)
        
        if self.model:
            self.model.save(f"{path}ppo_portfolio")
            print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str = "ml_models/saved_models/"):
        """Load trained model"""
        try:
            self.model = PPO.load(f"{path}ppo_portfolio")
            self.is_trained = True
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")


def get_optimal_allocation(amount: float, risk_level: str) -> Dict:
    """
    Convenience function to get optimal portfolio allocation
    
    Args:
        amount: Investment amount
        risk_level: "Low", "Medium", or "High"
    
    Returns:
        Dictionary with allocation details
    """
    risk_map = {"Low": 0, "Medium": 1, "High": 2}
    risk_idx = risk_map.get(risk_level, 1)
    
    optimizer = PortfolioOptimizer()
    allocation = optimizer.optimize_allocation(amount, risk_idx)
    
    # Calculate amounts
    allocation_amounts = {
        asset: round(amount * (pct / 100), 2)
        for asset, pct in allocation.items()
    }
    
    return {
        "total_amount": amount,
        "risk_level": risk_level,
        "allocation_percentages": allocation,
        "allocation_amounts": allocation_amounts,
        "method": "rule_based"  # Change to "rl" when trained
    }
