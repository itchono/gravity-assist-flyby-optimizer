from matplotlib.animation import FuncAnimation
from flyby.visualizers.solar_system_plot import plot_body
from flyby.time_model.julian_day import datetime64_to_jd, jd_to_datetime64
from flyby.solar_system_model.relational_tree import RelationalTree
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from matplotlib.patches import Rectangle

initial_time = np.datetime64("now")
t_jd = datetime64_to_jd(initial_time) + np.arange(0, 365, 1)
solar_system = RelationalTree.solar_system()

artist_lists = [[] for _ in range(len(t_jd))]

plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

ax1.plot(0, 0, 'o', markersize=5,
         color=f"#{solar_system.root.color:X}")
ax2.plot(0, 0, 'o', markersize=20,
         color=f"#{solar_system.root.color:X}")

# Construct artist lists
with tqdm(total=len(t_jd), desc="Generating Animation Frames", unit="d") as pbar:
    for i, jd in enumerate(t_jd):
        for j in range(8):
            artist_lists[i].extend(
                plot_body(solar_system.root.children[j],
                          jd, ax1, solar_system.root.mu, num_ellipse_samples=50))

            if j < 4:
                artist_lists[i].extend(
                    plot_body(solar_system.root.children[j],
                              jd, ax2, solar_system.root.mu, num_ellipse_samples=50,
                              markersize=10))
        pbar.update(1)

# place title inside the axes so it can blit
title_1 = ax1.set_title(f"Solar System at {initial_time}", y=0.9, x=0.5)
title_2 = ax2.set_title(f"Inner Solar System at {initial_time}", y=0.9, x=0.5)

AU = 149597870.7 * 1e3
inner_sys_bounding_box = Rectangle((-2*AU, -2*AU), 4*AU, 4*AU, fill=False, color='white')
ax1.add_patch(inner_sys_bounding_box)


ax1.set_axis_off()
ax1.set_aspect('equal')
#ax2.set_axis_off()
ax2.get_xaxis().set_ticks([])
ax2.get_yaxis().set_ticks([])
ax2.set_aspect('equal')

fig.suptitle("Solar System Animation, Barycentric Ecliptic Frame", fontsize=16)
fig.tight_layout()

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

    current_time = np.datetime_as_string(jd_to_datetime64(t_jd[i]), unit="D")

    title_1.set_text(f"Solar System at {current_time}")
    title_2.set_text(f"Inner Solar System at {current_time}")

    return artist_lists[i] + [title_1, title_2]


animation = FuncAnimation(fig, animate, frames=len(
    t_jd) - 1, interval=10, blit=True)

plt.show()
