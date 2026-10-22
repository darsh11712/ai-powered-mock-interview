import language_tool_python

def calculate_grammatical_score(text):
    # Initialize the grammar checking tool
    tool = language_tool_python.LanguageTool('en-US')

    # Check the text for grammar issues
    matches = tool.check(text)

    # Count the total errors
    total_errors = len(matches)

    # Simple scoring: 
    # Assume 100 as a perfect score and subtract 10 points per error (or adjust as needed)
    score = max(0, 100 - (total_errors * 10))

    # Prepare error details
    error_details = [
        {
            "message": match.message,
            "suggestions": match.replacements,
            "error": match.context,
        }
        for match in matches
    ]

    return score, total_errors, error_details

# Example usage
text = """This is an example text. It have some grammar mistakes, like a missplaced word."""
score, total_errors, errors = calculate_grammatical_score(text)

print(f"Grammatical Score: {score}")
print(f"Total Errors: {total_errors}")
print("Details of Errors:")
for i, error in enumerate(errors, 1):
    print(f"{i}. Error: {error['error']}")
    print(f"   Message: {error['message']}")
    print(f"   Suggestions: {', '.join(error['suggestions'])}")
