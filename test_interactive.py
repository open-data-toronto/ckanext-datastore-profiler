from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

x = [x*0.005 for x in range(0, 200)]
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

plot1 = Figure(plot_width=400, plot_height=400)
plot1.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback_code = """
    var data = source.data;
    var f = cb_obj.value
    console.log("callback activated!");
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = Math.pow(x[i], f)
    }
    source.change.emit();
"""
callback = CustomJS(args=dict(source=source), code=callback_code)

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
slider.js_on_change('value', callback)

print(slider.js_property_callbacks)
layout = column(slider, plot1)

show(layout)