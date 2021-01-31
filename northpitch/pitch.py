import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np

_default_metric_dims = {
    'pen_length': 16.5, 'pen_width': 16.5 * 2 + 7.32,
    'six_length': 5.5, 'six_width': 5.5 * 2 + 7.32,
    'pk_length': 11, 'circle_rad': 9.15,
    'goal_size': 7.32
}

_default_dims = {
    'pen_length': 18, 'pen_width': 18 * 2 + 8,
    'six_length': 6, 'six_width': 6 * 2 + 8,
    'pk_length': 12, 'circle_rad': 10,
    'goal_size': 8
}

_pitch_cosmetics = {
    'linewidth': 1,
    'facecolor': (1, 1, 1, 1),
    'edgecolor': (0, 0, 0, 1)
}

_pass_cosmetics = {
    'length_includes_head': True,
    'head_width': 2,
    'head_length': 2,
    'width': 0.5,
    'facecolor': (0, 0, 1, 0.6),
    'edgecolor': (0, 0, 0, 0)
}

_point_cosmetics = {
    'linewidth': 1,
    'facecolor': (0, 0, 1, 0.6),
    'edgecolor': (0, 0, 0, 0),
    'radius': 1
}

_vector_cosmetics = {'length_includes_head': True,
                     'head_width': 1,
                     'head_length': 1,
                     'width': 0.1,
                     'facecolor': (0, 0, 0, 0.8),
                     'edgecolor': (0, 0, 0, 0),
                     'zorder': 4}


def get_dot_style(name, home_color, away_color,
                  ball_color, player_size, ball_size):

    dot_styles = {
        'simple': {
            "home": {'facecolor': home_color,
                     'edgecolor': 'white',
                     'linewidth': 0.8,
                     'radius': player_size,
                     'zorder': 5},
            "away": {'facecolor': away_color,
                     'edgecolor': 'white',
                     'linewidth': 0.8,
                     'radius': player_size,
                     'zorder': 5},
            "ball": {'facecolor': ball_color,
                     'edgecolor': 'black',
                     'radius': ball_size,
                     'zorder': 5}
        }
    }

    return dot_styles[name]


class Pitch(object):
    """
    This is a class for drawing a soccer pitch.
    Parameters
    ----------
    length : Length of field in yards. Default to 120.
    width : Width of field in yards. Default to 80.
    dimensions : Dimensions of interior lines in yards
            default = {'pen_length': 18, 'pen_width': 44,
                       'six_length': 6, 'six_width': 20,
                       'pk_length': 12, 'circle_rad': 10}
    vert : Plot field vertically. Default is False.
    scale : scaling factors for provider data.
            Opta is default at (100,100)
            For StatsBomb, use (120,80)
    padding : Padding for plot. Defaults to 5.
    Examples
    --------
    Basic Usage
    >>> from northpitch.pitch import Pitch
    >>> import matplotlib.pyplot as plot
    >>> fig, ax = plt.subplots()
    >>> pitch = Pitch()
    >>> pitch.create_pitch(ax)
    >>> plt.ylim(pitch.ylim)
    >>> plt.xlim(pitch.xlim)
    >>> plt.show()
    """

    def __init__(self,
                 length=120,
                 width=80,
                 title=None,
                 dimensions=_default_dims,
                 vert=False, scale=(100, 100),
                 padding=5):

        self.vert = vert
        self.length = length
        self.width = width
        self.x_scale = scale[0]
        self.y_scale = scale[1]
        self.title = title

        if self.vert:
            self.xlim = (-padding, self.width + padding)
            self.ylim = (-padding, self.length + padding)
        else:
            self.xlim = (-padding, self.length + padding)
            self.ylim = (-padding, self.width + padding)

        for k, v in dimensions.items():
            assert k in _default_dims.keys(), '{} not an attribute'.format(k)
            setattr(self, k, v)

    def __repr__(self):
        """
        Return string representation of Pitch object
        """
        return 'Pitch({}x{})'.format(self.length, self.width)

    def _pitch_components(self, cosmetics):

        rect, circ, arc = patches.Rectangle, patches.Circle, patches.Arc

        comps = {
            'border': (rect,
                       {'xy': (0, 0),
                        'width': self.length,
                        'height': self.width,
                        **cosmetics}),

            'left_circle': (circ,
                            {'xy': (self.pk_length,
                                    self.width/2),
                             'radius': self.circle_rad,
                             **cosmetics}),

            'right_circle': (circ,
                             {'xy': (self.length-self.pk_length,
                                     self.width/2),
                              'radius': self.circle_rad,
                              **cosmetics}),

            'left_penalty': (rect,
                             {'xy': (0, (self.width/2)-(self.pen_width/2)),
                              'width': self.pen_length,
                              'height': self.pen_width,
                              **cosmetics}),

            'right_penalty': (rect,
                              {'xy': (self.length,
                                      (self.width/2)-(self.pen_width/2)),
                               'width': -self.pen_length,
                               'height': self.pen_width,
                               **cosmetics}),

            'left_pk_dot': (circ,
                            {'xy': (self.pk_length,
                                    self.width/2),
                             'radius': 0.3,
                             'facecolor': cosmetics['edgecolor']}),

            'right_pk_dot': (circ,
                             {'xy': (self.length-self.pk_length,
                                     self.width/2),
                              'radius': 0.3,
                              'facecolor': cosmetics['edgecolor']}),

            'left_six': (rect,
                         {'xy': (0, (self.width/2)-(self.six_width/2)),
                          'width': self.six_length,
                          'height': self.six_width,
                          **cosmetics}),

            'right_six': (rect,
                          {'xy': (self.length,
                                  (self.width/2)-(self.six_width/2)),
                           'width': -self.six_length,
                           'height': self.six_width,
                           **cosmetics}),

            'half_circle': (circ,
                            {'xy': (self.length/2,
                                    self.width/2),
                             'radius': self.circle_rad,
                             **cosmetics}),

            'half_line': (rect,
                          {'xy': (self.length/2, 0),
                           'width': 0,
                           'height': self.width,
                           **cosmetics}),

            'half_dot': (circ,
                         {'xy': (self.length/2,
                                 self.width/2),
                          'radius': 0.3,
                          'facecolor': cosmetics['edgecolor']}),
            'post_left_top':
                (circ, {'xy': (0, self.width/2 + self.goal_size/2),
                        'radius': 0.3,
                        'facecolor': cosmetics['edgecolor']}),

            'post_left_bot':
                (circ, {'xy': (0, self.width/2 - self.goal_size/2),
                        'radius': 0.3,
                        'facecolor': cosmetics['edgecolor']}),

            'post_right_top':
                (circ, {'xy': (self.length, self.width/2 + self.goal_size/2),
                        'radius': 0.3,
                        'facecolor': cosmetics['edgecolor']}),

            'post_right_bot':
                (circ, {'xy': (self.length, self.width/2 - self.goal_size/2),
                        'radius': 0.3,
                        'facecolor': cosmetics['edgecolor']}),

            'bot_left_corner':
                (arc, {'xy': (0, 0), 'width': 1, 'height': 1,
                       'angle': 0, 'theta1': 0, 'theta2': 90,
                       'facecolor': cosmetics['edgecolor']}),

            'top_left_corner':
                (arc, {'xy': (0, self.width), 'width': 1, 'height': 1,
                       'angle': 0, 'theta1': -90, 'theta2': 0,
                       'facecolor': cosmetics['edgecolor']}),

            'top_right_corner':
                (arc, {'xy': (self.length, self.width),
                       'width': 1, 'height': 1,
                       'angle': 0, 'theta1': 180, 'theta2': -90,
                       'facecolor': cosmetics['edgecolor']}),

            'bot_right_corner':
                (arc, {'xy': (self.length, 0),
                       'width': 1, 'height': 1,
                       'angle': 0, 'theta1': 90, 'theta2': 180,
                       'facecolor': cosmetics['edgecolor']}),
        }

        if self.vert:
            for k, (shape, attrs) in comps.items():
                attrs['xy'] = (attrs['xy'][1], attrs['xy'][0])
                if shape == rect:
                    new_width = attrs['height']
                    attrs['height'] = attrs['width']
                    attrs['width'] = new_width

        return [s(**attrs) for k, (s, attrs) in comps.items()]

    def x_adj(self, x):
        """
        X Coordinate Adjuster for Spatial Data
        Parameters
        ----------
        x: spatial x coordinate from data provider
        Returns
        -------
        Float
            An adjusted x coordinate for field scale
        Examples
        --------
        >>> from northpitch.pitch import Pitch
        >>> pitch = Pitch(length=120, width=80)
        >>> opta_x, opta_y = 50, 50
        >>> pitch.x_adj(50)
        60
        """
        return x * (self.length / self.x_scale)

    def y_adj(self, y):
        """
        Y Coordinate Adjuster for Spatial Data
        Parameters
        ----------
        y: spatial y coordinate from data provider
        Returns
        -------
        Float
            An adjusted y coordinate for field scale
        Examples
        --------
        >>> from from northpitch.pitch import Pitch
        >>> pitch = Pitch(length=120, width=80)
        >>> opta_x, opta_y = 50, 50
        >>> pitch.y_adj(50)
        40
        """
        return y * (self.width / self.y_scale)

    def draw_lines(self, ax, passes, cosmetics=_pass_cosmetics, adjust=True):
        """
        Add Passes to Particular Axes
        Parameters
        ---------
        ax: matplotlib Axes object
        passes: list of pass coordinates
            eg. - >>> [(x, y, end_x, end_y)]
        cosmetics: dict of keyword arguments for patches.FancyArrow()
            default = {'length_includes_head': True,
                       'head_width': 2,
                       'head_length': 2,
                       'width': 0.5,
                       'facecolor': (0, 0, 1, 0.6),
                       'edgecolor': (0, 0, 0, 0)}
        Examples
        -------
        >>> from from northpitch.pitch import Pitch
        >>> import matplotlib.pyplot as plot
        >>> fig, ax = plt.subplots()
        >>> pitch = Pitch()
        >>> pitch.create_pitch(ax)
        >>> passes = [(60,60,25,25), (20,20, 50,50)]
        >>> pitch.draw_passes(ax, passes)
        >>> plt.ylim(pitch.ylim)
        >>> plt.xlim(pitch.xlim)
        >>> plt.show()
        """

        # TODO Accept Different Pass Vector Formats
        for x, y, end_x, end_y in passes:

            y = (self.y_scale-y) if self.vert else y
            end_y = (self.y_scale-end_y) if self.vert else end_y

            dx = end_x - x
            dy = end_y - y

            if adjust:
                attributes = {
                    'x': self.y_adj(y) if self.vert else self.x_adj(x),
                    'y': self.x_adj(x) if self.vert else self.y_adj(y),
                    'dx': self.y_adj(dy) if self.vert else self.x_adj(dx),
                    'dy': self.x_adj(dx) if self.vert else self.y_adj(dy)
                }
            else:
                attributes = {
                    'x': y if self.vert else x,
                    'y': x if self.vert else y,
                    'dx': dy if self.vert else dx,
                    'dy': dx if self.vert else dy
                }

            ax.add_patch(patches.FancyArrow(**attributes, **cosmetics))

    def draw_players(self, ax, points, labels):
        for i, label in enumerate(labels):
            x, y = points[i]
            ax.text(x, y, label,
                    fontsize=7, ha='center', va='center', color='white')

    def draw_points(self, ax, shots, cosmetics=_point_cosmetics, adjust=True):
        """
        Add Points to Particular Axes
        Parameters
        ---------
        ax: matplotlib Axes object
        passes: list of point coordinates
            eg. - >>> [(x, y)]
        cosmetics: dict of keyword arguments for patches.Circle()
            default = {'linewidth': 1,
                       'facecolor': (0, 0, 1, 0.6),
                       'edgecolor': (0, 0, 0, 0),
                       'radius': 1}
        Examples
        -------
        >>> from from northpitch.pitch import Pitch
        >>> import matplotlib.pyplot as plot
        >>> fig, ax = plt.subplots()
        >>> pitch = Pitch()
        >>> pitch.create_pitch(ax)
        >>> shots = [(90,50), (85,60)]
        >>> pitch.draw_points(ax, passes)
        >>> plt.ylim(pitch.ylim)
        >>> plt.xlim(pitch.xlim)
        >>> plt.show()
        """
        for x, y in shots:

            y = (self.y_scale-y) if self.vert else y

            if adjust:
                attributes = {
                    'xy': (self.y_adj(y) if self.vert else self.x_adj(x),
                           self.x_adj(x) if self.vert else self.y_adj(y))
                }
            else:
                attributes = {
                    'xy': (y if self.vert else x,
                           x if self.vert else y)
                }

            ax.add_patch(patches.Circle(**attributes, **cosmetics))

    def create_pitch(self, ax, cosmetics=_pitch_cosmetics):
        """
        Draw Pitch on Axes
        Parameters
        ---------
        ax: matplotlib Axes object
        cosmetics: dict of keyword arguments for pitch component patches.
            default = {'linewidth': 1,
                       'facecolor': (1, 1, 1, 1),
            'edgecolor': (0, 0, 0, 1)}
        Examples
        -------
        >>> from from northpitch.pitch import Pitch
        >>> import matplotlib.pyplot as plot
        >>> fig, ax = plt.subplots()
        >>> pitch = Pitch()
        >>> pitch.create_pitch(ax)
        >>> plt.ylim(pitch.ylim)
        >>> plt.xlim(pitch.xlim)
        >>> plt.show()
        """
        ax.set_aspect(1)

        if self.title is not None:
            ax.text(0, self.width+1, self.title, fontsize=12)

        for patch in self._pitch_components(cosmetics):
            ax.add_patch(patch)


def draw_tracking_frame(
    frame, ax=None, title=None,
    length=105, width=68, deltas=False, framerate=25,
    figsize=(12, 8), skirt=2,
    home_color='red', away_color='blue', ball_color='yellow',
    dot_style='simple', player_size=1, ball_size=0.5, hide_axis=True
):
    """
    Draw Tracking Frame
    Parameters
    ----------
    ax: matplotlib Axes object
    title: optional string to put in top left of plot
    length: field length
    width: field width
    deltas: include player velocity vectors
    framerate: framerate of tracking data (in hertz)
    figsize: matplotlib plot figure size
    skirt: units of padding on plot
    home_color: color of home team dots
    away_color: color of away team dots
    ball_color: color of ball
    dot_style: various dot styles for players
    player_size: radius of player dots
    ball_size: radius of ball dot
    hide_axis: hide matplotlib axis

    Returns
    -------
    fig: matplotlib Figure
    ax: matplotlib Axis

    Tracking Frame Structure
    ------------------------
    [{
        'homePlayers': [
            {'xyz':   [0.0, 0.0, 0.0],
             'delta': [0.0, 0.0, 0.0]}, # Deltas are Optional
             ... }],

        'awayPlayers': [ ... ],

        'ball': {'xyz': [0.0, 0.0, 0.0]}
    }]
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    if hide_axis:
        ax.set_axis_off()

    ax.set_aspect(1)

    pitch = Pitch(length, width,
                  title=title, dimensions=_default_metric_dims)
    pitch.create_pitch(ax)

    cosmetics = get_dot_style(dot_style, home_color, away_color, ball_color,
                              player_size, ball_size)

    adjust = [length/2, width/2]

    home_players = \
        np.array([x['xyz'][:2] for x in frame['homePlayers']]) + adjust
    away_players = \
        np.array([x['xyz'][:2] for x in frame['awayPlayers']]) + adjust
    ball = np.array([frame['ball']['xyz'][:2]]) + adjust

    pitch.draw_points(
        ax, home_players, cosmetics=cosmetics['home'], adjust=False)
    pitch.draw_points(
        ax, away_players, cosmetics=cosmetics['away'], adjust=False)
    pitch.draw_points(
        ax, ball, cosmetics=cosmetics['ball'], adjust=False)

    if deltas:
        home_deltas = \
            np.array(
                [p['delta'][:2] for p in frame['homePlayers']]) * framerate
        away_deltas = \
            np.array(
                [p['delta'][:2] for p in frame['awayPlayers']]) * framerate

        home_vectors = np.hstack(
            (home_players, home_players + home_deltas)).tolist()

        away_vectors = np.hstack(
            (away_players, away_players + away_deltas)).tolist()

        pitch.draw_lines(
            ax, home_vectors, cosmetics=_vector_cosmetics, adjust=False)
        pitch.draw_lines(
            ax, away_vectors, cosmetics=_vector_cosmetics, adjust=False)

    ax.set_xlim([-skirt, length+skirt])
    ax.set_ylim([-skirt, width+skirt])

    return fig, ax


def overlay_surface(ax, surface, length=105, width=68,
                    range=[-1, 1], levels=25,
                    alpha=0.4, cmap='bwr_r'):
    """
    Overlay Surface on matplotlib axis
    """
    assert len(surface.shape) == 2, "Surface wrong dimensions"
    x_bins, y_bins = surface.shape

    xx = np.linspace(0, length, x_bins)
    yy = np.linspace(0, width, y_bins)
    z = np.rot90(np.flip(surface, 1), 1)

    return ax.contourf(
        xx, yy, z,
        zorder=2,
        levels=np.linspace(range[0], range[1], levels),
        alpha=alpha,
        antialiased=True,
        cmap=cmap, vmin=range[0], vmax=range[1])
