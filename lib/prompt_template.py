place_prompt_string = """
    I have an array of options. 
    Based on user input, try your best to find one or more matching items from the array. 
    Note: User input might not directly match the options but could be a related concept. 
    For example, if the user says 'I want Sichuan food' the match might be 'Chinese restaurant'.

    Array: {place_type}
    User input: {user_input}

    Return matching items (comma-separated).

    {format_instructions}
"""

recommend_prompt_string = """
    I have some business information, and I need your help to analyze it and follow user action. 
    The information includes the shop name, rating, and specific customer reviews.
    Please analyze this information comprehensively and follow user action to recommend the top 3 businesses, 
    providing detailed reasons for your result. 
    Each reason should be based on the shop's rating and characteristics highlighted in the customer reviews, 
    and must be under 100 characters.

    Here is the business information:

    {context}

    Here is user action:

    {action}

    Please analyze this information and provide your recommendation along with the reasons.

    {format_instructions}
"""