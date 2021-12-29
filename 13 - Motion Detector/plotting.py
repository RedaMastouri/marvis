from motion import df        #运行ploting  会运行capture
from bokeh.plotting import figure,show,output_file
from bokeh.models import HoverTool,ColumnDataSource #引入hovertool
                                    #传入columndatasource

#1. Getting all the data from Times.csv in pandas dataframe structure
df['Start_string']=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df['End_string']=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)         #将df规范化——便于bokeh理解

#2. Set the size, title, responsiveness of the graph
p=figure(x_axis_type="datetime",height=100,width=500,sizing_mode="scale_both",title="Motion Graph")

#修改
p.yaxis.minor_tick_line_color=None      #
p.yaxis[0].ticker.desired_num_ticks=1

#3. This is cool! Turn on Hover effect!
hover = HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])         #@后面为columns名称
p.add_tools(hover)

#4. Set the color of infobar
q=p.quad(left='Start',right="End",bottom=0,top=1,color="green",source=cds)            #方框

#5. Save it as HTML file
output_file("Graph.html")
show(p)

