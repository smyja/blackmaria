import os

from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


from gpt_index import (GPTSimpleVectorIndex, PromptHelper,
                       )
from gpt_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from gpt_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL, DEFAULT_REFINE_PROMPT_TMPL
from gpt_index.output_parsers import GuardrailsOutputParser
from gpt_index.llm_predictor import StructuredLLMPredictor, LLMPredictor
from langchain.chat_models import ChatOpenAI
llm_predictor = StructuredLLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))
# llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-curie-001"))
from blackmaria.cray import BeautifulSoupWebReader

def night_crawler(url: str,spec,query):

    loader = BeautifulSoupWebReader()
    max_input_size = 4096
    # set number of output tokens
    num_output = 100
    # set maximum chunk overlap
    max_chunk_overlap = 20
    prompt_helper = PromptHelper( max_input_size,num_output, max_chunk_overlap)

    documents = loader.load_data(urls=[url])
    base_url = url
    parsed_url = urlparse(base_url)
    filename = parsed_url.netloc.split(".")[1]

    # save to disk
    if not os.path.exists(os.path.join(os.getcwd(), filename + ".json")):
        documents = loader.load_data(urls=[base_url])
        # print(documents)
        index = GPTSimpleVectorIndex(documents,prompt_helper=prompt_helper)
        
        index.save_to_disk(os.path.join(os.getcwd(), filename + ".json"))
        print(f"{filename}.json saved successfully!")
    else:
        print(f"{filename}.json already exists.")

        # load from disk
    index = GPTSimpleVectorIndex.load_from_disk(
        os.path.join(os.getcwd(), filename + ".json")
    )
    

    rail_spec = spec
    
    output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, llm=llm_predictor.llm)
    # NOTE: we use the same output parser for both prompts, though you can choose to use different parsers
    # NOTE: here we add formatting instructions to the prompts.

    fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
    fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

    qa_prompt = QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)
    refine_prompt = RefinePrompt(fmt_refine_tmpl, output_parser=output_parser)
    # llm_predictor_gpt4 = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))
    response = index.query(
        query_str=query,
        text_qa_template=qa_prompt, 
        refine_template=refine_prompt, 
        llm_predictor=llm_predictor,
        
    
    )
    return response