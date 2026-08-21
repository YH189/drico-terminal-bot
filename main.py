print('---------Rule Based ChatBot---------')

while True:
    user_input = input('User > ').lower()

    if 'bye' in user_input or 'exit' in user_input:
        print('Bot > Goodbye! Have a great day.')
        break
    elif 'hi' in user_input or 'hello' in user_input:
        print('Bot > How can I assist you today?')
    elif 'how are you' in user_input or 'who are you' in user_input:
        print('Bot > I am a rule-based chatbot built using Python.')
    elif 'what ai tools should i use' in user_input or 'which ai is best' in user_input:
        print('Bot > If you want information for your queries, I can help you determine which AI tools to use.')
    elif 'research' in user_input or 'found' in user_input:
        print('Bot > By analyzing your query, it appears to be research-focused, so you can use: Perplexity, Grok.')
    elif 'create' in user_input or 'image' in user_input or 'video' in user_input:
        print('Bot > By analyzing your query, it appears to be a creation task, so you can use: Gemini, GPT.')
    elif 'build' in user_input or 'website' in user_input or 'app' in user_input:
        print('Bot > By analyzing your query, it appears to be software development, so you can use: Claude, Codex.')
    elif 'what' in user_input or 'how' in user_input:
        print('Bot > For your queries, you can use AI tools like OpenAI and Claude.')
    else:
        print('Bot > I did not understand that. Please try asking something else.')