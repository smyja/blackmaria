from blackmaria import maria

url="https://www.imdb.com/user/ur68581805/watchlist"
spec=("""
    <rail version="0.1">

<output>
    <object name="watchlist">

        <string
            name="title"
            description="the exact title of show or movie"
            format="length: 200 240"
            on-fail-length="noop"
        />
        <string
            name="summary"
            description="the exact summary section of show or movie"
            format="length: 200 240"
            on-fail-length="noop"
        />

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
query="get the title and summary of the movie/tvshow"
query_response=maria.night_crawler(url,spec,query)
print(query_response)