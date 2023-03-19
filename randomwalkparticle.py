########  Animation of Diffusion of a particle  #########

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


box_size = 20 # size of the box
n_particles = 100 # number of particles inside box
v_max = 2 # maximum velocity of the particles
r_max = 0.2 # maximum radius of the particles
duration = 500 # duration of the animation
dt = 0.1 # step size


fig, ax = plt.subplots() # Initializing the figure and axes

ax.set_xlim([0, box_size])
ax.set_ylim([0, box_size])

circles = [plt.Circle((0, 0), r_max) for _ in range(n_particles)] # define the particles as circles

# Add the particles to the axes
for circle in circles:
    ax.add_artist(circle)

# Initialize the positions, velocities, and radii of the particles
positions = box_size * np.random.rand(n_particles, 2)
velocities = v_max * (2 * np.random.rand(n_particles, 2) - 1)
radii = r_max * np.random.rand(n_particles)

# Defining a function to simulate the motion and collisions of the particles
def animate(frame):
    global positions, velocities

    positions += velocities * dt #new position is old position times step size
 
    for i in range(n_particles): # for collisions with the walls of the box
        if positions[i][0] - radii[i] < 0:
            positions[i][0] = radii[i]
            velocities[i][0] = abs(velocities[i][0])
        elif positions[i][0] + radii[i] > box_size:
            positions[i][0] = box_size - radii[i]
            velocities[i][0] = -abs(velocities[i][0])
        if positions[i][1] - radii[i] < 0:
            positions[i][1] = radii[i]
            velocities[i][1] = abs(velocities[i][1])
        elif positions[i][1] + radii[i] > box_size:
            positions[i][1] = box_size - radii[i]
            velocities[i][1] = -abs(velocities[i][1])

    # Check for collisions between the particles
    for i in range(n_particles):
        for j in range(i+1, n_particles):
            distance = np.linalg.norm(positions[i] - positions[j])
            if distance < radii[i] + radii[j]:
                normal = (positions[i] - positions[j]) / distance
                tangent = np.array([-normal[1], normal[0]])
                v_i = np.dot(velocities[i], tangent) * tangent + np.dot(velocities[i], normal) * normal
                v_j = np.dot(velocities[j], tangent) * tangent + np.dot(velocities[j], normal) * normal
                velocities[i] = v_j
                velocities[j] = v_i

    # Update the positions of the circles
    for i in range(n_particles):
        if i == 0:  # Highlight the first particle
            circles[i].set_edgecolor('orange')
            circles[i].set_linewidth(2)
        else:
            circles[i].set_edgecolor('blue')
            circles[i].set_linewidth(1)
        circles[i].center = positions[i]

    return circles


# Create the animation
animation = animation.FuncAnimation(fig, animate, frames=duration, interval=50, blit=True)

# Show the animation
plt.show()

