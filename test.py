import numpy as np
import matplotlib.pyplot as plt

# Generate input values from -10 to 10
x = np.linspace(-10, 10, 400)

# Calculate the tanh values
y = np.tanh(x)

# Plot the tanh function
plt.figure(figsize=(8, 4))
plt.plot(x, y, label='tanh(x)', color='blue')
plt.title('Funkcja tanh', fontsize=16)
plt.xlabel('x', fontsize=16)
plt.ylabel('tanh(x)', fontsize=16)



plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.tight_layout()
plt.show()
