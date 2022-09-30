from matplotlib.animation import FuncAnimation
from flyby.visualizers.solar_system_plot import plot_body
from flyby.time_model.julian_day import datetime64_to_jd
from flyby.solar_system_model.relational_tree import RelationalTree
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

initial_time = np.datetime64("now")
t_jd = datetime64_to_jd(initial_time) + np.arange(0, 365, 1)
solar_system = RelationalTree.solar_system()

artist_lists = [[] for _ in range(len(t_jd))]

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

ax1.plot(0, 0, 'o', markersize=5,
         color=f"#{solar_system.root.color:X}")
ax2.plot(0, 0, 'o', markersize=5,
         color=f"#{solar_system.root.color:X}")

# Construct artist lists
with tqdm(total=len(t_jd), desc="Generating Animation Frames") as pbar:
    for i, jd in enumerate(t_jd):
        for j in range(8):
            artist_lists[i].extend(
                plot_body(solar_system.root.children[j],
                          jd, ax1, solar_system.root.mu, num_ellipse_samples=50))

            if j < 4:
                artist_lists[i].extend(
                    plot_body(solar_system.root.children[j],
                              jd, ax2, solar_system.root.mu, num_ellipse_samples=50))
        pbar.update(1)

ax1.set_title("Solar System")
ax1.set_axis_off()
ax1.set_aspect('equal')

ax2.set_title("Inner Solar System")
ax2.set_axis_off()
ax2.set_aspect('equal')

# Construct animation

for artist_list in artist_lists:
    for artist in artist_list:
        artist.set_visible(False)


def animate(i):
    for artist in artist_lists[i]:
        artist.set_visible(True)

    if i > 0:
        for artist in artist_lists[i-1]:
            artist.set_visible(False)

    return artist_lists[i]


animation = FuncAnimation(fig, animate, frames=len(
    t_jd) - 1, interval=10, blit=True)

plt.show()
