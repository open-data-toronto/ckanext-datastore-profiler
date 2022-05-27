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

# Bokeh - Widgets
from bokeh.models.widgets import Tabs, Panel


def plot_pie_chart(data_dict, column_name='index', lshow=True):
    """
        Returns a pie chart using data from dictionary and column_name ones wants to display index as.
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

    # Save transposed DataFrame
    df_t = df.T.reset_index()
    
    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df_t)

    # Customize Table columns 
    if (id == 'numerics'):
        columns = [TableColumn(field="index", title="Attribute Name"),
                    TableColumn(field="min", title="Minimum"),
                    TableColumn(field="max", title="Maxmimum"),
                    TableColumn(field="median", title="Median"),
                    TableColumn(field="mean", title="Mean"),
                    TableColumn(field="null_count", title="Null count"),
                    ]
    elif (id == 'datetimes'):
        columns = [TableColumn(field="index", title="Attribute Name"),
                    TableColumn(field="min", title="Minimum"),
                    TableColumn(field="max", title="Maxmimum"),
                    TableColumn(field="null_count", title="Null count"),
                    ]
    elif (id == 'strings_wc1'):
        columns = [TableColumn(field="index", title="Attribute Name"),
                    TableColumn(field="min_word_count", title="Min. Word Count"),
                    TableColumn(field="max_word_count", title="Max. Word Count"),
                    TableColumn(field="min_string_length", title="Min. String Length"),
                    TableColumn(field="max_string_length", title="Max. String Length"),
                    ]
    elif (id == 'strings_mc'):
        columns = [TableColumn(field="index", title="Attribute Name"),
                    TableColumn(field="mask_count", title="Mask Counts"),
                    ]
    elif (id == 'strings_sc'):
        columns = [TableColumn(field="index", title="Attribute Name"),
                    TableColumn(field="unique_count", title="String Counts"),
                    ]

    else:
        print(" >>> ERROR - Enter a valid id=['numerics','datetimes','strings']")
        return 


    # Finalize DataTable with dimensions
    data_table = DataTable(source=source, columns=columns, width=550, height=480)

    # Output visual will be saved as below
    output_file(f"html/datatable_datastore_{id}.html")

    # Return or show datatable
    if (lshow): show(data_table)

    return data_table


def display_tables_in_tabs(dict_numerics, dict_datetimes, dict_strings, lshow=True):

    # Build vizes to display
    viz1 = plot_data_table(dict_numerics, id='numerics', lshow=False)
    viz2 = plot_data_table(dict_datetimes, id='datetimes', lshow=False)
    viz3 = plot_data_table(dict_strings, id='strings_wc1', lshow=False)

    # Built tabs to display
    tab1 = Panel(child=viz1, title="Numerics Stats Table")
    tab2 = Panel(child=viz2, title="DateTime Stats Table")
    tab3 = Panel(child=viz3, title="Strings Stats Table")

    # Display all tabs as one viz
    tabs = Tabs(tabs=[ tab1, tab2, tab3])
    
    if(lshow): show(tabs)


def display_strings_tables_for_ckan(dict_strings, lshow=True):

    # Build vizes to display
    viz_wc1 = plot_data_table(dict_strings, id='strings_wc1', lshow=False)
    viz_mc  = plot_data_table(dict_strings, id='strings_mc', lshow=False)
    viz_sc  = plot_data_table(dict_strings, id='strings_sc', lshow=False)

    # Built tabs to display
    tab_wc = Panel(child=viz_wc1, title="Word Counts")
    tab_mc = Panel(child=viz_mc,  title="Mask Counts")
    tab_sc = Panel(child=viz_sc,  title="String Counts")

    # Display all tabs as one viz
    tabs = Tabs(tabs=[tab_wc, tab_mc, tab_sc])
    
    if(lshow): show(tabs)


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