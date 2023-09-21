---
title: "🚧WIP: Building an RL agent to play Snakes and Ladders🚧"
date: 2023-03-28T01:54:20+05:30
draft: true
---

## Goal
Build an RL-based agent that can beat humans in a modified version of the classic board game 'Snakes and Ladders'.

## Wait, isn't Snakes and Ladders entirely random? 
Yes. The original game is subject to the whims of the probability gods manifested as a dice. Clearly, the agent has no decisions to make in this version and it's as useless as me holding the torch while my dad fixes the cooler. So we tweaked the rules a bit.

### New Rules
1. **Eliminate the die roll:** Let the agent decide the number of places to move between 1-6 at each turn.
2. **Choice of taking the ladder:** If the agent reaches the bottom of a ladder, it can decide whether to take it or potentially wait and hang around for a bigger ladder coming up.

## Implementation

1. Create the `SNL` game environment in Python using Pygame
2. Create a `SNLGym` training environment by inheriting from the `gymnasium.Env` class. Implement the Gymnasium API methods by calling the respective methods in the `SNL` game env.
3. Algorithm: I will most likely choose Q-Learning or SARSA as they are computationally lighter and work well for environments with discrete "action space" and "observation space".
4. 
