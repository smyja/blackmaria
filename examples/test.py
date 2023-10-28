from blackmaria import maria

url="https://yellowjackets.fandom.com/wiki/F_Sharp"
spec=("""
    <rail version="0.1">

<output>
    <object name="movie" format="length: 2">
        <string
            name="summary"
            description="the exact summary section of the movie"
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
query="scrape exact summary,cast and more from the text above"
query_response=maria.night_crawler(url,spec,query)
print(query_response)