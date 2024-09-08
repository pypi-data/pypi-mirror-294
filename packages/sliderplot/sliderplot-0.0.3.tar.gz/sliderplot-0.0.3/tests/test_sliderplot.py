import pytest

from sliderplot import sliderplot
import numpy as np


def test_minimal_example():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return x, y

    sliderplot(f)