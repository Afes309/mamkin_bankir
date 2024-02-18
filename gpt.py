from pl import prompt_for_review
import g4f



allowed_models = [
        'code-davinci-002',
        'text-ada-001',
        'text-babbage-001',
        'text-curie-001',
        'text-davinci-002',
        'text-davinci-003'
        ]

def get_market_overview(prompt_text):

    #prompt_text = prompt_for_review()
    #prompt_text = 'Сделай обзор рынков'

    response = g4f.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            provider = g4f.Provider.GPTalk,
            messages = [{'role':'user', 'content':prompt_text}]
            )

    print(response)


if __name__ == '__main__':
    #prompt_text = prompt_for_review()
    prompt_text = 'Сделай обзор рынков'
    #chats = [g4f.Provider.Bard,g4f.Provider.Bing,g4f.Provider.ChatBase,g4f.Provider.ChatForAi]
    get_market_overview(prompt_text)
    #print([provider.__name__ for provider in g4f.Provider.__providers__ if provider.working ])
