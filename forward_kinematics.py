import numpy as np

def dh_transform(a, alpha, d, theta):
    """Compute the DH transformation matrix."""
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,              np.sin(alpha),                np.cos(alpha),                 d],
        [0,              0,                            0,                             1]
    ])

# Define the DH parameters for the Epson VT6 (example values)
dh_params = [
    (0, np.pi/2, 300, np.pi/4),   # Joint 1
    (200, 0, 0, -np.pi/6),        # Joint 2
    (150, 0, 0, np.pi/3),         # Joint 3
    (0, -np.pi/2, 200, np.pi/2),  # Joint 4
    (0, np.pi/2, 0, -np.pi/4),    # Joint 5
    (0, 0, 100, 0)                # Joint 6
]

# Compute the overall transformation matrix
T = np.eye(4)  # Start with the identity matrix
for params in dh_params:
    T = np.dot(T, dh_transform(*params))

# Extract position and orientation
position = T[:3, 3]  # X, Y, Z position
orientation = T[:3, :3]  # Rotation matrix

print("End-Effector Position (X, Y, Z):", position)
print("End-Effector Orientation (Rotation Matrix):\n", orientation)
