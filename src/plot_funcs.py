import plotly.graph_objects as go
import json
from collections import OrderedDict
import os
data_path = os.path.join(os.getcwd(),os.path.dirname(__file__)) + '/../data/'

##with open('../data/MasterData.txt') as f:
with open(data_path + 'MasterData.txt') as f:
    mdata = json.load(f,  object_pairs_hook=OrderedDict)

##with open('../data/riket.txt') as f:
with open(data_path + 'riket.txt') as f:
    riket_data = json.load(f)

##with open('../data/sekom.json') as f:
with open(data_path + 'sekom.json') as f:
    sekom_data = json.load(f)

key_to_desc = {
        "N15419": "Kunskapskrav uppnått, procent",
        "N15505": "Meritvärde",
        "N15436": "Behörighet, yrkesprogram, procent",
        "U15461": "Elever i år 9 som är behöriga till yrkespr. avvikelse från modellberäknat värde kommunala skolor, procentenheter",
        "N15485": "Elever i åk 6 med lägst betyget E i matematik, kommunala skolor, andel (%)",
        "N15488": "Elever i åk 6 med lägst betyget E i svenska, kommunala skolor, andel (%)",
        "N15574": "Elever i år 9 som fått ett högre betyg än provbetyg för ämnesprov i engelska, kommunala skolor, andel (%)",
        "N15573": "Elever i år 9 som fått ett lägre betyg än provbetyg för ämnesprov i engelska, kommunala skolor, andel (%)",
        "N15572": "Elever i år 9 som fått ett högre betyg än provbetyg för ämnesprov i matematik, kommunala skolor, andel (%)",
        "N15571": "Elever i år 9 som fått ett lägre betyg än provbetyg för ämnesprov i matematik, kommunala skolor, andel (%)",
        "N15570": "Elever i år 9 som fått ett högre betyg än provbetyg för ämnesprov i svenska, kommunala skolor, andel (%)",
        "N15569": "Elever i år 9 som fått ett lägre betyg än provbetyg för ämnesprov i svenska, kommunala skolor, andel (%)",
        "N15814": "Lärare (heltidstjänster) med lärarlegitimation och behörighet i minst ett ämne i grundskola åk 1-9, kommunala skolor, andel (%)",
        "N15034": "Elever/lärare (årsarbetare) i kommunal grundskola åk 1-9, lägeskommun, antal",
        "N15008": "Kostnad för kommunal grundskola åk 1-9, kr/elev",
        "N15902": "Nyinvandrade och elever med okänd bakgrund i kommunal grundskola åk. 1-9, andel (%)",
        "N15823": "Nyinvandrade och elever med okänd bakgrund i år 9, kommunala skolor, andel (%)",
        "N15820": "Elever vars föräldrar har eftergymnasial utbildning, åk 1-9 i kommunal grundskola, lägeskommun, andel (%)"
}

desc_to_key = {v:k for k,v in key_to_desc.items()}


class plot:

    def __init__(self):
        self._fig = go.Figure()

    def clear(self):
        """
        Reset the current canvas.
        """
        self._fig = go.Figure()

    def show(self, CONFIG = {}):
        """
        Display the canvas.
        """
        self._fig.show(config=CONFIG)

    def plot_line(self,x_0,y_0,x_1,y_1,col="black",line_width=1,line_type="solid"):
        """
        Draw a line on the canvas.

        Arguments:
        (x_0,y_0)  -- Starting point
        (x_1,y_1)  -- End_point
        col        -- Colour
        line_width -- Width
        line_type  -- Type
        """
        self._fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=x_0,
                y0=y_0,
                x1=x_1,
                y1=y_1,
                line=dict(
                    color=col,
                    width=line_width,
                    dash=line_type
                    )
                )
            )



    def add_def(self,Diagram,RikeAvg):
        """
        Add a box with text in

        Arguments:
        RikeAvg --National avgrage.
        """
        if Diagram==True:
            self._fig.update_layout(
                    annotations=[
                        go.layout.Annotation(
                            text = 'Den sträckade linjen visar<br>rikets medel: '+str(RikeAvg)+' procent',
                            align='left',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.05,
                            y=0.95,
                            bordercolor='black',
                            borderwidth=1,
                            bgcolor = 'white'
                        )
                    ]
                )
        else: 
            self._fig.update_layout(
                    annotations=[
                        go.layout.Annotation(
                            text = "Flickor har högre resultat än pojkar",
                            align='left',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.04,
                            y=1.00,
                            font=dict(family="Open Sans, sans-serif",size=12,color="black")
                          
                        ),  go.layout.Annotation(
                            text = "Pojkar har högre resultat än flickor",
                            align='left',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=1.00,
                            y=0.025,
                            font=dict(family="Open Sans, sans-serif",size=12,color="black")
                            
                        )
                    ]
                ) 






    def add_scatter(self, data_x, data_y, data_text, colors, xlabel, ylabel):
        """
        Add a scatter plot to the canvas.

        Arguments:
        data_x    -- Data plotted against the x-axis.
        data_y    -- Data plotted against the y-axis.
        data_text -- Information displayed on hover.
        colors      -- Decides the colour of each data point.
        xlabel    -- Information displayed on hover.
        ylabel    -- Information displayed on hover.
        """

        self._fig.add_trace(go.Scatter(
            x=data_x,
            y=data_y,
            customdata=list(zip(list(map(round,data_y)),list(map(round,data_x)))),
            hovertemplate = '<b>%{text}</b><br><br>'+
            '{}'.format(ylabel) + ': <b>%{customdata[0]}</b><br>'+
            '{}'.format(xlabel)+': <b>%{customdata[1]}</b><br><extra></extra>',
            hoverlabel = dict(
                bgcolor = 'white'
            ),
            text=data_text,
            marker=dict(
                color=colors,
            ),
            showlegend=False))

        self._fig.update_traces(mode='markers', marker=dict(symbol='circle', size=8))


    def add_bar(self, data_x, data_y, colors, x_ticks = True, text="", show_legend = False, legend_name=""):
        """
        Add a bar plot to the canvas.

        Arguments:
        data_x    -- Data/labels plotted against the x-axis.
        data_y    -- Data plotted against the y-axis.
        colors    -- Decides the colour of each data point.
        xticks    -- Show x-ticks or not, default is True
        text      -- Text shown on hover-labels, default is ""
        show_legend --  Show legend or not, default is False
        legend_name --  Name of the bar trace shown in the legend, default is ""
        """
        data_y_rounded = list(map(round,(list(map(lambda x: x + 0.001, list(map(abs,data_y)))))))

        self._fig.add_trace(go.Bar(
            x=data_x,
            y=data_y,
            hoverinfo= 'none',
            customdata=data_y_rounded,       # Här skickar vi med en lista av absolutvärden, vilket blir de värden som visas vid hovring.
            hovertemplate = '<b>%{x}</b><br><br>'+
            text + '<b>%{customdata}</b><br>',
            hoverlabel = dict(
                bgcolor = 'white',
                namelength = 0),
            text = data_y_rounded,
            textfont = dict(color="white"),
            textposition='auto',
            name = legend_name,
            marker_color=colors,
            cliponaxis = False,
            showlegend=show_legend,
            textangle=0))


        self._fig.update_layout(barmode="relative",
                                xaxis = dict(showticklabels=x_ticks),
                                uniformtext_minsize=18, uniformtext_mode='hide') #Denna rad bestämmer hur små värdena får vara inuti stapeln innan de kapas bort.
                                                                                #Är de mindre än 20 punkter så visas de inte. Tar man bort "uniformtext_minsize" och "uniformtext_mode"
                                                                                #kommer siffrona alltid att visas, även om de blir oändligt små om stapeln är liten.

    def add_title(self, title, x_title = "", y_title = ""):
        """
        Add/change the title of the plot.

        Arguments:
        title    -- Title as string.
        x_title  -- Add a title to the x-axis.
        y_title  -- Add a title to the y-axis.
        """
        self._fig.update_layout(title_text = title,
                                xaxis_title = x_title,
                                yaxis_title = y_title)


    def format_layout(self, show_x_grid=False, show_y_grid=False):
        """
        Update the appearence of the canvas.

        Arguments:
        plot_title  -- Add a title to the plot.
        show_x_grid -- If True, display a vertical line on each x-axis tick.
        show_y_grid -- If True, display a horizontal line on each y-axis tick.

        """
        self._fig.update_layout(
            title=dict(
                y=0.9,
                x=0.5,
                xanchor='center',
                yanchor='top'),
            font=dict(
                family="Open Sans, sans-serif",
                size=18,
                color="#7f7f7f"),
            xaxis=dict(
                showgrid=show_x_grid,
                gridwidth=1,
                gridcolor='LightGrey',
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)',
                ),
            yaxis=dict(
                showgrid=show_y_grid,
                gridwidth=1,
                gridcolor='LightGrey',
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)',
                ),
            margin=dict(l=140, r=40, b=50, t=120),
            legend=dict(
                font_size=10,
                yanchor='middle',
                xanchor='right',
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='closest',
            )

    def show_zero_line(self):

        self._fig.update_layout(
            xaxis = dict(
                zerolinecolor='black',
                zerolinewidth=1),
            yaxis = dict(
                zerolinecolor='black',
                zerolinewidth=1)
        )

    def format_size(self, WIDTH, HEIGHT):
        """
        Change the dimensions of the canvas.
        """
        self._fig.update_layout(
            width=WIDTH,
            height=HEIGHT,
        )

    def format_x_axis(self, x_tick, x_limits):
        """
        Alter the scope of the x-axis.

        Arguments:
        x_tick   -- Change the frequency of the x-axis ticks.
        x_limits -- Tuple, containing the end_points of the displayed x-axis.
        """
        self._fig.update_layout(
            xaxis=dict(
                range=x_limits,
                dtick=x_tick,
            ),
        )

    def format_y_axis(self, y_tick, y_limits):
        """
        Alter the scope of the y-axis.

        Arguments:
        y_tick   -- Change the frequency of the y-axis ticks.
        y_limits -- Tuple, containing the end_points of the displayed y-axis.
        """
        self._fig.update_layout(
            yaxis=dict(
                range=y_limits,
                dtick=y_tick,
            ),
        )

    def edit_toolbar(self, filename, format, height=750,width=1050):
        """
        Edit the options of the toolbar at the top of the diagram canvas.

        Argument description:
        filename 	-- a string specifying the default name of the file that downloads when pressing the “save plot” icon.
        format 		-- one of “png”, “svg”, “jpeg”, “webp”. Specifies the file format of the file that downloads when pressing the “save plot” icon.
        height		-- the height of the download, in pixels. Default is 750px.
        width		-- the width of the download, in pixels. Default is 1050px.
        """
        return {
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': format,                     # png, svg, jpeg, webp
                'filename': filename,
                'height': height,
                'width': width,
                'scale': 1
            },
            #'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian','autoScale2d','zoom2d', 'pan2d','lasso2d','select2d']
        }

    def dotted_line(self,legend_text,x_0,y_0,x_1,y_1,col="black",line_width=1):
        self._fig.add_trace(go.Scatter(
                        x=[x_0,x_1], 
                        y=[y_0,y_1], 
                        name=legend_text,
                        line = dict(color=col, width=line_width, dash='dot'),
                        hoverinfo='skip',
                        xaxis="x2",
                        mode='lines'))
        self._fig.update_layout(legend = dict(font = dict(color="black", size = 12, family="Open Sans, sans-serif")),
                                xaxis2=dict(showticklabels=False, overlaying= 'x',showgrid=False))