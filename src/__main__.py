import configparser
import os
import shutil

import openai
import datetime
from gtts import gTTS
from playsound import playsound

# Le o arquivo ini
config = configparser.ConfigParser()
config.read('config.ini')

# Seta o API key
openai.api_key = config['openai']['api_key']

while True:
    try:
        frase = input("Qual sua pergunta Mestre Junior para GPT4 : ")
        response = openai.Completion.create(
            # engine="davinci",
            ##engine="text-davinci-002",
            engine="text-davinci-003",
            # model="code-davinci-002",
            prompt=frase,
            max_tokens=1024,  # Aumente o número máximo de tokens para obter respostas mais longas
            temperature=0.9,  # Aumente a temperatura para obter respostas mais criativas
            top_p=0.9,  # Diminua o valor de top_p para obter respostas mais inovadoras
        )
        print(response['choices'][0]['text'])

        # Gerar áudio a partir da resposta
        tts = gTTS(response['choices'][0]['text'], lang='pt')
        now = datetime.datetime.now()
        filename = f"mp3/{now.strftime('%Y-%m-%d %H:%M:%S')}.mp3"
        filename_text = f"text/{now.strftime('%Y-%m-%d %H:%M:%S')}.txt"
        tts.save(filename)
        playsound(filename)
        with open(filename_text, 'w') as file:
            file.write(frase + ' : ' + response['choices'][0]['text'])

    except:
        print(response['choices'][0]['text'])
    if frase == 'sair':

        folder = '/home/ubuntu/PycharmProjects/ChatGPT_v1/src/mp3'

        for filename in os.listdir(folder):
            if filename.endswith('.mp3'):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        break

if __name__ == "__main__":
    pass
