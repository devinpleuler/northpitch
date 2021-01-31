# NorthPitch

NorthPitch is a python soccer plotting library that sits on top of Matplotlib.

### Install:

```
pip install git+https://github.com/devinpleuler/northpitch.git
```

### Basic Example:
```python
from northpitch.pitch import Pitch

fig, ax = plt.subplots(figsize=(15,9))
ax.set_axis_off()

pitch = Pitch()
pitch.create_pitch(ax)

plt.ylim(pitch.ylim)
plt.xlim(pitch.xlim)

plt.show()
```
![alt text](./images/basic.png)


### Surface Example:

```python
from northpitch.pitch import draw_tracking_frame
from northpitch.pitch import overlay_surface

frame = tracking_frames[n]
surface = pitch_control_function(frame)

fig, ax = draw(frame, deltas=True, title="NorthPlotter example")
contours = overlay_surface(ax, surface)

plt.colorbar(contours, ax=ax)
plt.show()
```
> Note: Provide your own list of tracking frames, and pitch control function. Sorry.

![alt text](./images/pcf.png)
