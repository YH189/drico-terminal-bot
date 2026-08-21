print('---------Rule Based ChatBot---------')
user_input = input('User >').lower()

if 'hi' in user_input or 'hello' in user_input:
    print('Bot > How can assist you today?')
elif 'how are you' in user_input or 'who are you' in user_input:
    print('Bot > I am rule based chatbot build by using python')
elif 'What AI tools should I use?' in user_input or 'Which AI is best' in user_input:
    print('Bot > If you want some information for your queries i can help you to assist for which AI tools you can use')
elif 'what' in user_input or 'how' in user_input:
    print('Bot > For your queries you can use AI tools like: openAI, Claude')
elif 'research' in user_input or 'found' in user_input:
    print('Bot > By analysing you quere it is a research type so you can use: Perplexity, Grok')
elif 'create' in user_input or 'image' in user_input or 'video' in user_input:
    print('Bot > By analysing you quere it is a creation type so you can use: Gemini, GPT, higgsfiels, seedance. ')
elif 'build' in user_input or 'website' in user_input or 'app' in user_input:
    print('Bot > By analysing you quere it a software building type fo you can use: Claude code, Codex, Grok, emergent, base44, loveable. ')