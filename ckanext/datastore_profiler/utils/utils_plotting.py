# Load base libaries
import pandas as pd
import numpy as np

# Bokeh - io, plotting, and layout
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import gridplot, row, column, layout

# Bokeh - palette
from bokeh.palettes import Category20c

# Bokeh - transofrmation and models
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn, Label, LabelSet, CustomJS, Select

# Bokeh - Widgets
from bokeh.models.widgets import Tabs, Panel


def plot_numerics(dict_numeric, lshow=True):

    # List of keys 
    list_features = list(dict_numeric.keys())

    # Select a Feature
    select = Select(title="Select a Feature:", value=list_features[0], options=list_features)
    select.js_on_change("value", CustomJS(code="""
        console.log('select: value=' + this.value, this.toString())
    """))

    # Layout of numeric feature 
    #layout_result = plot_numeric_feature(dict_numeric, feature=select.value, lshow=False)

    # Layout with select 
    layout_final = column(select, plot_numeric_feature(dict_numeric, feature=select.value, lshow=False))

    if (lshow): show(layout_final)

    #return

def plot_numeric_feature(dict_numeric, feature='inspID', lshow=True):

    # Get info of a feature
    dict_feature = dict_numeric.get(feature)
    print(dict_feature)

    # Convert dict to DataFrame
    df  = pd.DataFrame(dict_feature, index=dict_feature.keys()).head(1)

    # Save transposed DataFrame
    df_t = df.T.reset_index()
    df_t.columns = ['stats', 'values']
    
    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df)

    # Display for null_count & all_unique
    rows_nulls_uniques = [TableColumn(field="null_count", title="Null Count"),
                          TableColumn(field="all_unique", title="All Unique"),]

    # Finalize DataTable with dimensions
    display_nulls_uniques = DataTable(source=source, columns=rows_nulls_uniques, width=500, height=50)

    # Create custom lists
    list_keys_m4 = [key for key, val in dict_feature.items() if key.startswith('m')]
    list_vals_m4 = [val for key, val in dict_feature.items() if key.startswith('m')]

    # Display for m4 = min, median, mean, max
    display_m4 = plot_m4_dot(list_keys_m4, list_vals_m4, lshow=False)

    # Output visual will be saved as below
    output_file(f"html/mockup_numeric_feature={feature}.html")

    # Layout of numeric key 
    layout_numeric_feature = column(display_nulls_uniques, display_m4)
    curdoc().add_root(layout_numeric_feature)

    # Return or show datatable
    if (lshow): show(layout_numeric_feature)

    #return layout_numeric_feature


def plot_timeseries_feature(dict_ts, feature='inspDate', lshow=True):

    # Get info of a feature
    dict_feature = dict_ts.get(feature)

    # Filter dict
    dict_3 = {key: val for key, val in dict_feature.items() if key in ['min','max','null_count']}
    dict_n3= {key: val for key, val in dict_feature.items() if key not in ['min','max','null_count']}

    # Create DataFrame = df_3 
    df_3  = pd.DataFrame(dict_3, index=dict_3.keys()).head(1)

    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df_3)

    # Display for null_count & all_unique
    min_max_nulls = [TableColumn(field="null_count", title="Null Count"),
                     TableColumn(field="min", title="Min Date"),
                     TableColumn(field="max", title="Max Date"),
                     ]

    # Finalize DataTable with dimensions
    display_min_max_nulls = DataTable(source=source, columns=min_max_nulls, width=750, height=50)

    # Create DataFrames = df_n3_*_counts
    df_n3    = pd.DataFrame(dict_n3)
    display_hour_count    = df_to_table(df_n3, 'hour_count', 'hour', 'counts')
    display_weekday_count = df_to_table(df_n3, 'weekday_count', 'weekday', 'counts')
    display_year_count    = df_to_table(df_n3, 'year_count', 'year', 'counts')

    # # Output visual will be saved as below
    output_file(f"html/mockup_timeseries_feature={feature}.html")

    # Layout of numeric key 
    layout_timeseries_feature = column(display_min_max_nulls, row(display_hour_count, display_weekday_count, display_year_count))
    curdoc().add_root(layout_timeseries_feature)

    # Return or show datatable
    if (lshow): show(layout_timeseries_feature)

    #return

def plot_string_feature(dict_string, feature='enfrID', lshow=True):

    # Get info of a feature
    dict_feature = dict_string.get(feature)

    # Create DF and Tables
    df_s3    = pd.DataFrame(dict_feature)
    display_mask_count    = df_to_table(df_s3, 'mask_count', 'mask', 'counts')
    display_unique_count  = df_to_table(df_s3, 'unique_count', 'string', 'counts')
    display_word_count    = df_to_table(df_s3, 'word_counts', 'word', 'counts')

    # Filter dict - min, max word counts, short, long strings 
    dict_4 = {key: val for key, val in dict_feature.items() if key not in ['mask_count', 'unique_count', 'word_counts']}
    print(dict_4)
    df_4   = pd.DataFrame(dict_4, index=dict_4.keys()).head(1).T.reset_index()
    df_4.columns = ['min_max','chars']

    # Create CDS using DataFrame
    source_4  = ColumnDataSource(data=df_4)

    # Display for null_count & all_unique
    min_max_chars = [TableColumn(field="min_max", title="Word/String"),
                     TableColumn(field="chars", title="counts (chars)"),
                     ]

    # Finalize DataTable with dimensions
    display_min_max_chars = DataTable(source=source_4, columns=min_max_chars, width=250, height=125)

    # Construct layouts
    layout_string_feature = row(column(display_min_max_chars, display_word_count), display_mask_count, display_unique_count)
    curdoc().add_root(layout_string_feature)

    # # Output visual will be saved as below
    output_file(f"html/mockup_string_feature={feature}.html")

    if(lshow): show(layout_string_feature)

    #return


def df_to_table(df0, feature_old, feature_new1, feature_new2):

    df = df0[[feature_old]].dropna().reset_index()
    df.columns = [feature_new1, feature_new2]

    # ---------------------------------------------------------------
    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df)

    # Display for null_count & all_unique
    table_rows = [TableColumn(field=feature_new1, title=feature_new1),
                            TableColumn(field=feature_new2, title=feature_new2),]

    # Finalize DataTable with dimensions
    display_table = DataTable(source=source, columns=table_rows, width=250, height=250)

    return display_table


def plot_m4_dot(factors, x, lshow=True):
    """ Plot Min, Median, Mean, Max as per Mockup"""

    # Columns data source
    source = ColumnDataSource(data=dict(x=x, factors=factors, names=[str(val) for val in x]))

    # Range: min_x and max_x 
    min_x = min(x)-min(x)/2.
    max_x = max(x)*1.25

    # Figure
    p = figure(title="Dot Plot - Min, Median, Mean, Max", tools="", toolbar_location=None,
               y_range=factors, x_range=[min_x, max_x], width=500, height=250,)

    p.segment(0, factors, x, factors, line_width=2, line_color="green", )
    p.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )

    # Add LabelSet
    labels = LabelSet(x='x', y='factors', text='names', x_offset=5, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)

    if (lshow): show(p)

    return p

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
