import inspect
from inspect import signature
from typing import Callable

from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

from sliderplot.sliderplot import _create_plot, BOTTOM_PADDING, SLIDER_HEIGHT, _get_lines


def sliderplot(f: Callable, params_bounds=(), show: bool = True):
    """
    Create an interactive plot with sliders to explore the outputs of the function f for different inputs.
    :param f: Function to explore.
    :param params_bounds: Sequence of (val_min, val_max) bounds for each parameter of the function f.
    :param show: If True, show the plot.
    :return: fig and axs (Axes object if there is one subplot, and list of Axes if there are multiple subplots).
    """
    # Get init parameters
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]
    outputs = f(*init_params)

    # Create plot
    fig, axs, lines, plot_mode = _create_plot(outputs)
    # Adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=sum(BOTTOM_PADDING) + len(params) * SLIDER_HEIGHT)

    # Create sliders
    sliders = []
    for i, param in enumerate(params.keys()):
        slider_ax = fig.add_axes((0.15, BOTTOM_PADDING[0] + SLIDER_HEIGHT * (len(params) - 1 - i), 0.6, 0.03))
        if i < len(params_bounds):
            val_min, val_max = params_bounds[i]
        else:
            val_min, val_max = 0, 20
        slider = Slider(
            ax=slider_ax,
            label=param,
            valmin=val_min,
            valmax=val_max,
            valinit=init_params[i],
        )
        sliders.append(slider)

    # The function to be called anytime a slider's value changes
    def update(_):
        try:
            outputs = f(*(slider.val for slider in sliders))
        except ZeroDivisionError:
            return

        for line, (x, y) in zip(lines, _get_lines(outputs, plot_mode)):
            line.set_data(x, y)
        fig.canvas.draw_idle()
        if hasattr(axs, "__len__"):
            [ax.relim() for ax in axs]
            [ax.autoscale_view(True, True, True) for ax in axs]
        else:
            axs.relim()
            axs.autoscale_view(True, True, True)

    # Register the update function with each slider
    [slider.on_changed(update) for slider in sliders]

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    reset_ax = fig.add_axes((0.85, BOTTOM_PADDING[0] + (len(params) - 1) * SLIDER_HEIGHT, 0.1, 0.04))
    button = Button(reset_ax, 'Reset', hovercolor='0.975')

    def reset(event):
        [slider.reset() for slider in sliders]

    button.on_clicked(reset)

    fig._sliderplot_button = button  # Prevent garbage collector from deleting button behavior

    if show:
        plt.show()
    return fig, axs
