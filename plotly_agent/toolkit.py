from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import pandas as pd
import plotly.express as px

@tool
def create_plotly_chart(df, plotly_code):
    '''
    Tool to create a chart with Plotly

    Parameters:
    df: pd.DataFrame
    plotly_code: str

    Return:
    fig: plotly.graph_objs._figure.Figure

    **Example**
    ```python
    fig = create_plotly_chart(
        df = pd.DataFrame(df),
        plotly_code = 'fig = px.line(df, x="A", y="B")'
    )
    fig.show()
    ```
    '''
    plotly_dict = {"df": pd.DataFrame(df), "px": px}

    try:
        exec(plotly_code, globals(), plotly_dict)
        fig = plotly_dict.get("fig", None)

        if fig is None:
            raise ValueError("The Plotly code did not create a 'fig' chart. Check the code.")

        return fig

    except Exception as e:
        repaired_fig = repair_plotly_code(df, plotly_code, str(e))

        if repaired_fig is None:
            raise ValueError("Failed to repair Plotly code.")

        return repaired_fig

@tool
def repair_plotly_code(df, plotly_code, error_message):
    '''
    Tool to handle possible Plotly code errors

    Parameters:
    df: pd.DataFrame
    plotly_code: str
    error_message: str

    Return:
    fig: plotly.graph_objs._figure.Figure

    **Error Example**
    ```python
    fig = repair_plotly_code(
        df = pd.DataFrame(df),
        plotly_code = 'px.bar(df, x="A", y="C")',
        error_message = "AttributeError: Value of 'y' is not the name of a column in 'data_frame'"
    )
    fig.show()
    ```

    **Correction Example**
    ```python
    fig = repair_plotly_code(
        df = pd.DataFrame(df),
        plotly_code = 'px.bar(df, x=df["A"], y=["B"])',
    )
    fig.show()
    ```
    '''
    repair_dict = {"df": pd.DataFrame(df), "plotly_code": plotly_code, "error_message": error_message, "px": px}

    try:
        exec(plotly_code, globals(), repair_dict)
        fig = repair_dict.get("fig", None)

        if fig is None:
            raise ValueError("The repaired Plotly code did not create a 'fig' chart. Check the code.")

        return fig

    except Exception as e:
        print(f"Failed to repair Plotly code: {e}")
        return None

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a data visualization assistant using Plotly.
        GENERAL INSTRUCTIONS:
        Visualize the input text and try to formulate a visualization for it.
        Consider processing column names in the dataframe, \
        i.e., remove accents and any other details that might hinder \
        the creation of the chart (Example: Número -> Numero).
        Always use the tool [create_plotly_chart] to create your visualization with Plotly.
        Use the tool [repair_plotly_code] if there is an error during the execution of the code \
        created by the [create_plotly_chart] tool.
        The Final Response step should receive the python code of the created chart, do not call a tool in the final response.
        After many repair attempts, return an explanatory excuse as to why you couldn't generate the chart.

        STEP INSTRUCTIONS:
        Format -> step name: content
        You must execute following these steps:
        - Thought: Reasoning to understand the input text and what your next step should be;
        - Tool: Tool you will use;
        - Action: Result of the used tool code;
        - Final Response: Python code with libraries, df, ...

        CHART INSTRUCTIONS:
        Always give a title and **ALWAYS** use html tag to make it bold.
        Always display very large numbers in approximate format with 2 decimal places.
        Add annotations to the values on the x-axis.
        Always style the chart to make it interesting and easy to understand.
        If the variable is a percentage, show it with 2 decimal places and the '%' sign.
        Display date values in Day/Month/Year format.
        In a line chart, place a dot on the axes.
        Make sure all matrices or vectors you are using to create the chart have \
        the same size.
        If both the x and y axes are categorical variables, consider using a scatter plot.
        If one axis is a categorical variable and the other is a date, also consider using a scatter plot.
        Consider making a timeline only when the start date and end date are different.
        If it is interesting, extract as much information as possible from the original dataframe to \
        be filled in the tooltip.
        """),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)
