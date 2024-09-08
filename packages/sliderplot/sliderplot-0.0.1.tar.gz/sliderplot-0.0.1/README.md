# sliderplot

Turn a function into an interactive plot with a single line of code.

<p align="center">
    <img src="https://github.com/ngripon/sliderplot/blob/main/demo.gif" width="520" alt="demo" />
</p>

``` python
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return x, y


    sliderplot(f, params_bounds=((0, 10), (0, 10 * np.pi), (0, 2 * np.pi)), show=True)
```
