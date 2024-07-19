import openai

# OpenAI API key
openai.api_key = 'your_api_key'

def summarize_document(document: str, lines: int = 10) -> str: #amount of required lines set to parameter
    prompt = f"Summarize the following document in exactly {lines} lines:\n\n{document}\n\nSummary:"
    response = openai.Completion.create(
        engine="text-davinci-003",  #type of AI engine used
        prompt=prompt,
        max_tokens=10,  
        n=1,
        stop=None,
        temperature=0.5 #model output creativity
    )
    summary = response.choices[0].text.strip()

    
    summary_lines = summary.split('\n')
    if len(summary_lines) == lines:
        return summary
    else:
        # Retry with more constrained prompt if the initial result does not work
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following document in exactly {lines} lines. Make sure the summary has exactly {lines} lines:\n\n{document}\n\nSummary:",
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5
        )
        summary = response.choices[0].text.strip()
        summary_lines = summary.split('\n')
        # Return the summary or handle if the retry still does not meet the requirement
        return summary if len(summary_lines) == lines else 'Summary could not be constrained to the exact line count.'

# document that I want summarized
document_text = """
*document goes here*
"""

summary = summarize_document(document_text)
print("Summary:")
print(summary)
