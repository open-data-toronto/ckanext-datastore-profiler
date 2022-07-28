# Load base libaries
from distutils.errors import DistutilsTemplateError
from gc import callbacks
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


def plot_datasource_features(dict_features, lshow=True, dtype='numerics'):

    # Convert dict to DF
    df_features = pd.DataFrame.from_dict(dict_features, orient="index").reset_index()    
    df_features = df_features.fillna(0.0)

    # List of keys 
    list_features = list(df_features['index'])

    # Get info of a feature
    feature = list_features[0]

    # Filter Data
    df_feature = df_features[df_features['index'] == feature]

    # Create CDS using DataFrame
    source = ColumnDataSource(data=df_features)
    filtered_source = ColumnDataSource(data=df_feature)
    print('Before filter:\n', filtered_source.data)

    if (dtype == 'numerics'):
        # Display for null_count & all_unique
        table_columns_ncau = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['index','null_count', 'all_unique']]
        datatable_ncau = DataTable(source=filtered_source, columns=table_columns_ncau, width=500, height=100)

        # Display for m4 = min, median, mean, max
        table_columns_m4 = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['index','min','max','median','mean']]
        datatable_m4 = DataTable(source=filtered_source, columns=table_columns_m4, width=500, height=100)
    
    elif (dtype == 'datetimes'):
        # Display for null_count, min & max
        table_columns_ncmm = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['index','null_count', 'min', 'max']]
        datatable_ncmm = DataTable(source=filtered_source, columns=table_columns_ncmm, width=500, height=100)

        # Display Year Counts table
        list_year = list(filtered_source.data.get('year_count')[0].keys())
        list_year_counts = list(filtered_source.data.get('year_count')[0].values())
        source_yc = ColumnDataSource({'year': list_year, 'count':list_year_counts})
        table_columns_yc = [TableColumn(field="year", title="Year"), TableColumn(field="count", title="Count")]
        datatable_yc = DataTable(source=source_yc, columns=table_columns_yc, width=150, height=250)

        # Display Weekend Counts table
        list_wkd = list(filtered_source.data.get('weekday_count')[0].keys())
        list_wkd_counts = list(filtered_source.data.get('weekday_count')[0].values())
        source_wkd = ColumnDataSource({'weekday': list_wkd, 'count':list_wkd_counts})
        table_columns_wkd = [TableColumn(field="weekday", title="Weekday"), TableColumn(field="count", title="Count")]
        datatable_wkd = DataTable(source=source_wkd, columns=table_columns_wkd, width=150, height=250)

        # Display Hour Counts table
        list_hour = list(filtered_source.data.get('hour_count')[0].keys())
        list_hour_counts = list(filtered_source.data.get('hour_count')[0].values())
        source_hour = ColumnDataSource({'hour': list_year, 'count':list_year_counts})
        table_columns_hour = [TableColumn(field="hour", title="Hour"), TableColumn(field="count", title="Count")]
        datatable_hour = DataTable(source=source_hour, columns=table_columns_hour, width=150, height=250)

        a = input('Enter ....')

    # Select a Feature
    selected_feature = Select(title="Select a Feature:", value=feature, options=list_features)

    # JS callback code
    callback_code = """
        var filter_dict = {};
        var original_data = source_original.data;
        var feature = cb_obj.value;
        var feature_id = 0;
        console.log('Selected Feature:', cb_obj.value, feature );
        console.log('Original Data:', original_data)

        // Get index of the feature
        for (var key in original_data) {            
            for (var i = 0; i < original_data['index'].length; ++i) {
                if (original_data['index'][i] === feature) {
                    feature_id = i;
                    break;
                }
            }
        }

        // Get data w.r.t the feature_id
        for (var key in original_data) {            
            filter_dict[key] = [];
            filter_dict[key] = [original_data[key][feature_id]];
        }
        console.log(' Filter  dict:',filter_dict)

        source_filtered.data = filter_dict; 
        source_filtered.change.emit();
    """
    callback = CustomJS(args=dict(source_original=source, 
                                  source_filtered=filtered_source), 
                        code=callback_code)
    selected_feature.js_on_change('value', callback)

    print('After filtereed:\n', filtered_source.data)

    # # Output visual will be saved as below
    # output_file(f"html/mockup_numeric_feature={feature}.html")

    # Layout of numeric key 
    if (dtype == 'numerics'):
        layout_feature = column(datatable_ncau, datatable_m4)
    elif (dtype == 'datetimes'):
        layout_feature = column(datatable_ncmm, row(datatable_yc, datatable_wkd, datatable_hour))

    # Layout with select 
    layout_final = row(selected_feature, layout_feature)
    curdoc().add_root(layout_final)

    if (lshow): show(layout_final)


def plot_numeric_feature(dict_numeric, feature=None, lshow=True):
    
    # Get info of a feature
    dict_feature = dict_numeric.get(feature)

    # Convert dict to DataFrame
    df  = pd.DataFrame(dict_feature, index=dict_feature.keys()).head(1)

    # Save transposed DataFrame
    df_t = df.T.reset_index()
    df_t.columns = ['stats', 'values']
    
    # Create CDS using DataFrame
    source  = ColumnDataSource(data=df)
    print(source)

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

    return layout_numeric_feature


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


def plot_m4_dot(source, lshow=True):
    """ Plot Min, Median, Mean, Max as per Mockup"""

    print('inside:', source.data.keys())
    a = input('Etner someot')

    # create local list of keys and vals
    list_all_keys = list(source.data.keys())
    list_all_vals = [x[0] for x in list(source.data.values())]

    # list of indices of min, max, mean, median
    list_idx_m4 = [idx for idx in range(len(list_all_keys)) if list_all_keys[idx].startswith('m')]

    # Create custom lists for plotting
    factors = [list_all_keys[idx] for idx in list_idx_m4]
    x = [list_all_vals[idx] for idx in list_idx_m4]

    # Columns data source
    source_new = ColumnDataSource(data=dict(x=x, factors=factors, names=[str(val) for val in x]))
    print('source_new:', source_new.data)
    a = input('')

    # Range: min_x and max_x 
    min_x = min(x)-min(x)/2.
    max_x = max(x)*1.25

    # Figure
    p = figure(title="Dot Plot - Min, Median, Mean, Max", tools="", toolbar_location=None,
               y_range=factors, x_range=[min_x, max_x], width=500, height=250,)

    # p.segment(x0=0, factors, x, factors, line_width=2, line_color="green", source=source_new,)
    p.circle(x='x', y='factors', size=15, fill_color="orange", line_color="green", line_width=3, source=source_new,)

    # Add LabelSet
    labels = LabelSet(x='x', y='factors', text='names', x_offset=5, y_offset=5, source=source_new, render_mode='canvas')
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
