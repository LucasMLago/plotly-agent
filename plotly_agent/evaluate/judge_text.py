# plotly_agent/evaluate/judge.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

def judge(text: str, openai_api_key: str, info: str = '') -> bool:
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name='gpt-4o-mini',
        temperature=0.0
    )

    system_prompt_job_raw = '''
    Given a text, you must judge whether a chart is needed to visualize its content or not. \
    Your answer should be '0' when no chart is needed and '1' when a chart is needed.
    '''

    system_prompt_job = system_prompt_job_raw + info if info else system_prompt_job_raw

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_job),
            ("human", "{prompt}")
        ]
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"prompt": text})
    final_response = bool(int(response))

    return final_response
