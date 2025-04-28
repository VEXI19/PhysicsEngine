import numpy as np
import matplotlib.pyplot as plt

# create a function that fakes the reward sum function and draws it. make it look like a logarithmic function

def generate_log_rewards(num_episodes, base_reward=100, noise_factor=0.08, growth_rate=0.0001, max_reward=15):

    """
    Generate a fake reward sum function with rapid growth at the beginning and gradual leveling off.

    Args:
    - num_episodes (int): Number of episodes to simulate.
    - base_reward (float): Base value for the reward (average reward per episode).
    - noise_factor (float): Standard deviation of the random noise added to rewards.
    - growth_rate (float): Controls how fast the reward curve flattens over time.
    - max_reward (float): Maximum reward that the system can reach, used to flatten the curve.

    Returns:
    - episodes (numpy array): Array of episode numbers.
    - rewards (numpy array): Array of cumulative rewards.
    """
    # Generate a rapidly increasing function with a flattening curve
    episodes_range = np.arange(1, num_episodes + 1)

    # Sigmoid-like growth to simulate rapid increase followed by flattening
    raw_rewards = base_reward * np.log(episodes_range + 1) * growth_rate
    cumulative_rewards = np.cumsum(raw_rewards)

    # Normalize the cumulative rewards to stay within a maximum limit
    cumulative_rewards = np.minimum(cumulative_rewards, max_reward)

    # Add some random noise to make the curve more natural
    noisy_rewards = cumulative_rewards + np.random.normal(0, noise_factor, num_episodes)

    # Ensure the cumulative sum doesn't dip below zero
    noisy_rewards = np.maximum(noisy_rewards, 0)

    episodes = np.arange(1, num_episodes + 1)

    return episodes, noisy_rewards

# Example usage:
num_episodes = 800
episodes, cumulative_rewards = generate_log_rewards(num_episodes)
# Introduce a plateau after 300 episodes
plateau_episode = 300
# cumulative_rewards[plateau_episode:] = cumulative_rewards[plateau_episode - 1]  # Maintain the plateau
# Plotting the results
cumulative_rewards -= 16.2




# Plot the cumulative reward
plt.figure(figsize=(10, 6))
plt.plot(cumulative_rewards, label="Suma nagród")
plt.xlabel('Epizod', fontsize=20)
plt.ylabel('Suma nagród', fontsize=20)
plt.title('Suma nagród w czasie', fontsize=16)
plt.legend()
plt.grid(True)
# bigger font
plt.xticks(fontsize=14)
plt.show()
