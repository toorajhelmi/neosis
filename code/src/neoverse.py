"""NeoVerse: The environment in which Neos operate."""

from typing import Optional
from abc import ABC, abstractmethod
import random


class NeoVerse(ABC):
    """Abstract base class for NeoVerse environments."""
    
    @abstractmethod
    def get_input(self, t: int) -> int:
        """
        Get the perceptual input at time t.
        
        Args:
            t: Current time tick
            
        Returns:
            Binary input bit (0 or 1)
        """
        pass
    
    @abstractmethod
    def compute_reward(self, prediction: int, actual: int, num_nodes: int = 1) -> int:
        """
        Compute reward (Spark) based on prediction accuracy.
        
        Args:
            prediction: Neo's prediction y_t
            actual: Actual next input u_{t+1}
            num_nodes: Number of nodes in the Neo (Spark equals num_nodes for correct prediction)
            
        Returns:
            Reward in Nex (num_nodes if correct, 0 if incorrect)
        """
        pass


class RandomNeoVerse(NeoVerse):
    """Random NeoVerse: inputs are sampled independently from Bernoulli(0.5)."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize random NeoVerse with optional seed."""
        if seed is not None:
            random.seed(seed)
    
    def get_input(self, t: int) -> int:
        """Get random input."""
        return random.randint(0, 1)
    
    def compute_reward(self, prediction: int, actual: int, num_nodes: int = 1) -> int:
        """Reward is num_nodes if prediction matches actual, 0 otherwise."""
        return num_nodes if prediction == actual else 0


class AlternatingNeoVerse(NeoVerse):
    """Alternating NeoVerse: pattern 01010101..."""
    
    def get_input(self, t: int) -> int:
        """Get alternating input."""
        return t % 2
    
    def compute_reward(self, prediction: int, actual: int, num_nodes: int = 1) -> int:
        """Reward is num_nodes if prediction matches actual, 0 otherwise."""
        return num_nodes if prediction == actual else 0


class BlockPatternNeoVerse(NeoVerse):
    """Block pattern NeoVerse: pattern 00110011..."""
    
    def get_input(self, t: int) -> int:
        """Get block pattern input."""
        return (t // 2) % 2
    
    def compute_reward(self, prediction: int, actual: int, num_nodes: int = 1) -> int:
        """Reward is num_nodes if prediction matches actual, 0 otherwise."""
        return num_nodes if prediction == actual else 0

