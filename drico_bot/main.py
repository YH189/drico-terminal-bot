def safe_calculate(user_input):
    parts = user_input.split()

    if len(parts) != 3:
        return None

    num1_str, operator, num2_str = parts

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        return None

    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            return 'error: division by zero'
        return num1 / num2
    elif operator == '%':
        if num2 == 0:
            return 'error: division by zero'
        return num1 % num2
    else:
        return None


def run_bot():
    print('--------------- ChatBot Router ---------------')

    while True:
        user_input = input('User > ').lower()

        if 'bye' in user_input or 'exit' in user_input:
            print('Bot > Thank you for utilizing the system. Goodbye. ')
            break
        elif 'automation' in user_input or 'agent' in user_input or 'workflow' in user_input:
            print('Bot > By analyzing your query, it appears to be automation or AI agent-focused:\n'
                  '- CrewAI: https://www.crewai.com/\n'
                  '- LangChain: https://www.langchain.com/\n'
                  '- Make.com: https://www.make.com/\n'
                  '- Zapier: https://zapier.com/')
        elif 'research' in user_input or 'found' in user_input:
            print('Bot > By analyzing your query, it appears to be research-focused:\n'
                  '- Perplexity: https://www.perplexity.ai/\n'
                  '- NotebookLM: https://notebooklm.google.com/\n'
                  '- Grok: https://grok.com/')
        elif 'create' in user_input or 'image' in user_input or 'video' in user_input:
            print('Bot > By analyzing your query, it appears to be a creation task:\n'
                  '- Midjourney: https://www.midjourney.com/\n'
                  '- Runway: https://runwayml.com/\n'
                  '- Gemini: https://gemini.google.com/\n'
                  '- ChatGPT: https://chatgpt.com/')
        elif 'build' in user_input or 'website' in user_input or 'app' in user_input or 'code' in user_input:
            print('Bot > By analyzing your query, it appears to be software development:\n'
                  '- Claude: https://claude.ai/\n'
                  '- Cursor: https://www.cursor.com/\n'
                  '- GitHub Copilot: https://github.com/features/copilot\n'
                  '- Base44 : https://app.base44.com/\n'
                  '- Loveable : https://lovable.dev/\n'
                  )
        elif '+' in user_input or '-' in user_input or '*' in user_input or '/' in user_input or '**' in user_input or '%' in user_input:
            result = safe_calculate(user_input)
            if result is None:
                print('Bot > I could not calculate that. Please provide a valid math expression.')
            else:
                print(f'Bot > The result is: {result}')
        elif 'how are you' in user_input or 'who are you' in user_input:
            print('Bot > I am a chatbot Router built using Python.')
        elif 'hi' in user_input or 'hello' in user_input:
            print('Bot > How can I assist you today?')
        elif 'list' in user_input or 'tools' in user_input or 'links' in user_input:
            print('Bot > Here are the recommended AI tools:\n'
                  '- Perplexity: https://www.perplexity.ai/\n'
                  '- Gemini: https://gemini.google.com/\n'
                  '- ChatGPT: https://chatgpt.com/\n'
                  '- Claude: https://claude.ai/')
        else:
            print('Bot > I did not understand that. Please try asking something else.')


if __name__ == '__main__':
    run_bot()