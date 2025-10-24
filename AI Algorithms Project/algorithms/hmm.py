"""
Hidden Markov Model (HMM) algorithm skeleton.

This module provides a class outline for a hidden Markov model.  
Fill in the algorithmic details for forward, Viterbi, and Baum-Welch methods as needed.
"""

import numpy as np
from typing import List, Sequence, Optional


class HiddenMarkovModel:
    """A simple hidden Markov model implementation."""

    def __init__(
        self,
        states: List[str],
        observations: List[str],
        transition_matrix: np.ndarray,
        emission_matrix: np.ndarray,
        initial_probs: np.ndarray,
    ) -> None:
        """
        Initialize the HMM with states, observations, and probability matrices.

        :param states: A list of hidden state labels.
        :param observations: A list of observation symbols.
        :param transition_matrix: A (N x N) matrix of state transition probabilities.
        :param emission_matrix: A (N x M) matrix of emission probabilities.
        :param initial_probs: A vector of initial state probabilities.
        """
        self.states = states
        self.observations = observations
        self.transition_matrix = transition_matrix
        self.emission_matrix = emission_matrix
        self.initial_probs = initial_probs

    def forward(self, sequence: Sequence[str]) -> float:
        """
        Compute the probability of an observation sequence using the forward algorithm.

        :param sequence: A sequence of observed symbols.
        :return: The likelihood of the observation sequence.
        """
        # TODO: Implement forward algorithm using dynamic programming
        pass

    def viterbi(self, sequence: Sequence[str]) -> List[str]:
        """
        Find the most likely sequence of hidden states for a given observation sequence.

        :param sequence: A sequence of observed symbols.
        :return: The most probable sequence of hidden states.
        """
        # TODO: Implement Viterbi algorithm to compute the best path
        pass

    def baum_welch(self, sequences: Sequence[Sequence[str]], max_iter: int = 100) -> None:
        """
        Train the HMM parameters using the Baum-Welch algorithm (EM).

        :param sequences: A list of observation sequences to train on.
        :param max_iter: Maximum number of iterations for the EM algorithm.
        """
        # TODO: Implement Baum-Welch algorithm for parameter estimation
        pass
