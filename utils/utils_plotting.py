# Load base libaries
from distutils.errors import DistutilsTemplateError
from gc import callbacks
import pandas as pd
import numpy as np

# Bokeh - io, plotting, and layout
from bokeh.io import output_file, show, curdoc, save
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
    """Returns interactive html using bokeh     
    """
    # Debugger flag (internal use)
    ldebug = False

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
    if (ldebug): print('Before filter:\n', filtered_source.data)

    if (dtype == 'numerics'):
        # Display for null_count & all_unique
        table_columns_ncau = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['index','null_count', 'all_unique']]
        datatable_ncau = DataTable(source=filtered_source, columns=table_columns_ncau, width=500, height=100)

        # Display for m4 = min, median, mean, max
        table_columns_m4 = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['min','max','median','mean']]
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

    elif (dtype == 'strings'):

        # NOT IMPLEMENTED YET 
        print('NOT IMPLEMENTEDD YET')
        return 
        # # Display for null_count, min & max
        # table_columns_ncmm = [TableColumn(field=col, title=col.replace('_'," ")) for col in list(df_features.columns) if col in ['index','null_count', 'min', 'max']]
        # datatable_ncmm = DataTable(source=filtered_source, columns=table_columns_ncmm, width=500, height=100)

        # # Display Year Counts table
        # list_year = list(filtered_source.data.get('year_count')[0].keys())
        # list_year_counts = list(filtered_source.data.get('year_count')[0].values())
        # source_yc = ColumnDataSource({'year': list_year, 'count':list_year_counts})
        # table_columns_yc = [TableColumn(field="year", title="Year"), TableColumn(field="count", title="Count")]
        # datatable_yc = DataTable(source=source_yc, columns=table_columns_yc, width=150, height=250)

        # # Display Weekend Counts table
        # list_wkd = list(filtered_source.data.get('weekday_count')[0].keys())
        # list_wkd_counts = list(filtered_source.data.get('weekday_count')[0].values())
        # source_wkd = ColumnDataSource({'weekday': list_wkd, 'count':list_wkd_counts})
        # table_columns_wkd = [TableColumn(field="weekday", title="Weekday"), TableColumn(field="count", title="Count")]
        # datatable_wkd = DataTable(source=source_wkd, columns=table_columns_wkd, width=150, height=250)

        # # Display Hour Counts table
        # list_hour = list(filtered_source.data.get('hour_count')[0].keys())
        # list_hour_counts = list(filtered_source.data.get('hour_count')[0].values())
        # source_hour = ColumnDataSource({'hour': list_year, 'count':list_year_counts})
        # table_columns_hour = [TableColumn(field="hour", title="Hour"), TableColumn(field="count", title="Count")]
        # datatable_hour = DataTable(source=source_hour, columns=table_columns_hour, width=150, height=250)


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

    if (ldebug): print('After filtereed:\n', filtered_source.data)

    # Layout of numeric key 
    if (dtype == 'numerics'):
        layout_feature = column(datatable_ncau, datatable_m4)
    elif (dtype == 'datetimes'):
        layout_feature = column(datatable_ncmm, row(datatable_yc, datatable_wkd, datatable_hour))

    # Layout with select 
    layout_final = row(selected_feature, layout_feature)
    curdoc().add_root(layout_final)

    if (lshow): 
        show(layout_final)
    else:
        # Output visual will be saved as below
        print(f">> HTML output is saved: html/mockup_datasourceid_{dtype}.html")
        output_file(f"html/mockup_datasourceid_{dtype}.html")
        save(layout_final)
