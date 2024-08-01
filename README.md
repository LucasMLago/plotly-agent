# plotly-agent

A library to create interactive charts with Plotly and Langchain through an data visualization agent.

# Installation

```bash
pip install plotly_agent
```

# Import

```bash
from plotly_agent import extract_python_code
from plotly_agent import create_plotly_agent
from plotly_agent.evaluate import judge
```

# Execution code

```bash
llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name='gpt-4o-mini',
            temperature=0.0
        )

# judge if a input deserve a data visualization
judgment = judge(text=prompt, llm=llm)

if judgment:
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            # gpt-4-turbo had a better perform than gpt-4o and gpt-4o-mini
            model_name='gpt-4-turbo',
            temperature=0.0
        )

        plotly_agent = create_plotly_agent(llm=llm, max_interations=8, verbose=True)
        plotly_response = plotly_agent.invoke({'input': prompt})
        
        # Get python code from llm reponse
        fig_code = extract_python_code(plotly_response['output'])
        fig_dict = {"fig": Figure}
        exec(fig_code, fig_dict)
        
        # Returns a plottable figure
        fig = fig_dict.get("fig", None)
```
