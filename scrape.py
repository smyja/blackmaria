#guard rails

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


from gpt_index import (GPTSimpleVectorIndex, PromptHelper,
                       )
from gpt_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from gpt_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL, DEFAULT_REFINE_PROMPT_TMPL
from gpt_index.output_parsers import GuardrailsOutputParser
from gpt_index.llm_predictor import StructuredLLMPredictor
llm_predictor = StructuredLLMPredictor()
# llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-curie-001"))
from cray import BeautifulSoupWebReader


loader = BeautifulSoupWebReader()
max_input_size = 4096
# set number of output tokens
num_output = 100
# set maximum chunk overlap
max_chunk_overlap = 20
prompt_helper = PromptHelper( max_input_size,num_output, max_chunk_overlap)

documents = loader.load_data(urls=["https://yellowjackets.fandom.com/wiki/F_Sharp"])
# print(documents)
#for readme.io, links shiuld look like this: https://docs.mono.com with
index = GPTSimpleVectorIndex(documents,prompt_helper=prompt_helper)
index.save_to_disk('com.json')
# # load from disk

index = GPTSimpleVectorIndex.load_from_disk('com.json')
rail_spec = ("""
<rail version="0.1">

<output>
    <object name="movie" format="length: 2">
        <string
            name="summary"
            description="the summary section of the movie"
            format="length: 200 240"
            on-fail-length="noop"
        />
        <object name="cast" description="The cast in the movie" format="length: 3">
        <list name="starring">
    
            <string format="two-words"
            on-fail-two-words="reask"
            description="The starring section for the movie and roles"
     
            
            />
        </list>
        <list name="guest_starring">
        
           <string format="two-words"
            on-fail-two-words="reask"
            description="The Guest starring section and roles"
            />
        </list>
        <list name="co-starring">
        
           <string format="two-words"
            on-fail-two-words="reask"
            description="the starring section"
            />
        </list>
        
        </object>


    </object>
</output>

<prompt>

Query string here.

@xml_prefix_prompt

{output_schema}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
""")
output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, llm=llm_predictor.llm)
# NOTE: we use the same output parser for both prompts, though you can choose to use different parsers
# NOTE: here we add formatting instructions to the prompts.

fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

qa_prompt = QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)
refine_prompt = RefinePrompt(fmt_refine_tmpl, output_parser=output_parser)
response = index.query(
    "provide details about the movie,summary,cast,cast.starring,cast.guest_starring,cast.co-starring", 
    text_qa_template=qa_prompt, 
    refine_template=refine_prompt, 
    llm_predictor=llm_predictor,
    similarity_cutoff=0.7,
    required
)
# response=index.query('can i verify my users identity?provide a link',similarity_cutoff=0.7,similarity_top_k=3,response_mode="compact")

print(response)