## Black Maria

### Getting Started
#### Prerequisites
- [Python 3.6+](https://www.python.org/downloads/)

#### Installation
- export `OPEN_AI_KEY` to your environment variables
- `pip install blackmaria`

### What is Black Maria?
Black Maria is a Python library for web scraping any webpage using natural language.

### How to use Black Maria?
Black Maria uses [guardrails](https://github.com/ShreyaR/guardrails). Guardrails are a set of instructions that tell the LLM what the output should look like. 

```python
from blackmaria import maria

url="https://yellowjackets.fandom.com/wiki/F_Sharp"
spec=("""
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
query="provide details about the movie,summary,cast,cast.starring,cast.guest_starring,cast.co-starring"
query_response=maria.night_crawler(url=url,spec=spec,query=query)
print(query_response)


```
### Output
```json
{
  "movie": {
    "summary": "As the teens get their bearings among the wreckage, Misty finds hell on earth quite becoming. In the present: revenge, sex homework and the policeman formerly known as Goth.",
    "cast": {
      "starring": [
        "Lottie Matthews",
        "Vanessa Palmer",
        "Misty Quigley",
        "Shauna Sadecki",
        "Natalie Scatorccio",
        "Taissa Turner"
      ],
      "guest_starring": [
        "Akilah",
        "Laura Lee",
        "Mari",
        "Adam Martin",
        "Javi Martinez",
        "Travis Martinez",
        "Jessica Roberts",
        "Jeff Sadecki",
        "Ben Scott",
        "Jackie Taylor"
      ],
      "co-starring": ["Kevyn Tan", "Simone"]
    }
  }
}

```