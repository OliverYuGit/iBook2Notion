import book

from config import Config
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain import LLMChain

cfg = Config()

annotations = book.query()


def annotations_formatter() -> str:
    if annotations:
        temp = [str(anno) for anno in annotations]
        return '||'.join(temp)
    return ''


# text_splitter = CharacterTextSplitter(separator="||", chunk_size=2000, chunk_overlap=0)

# texts = text_splitter.split_text(annotations_formatter())

llm = OpenAI(temperature=0, openai_api_key=cfg.openai_api_key)

summarize_template = """
Please summarize the content in the original language, and cannot exceed 30 characters.

Content:
{content}

RESULT:
"""

summarize_chain = LLMChain(
    llm=llm, prompt=PromptTemplate.from_template(summarize_template))

zapier = ZapierNLAWrapper(zapier_nla_api_key=cfg.zapier_api_key)
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
tools = toolkit.get_tools()

summarize_tool = Tool(
    name="Summarize",
    func=summarize_chain.run,
    description="useful for when you need to summarize content")

tools.append(summarize_tool)

agent = initialize_agent(tools,
                         llm,
                         agent="zero-shot-react-description",
                         verbose=True)

# output = agent.run(f"Summarize the content as following in the original language.\nContent: {annotations[1]['content']}")

agent.run(f"""
There are multiple note data in the following, separated by ||. 
Each note data can be used to create a notion note item.
Please create notion note item for each of these note data one by one.

%NOTE DATA:
{annotations_formatter()}
""")