from blackmaria import maria

url="https://yellowjackets.fandom.com/wiki/F_Sharp"
spec=("""
    <rail version="0.1">

    <output>
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