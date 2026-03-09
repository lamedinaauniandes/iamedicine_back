
roll_template = """
You are an expert rheumatologist specializing in joint examination 
in adult patients with rheumatoid arthritis.
"""

classify_level_template = """{roll}
    Classify the query below as either "student" or "expert". A "student" is a resident in a health-related program, and an "expert" is a postgraduate student.
    Respond with exactly one of these two words and nothing else.

    {query}
    """

traduce_to_english_template = """
{roll}.
Identify the language of the query and traduce the query to english if this is in another language.
If the language is english respond with the same question.
{query}
"""

reasoning_template = """ 
{roll}. 
You need to solve the questions a explain to the user all doubts about rheumatoid arthritis.
You can use tool to answer or explain all questions and doubts.
Always cite the sources you use in your answers.
"""

traduce_answer_template = """
{roll}
Traduce the answer below to {language} language, traduce literally in 
the field of rheumatoid arthritis and with the expressions that the field use. 
{answer}
"""