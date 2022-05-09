# Load base libaries
import pandas as pd
import numpy as np

# Bokeh - io, plotting, and layout
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.layouts import gridplot

# Bokeh - palette
from bokeh.palettes import Category20c

# Bokeh - transofrmation and models
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn


def plot_pie_chart(data_dict, column_name='index', lshow=True):
    """
        Returns a pie chart using data from dictionary
    """
    # Convert dictionary into Pandas series
    data_series = pd.Series(data_dict).reset_index(name='value').rename(columns={'index': column_name})
    print(data_series)
    data_series['angle'] = data_series['value']/data_series['value'].sum() * 2*np.pi
    data_series['color'] = Category20c[len(data_dict)]

    # Initialize Figure
    p = figure(height=350, title="Pie Chart of Top"+str(len(data_dict))+' - '+str(column_name), 
                toolbar_location=None, 
                tools="hover", tooltips=[(column_name, "@{"+column_name+"}"), 
                                         ('count', "@{value}")], 
                x_range=(-0.5, 1.0))

    # Create piechart using Wedge option in bokeh
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=data_series)

    # Labels for the plot
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    if (lshow): show(p)

def plot_data_table(data_dict, id='1', lshow=True):
    """
        Returns DataTable from data dictionary
    """
    # Convert dict to DataFrame
    df  = pd.DataFrame(data_dict)

    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df.T.reset_index())

    # Customize Table columns 
    columns = [TableColumn(field="index", title="Attribute Name"),
                TableColumn(field="min", title="Minimum"),
                TableColumn(field="max", title="Maxmimum"),
                TableColumn(field="median", title="Median"),
                TableColumn(field="mean", title="Mean"),
                TableColumn(field="null_count", title="Null count"),
                ]

    # Finalize DataTable with dimensions
    data_table_numerics = DataTable(source=source, columns=columns, width=550, height=480)

    # Output visual will be saved as below
    output_file(f"html/datatable_datastore_{id}.html")

    # Return or show datatable
    if (lshow): show(data_table_numerics)


if __name__ == "__main__":

    data_dict = {
        'United States': 157,
        'United Kingdom': 93,
        'Japan': 89,
        'China': 63,
        'Germany': 44,
        'India': 42,
        'Italy': 40,
        'Australia': 35,
        'Brazil': 32,
        'France': 31,
        'Taiwan': 31,
        'Spain': 29
    }

    plot_pie_chart(data_dict, column_name='country', lshow=True)