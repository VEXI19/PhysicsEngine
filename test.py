import matplotlib.pyplot as plt
import numpy as np
#
# # Przykładowe dane - zamień na swoje
# episodes = np.arange(0, 1000)  # numery epizodów
# rewards = np.random.normal(loc=200, scale=30, size=1000).cumsum() / (np.arange(1, 1001))  # symulowana średnia nagroda
#
# # Wykres
# plt.figure(figsize=(10,6))
# plt.plot(episodes, rewards, label='Średnia nagroda')
# plt.xlabel('Epizody')
# plt.ylabel('Nagroda')
# plt.title('Postęp uczenia - Krzywa nagrody PPO')
# plt.legend()
# plt.grid(True)
# plt.show()

# Przykładowe dane
# time = np.linspace(0, 20, 1000)  # 0 do 20 sekund, 1000 punktów
# deviation = np.sin(time) * 5 + np.random.normal(0, 0.5, size=1000)  # symulowane odchylenie w stopniach
#
# # Wykres
# plt.figure(figsize=(10,6))
# plt.plot(time, deviation, label='Kąt odchylenia')
# plt.xlabel('Czas [s]')
# plt.ylabel('Odchylenie od pionu [°]')
# plt.title('Stabilność lotu rakiety - Odchylenie w czasie')
# plt.legend()
# plt.grid(True)
# plt.show()
import numpy as np
import matplotlib.pyplot as plt


def generate_log_rewards(num_episodes, base_reward=100, noise_factor=10, growth_rate=0.05, max_reward=5000):
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
num_episodes = 1000
episodes, cumulative_rewards = generate_log_rewards(num_episodes)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(episodes, cumulative_rewards, label='Cumulative Rewards')
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward')
plt.title('Logarithmic Reward Sum Over Episodes (Flattening Growth)')
plt.legend()
plt.grid(True)
plt.show()


