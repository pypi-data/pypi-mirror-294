import enum

import matplotlib.pyplot as plt
import numpy as np

from sliderplot import sliderplot

SLIDER_HEIGHT = 0.05
BOTTOM_PADDING = (0.03, 0.1)


class _PlotMode(enum.Enum):
    LINE_X = 0
    LINE_XY = 1
    MULTI_LINE = 2
    MULTI_PLOT = 3


def _get_plot_mode(output_data) -> _PlotMode:
    plot_mode_map = {1: _PlotMode.LINE_X, 2: _PlotMode.LINE_XY, 3: _PlotMode.MULTI_LINE, 4: _PlotMode.MULTI_PLOT}
    depth = _compute_depth(output_data)
    if depth in plot_mode_map.keys():
        return plot_mode_map[depth]
    else:
        raise Exception("Failed to transform the output data of the function into plots. "
                        "Please look at the documentation for correct data formatting.")


def _compute_depth(data) -> int:
    # TODO: check depth of all elements
    depth = 0
    current_element = data
    while True:
        try:
            current_element = current_element[0]
            depth += 1
        except IndexError:
            break
    return depth


def _create_plot(outputs):
    lines = []
    plot_mode = _get_plot_mode(outputs)
    n_plots = len(outputs) if plot_mode is _PlotMode.MULTI_PLOT else 1
    fig, axs = plt.subplots(ncols=n_plots)
    if plot_mode is _PlotMode.MULTI_PLOT:  # axs is an array of Axes objects
        for ax, subplot_data in zip(axs, outputs):
            ax.grid()
            for x, y in subplot_data:
                line, = ax.plot(x, y, lw=2)
                lines.append(line)
    else:  # axs is an Axes object
        axs.grid()
        if plot_mode is _PlotMode.MULTI_LINE:
            for x, y in outputs:
                line, = axs.plot(x, y, lw=2)
                lines.append(line)
        elif plot_mode is _PlotMode.LINE_XY:
            line, = axs.plot(outputs[0], outputs[1], lw=2)
            lines.append(line)
        elif plot_mode is _PlotMode.LINE_X:
            x = np.arange(len(outputs))
            line, = axs.plot(x, outputs, lw=2)
            lines.append(line)
    return fig, axs, lines, plot_mode


def _get_lines(outputs, plot_mode: _PlotMode):
    if plot_mode is _PlotMode.MULTI_LINE:
        return outputs
    elif plot_mode is _PlotMode.LINE_XY:
        return ((outputs[0], outputs[1]),)
    elif plot_mode is _PlotMode.LINE_X:
        x = np.arange(len(outputs))
        return ((x, outputs),)
    elif plot_mode is _PlotMode.MULTI_PLOT:
        return np.concatenate((*outputs,))
    else:
        raise Exception("Invalid plot_mode argument.")


if __name__ == '__main__':
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return x, y


    fig, axs = sliderplot(f, params_bounds=((0, 10), (0, 10 * np.pi), (0, 2 * np.pi)))
