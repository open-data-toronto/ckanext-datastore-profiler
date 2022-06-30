from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource, DataTable, TableColumn, CustomJS, Select
from bokeh.io import show, output_file, output_notebook, reset_output
from bokeh.layouts import row, column, layout

import pandas as pd

raw_data = {'ORG': ['APPLE', 'ORANGE', 'MELON'],
        'APPROVED': [5, 10, 15],
        'CREATED': [1, 3, 5],
        'INPROCESS': [4,2,16]}

df = pd.DataFrame(raw_data)

# create CDS for source
src1 = ColumnDataSource(df)

# create cols
table_columns1 = [TableColumn(field = Ci, title = Ci) for Ci in df.columns]

# original data table
data_table1 = DataTable(source=src1, 
                   columns=table_columns1, width=400, height=280)

# create empty dataframe to hold variables based on selected ORG value
df2 = pd.DataFrame({'status':['APPROVED', 'CREATED', 'INPROCESS'],
               'count':[float('nan'), float('nan'), float('nan')]})

# create CDS for empty dataframe
src2 = ColumnDataSource(df2)

# create cols
table_columns2 = [TableColumn(field = Ci, title = Ci) for Ci in df2.columns] 

callback = CustomJS(args=dict(src1=src1, src2=src2), code='''
var count = ['APPROVED', 'CREATED', 'INPROCESS'];
if (cb_obj.value != 'Please choose...') {
    var org = src1.data['ORG'];
    var ind = org.indexOf(cb_obj.value);
    for (var i = 0; i < count.length; i++) {
        src2.data['count'][i] = src1.data[count[i]][ind];
    }
}
else {
    for (var i = 0; i < status.length; i++) {
        src2.data['status'][i] = undefined;
    }

}
src2.change.emit();
table_columns2.change.emit();
''')

options = ['Please choose...'] + list(src1.data['ORG'])
select = Select(title='Test', value=options[0], options=options)
select.js_on_change('value', callback)

show(column(select, data_table1))