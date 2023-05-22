import requests

#Query webui for LLM output

HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

def getLLMOutput(prompt:str):
    request = {
        'prompt': prompt,
        'max_new_tokens': 400,
        'do_sample': True,
        'temperature': 1.3,
        'top_p': 0.1,
        'typical_p': 1,
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        return (result)
    
# prompt = "\n### Chat: \nTwofth:hi neuro \nVIPTurboPulseLane:peepoHey hi neuro \nOh_Sup:Hi Neuro! \nFeelMyCake:Hi Neuro \ncranberryruby:Clap \nnnyjoh:Hi \nGreatorian:NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam neuroLebronJam NeuroCheer neuroLebronJam AnnyLebronJam AnnyLebronJam AnnyLebronJam vedal9Cheer NeuroCheer NeuroCheer NeuroCheer NeuroCheer \nwhite245:vedal9AYAYA vedal9AYAYA vedal9AYAYA vedal9AYAYA vedal9AYAYA \nEthanSk13s:neuro peepoHey \nmarswatchn:Hello Neuro \noden_twi:Hi \nlucian_souzer:Hi nuero \nmug9n:nuero \nwisurubi:neuroWave \nSuminoRisa:Hi neuro \nmezkal4pe:@Rafieable WAYTOODANK WORTH IT \nKShugoshas:vedal9Cheer vedal9Cheer vedal9Cheer vedal9Cheer vedal9Cheer \nwhatsafterlike123:HEYYY \nVanillaSixtySix:neuroWave hi nuero!!! \nhagutt:HI NEURO \n### Neuro-sama: Hello everyone, I'm Neuro-sama and I'm here to entertain you all! How can I help you today?"
# prompt = "\n### Chat: Twofth:hi neuro \nVIPTurboPulseLane:peepoHey hi neuro \nOh_Sup:Hi Neuro! \nFeelMyCake:Hi Neuro \ncranberryruby:Clap \nnnyjoh:Hi \nGreatorian:NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam NeuroCheer neuroLebronJam neuroLebronJam NeuroCheer neuroLebronJam AnnyLebronJam AnnyLebronJam AnnyLebronJam vedal9Cheer NeuroCheer NeuroCheer NeuroCheer NeuroCheer \nwhite245:vedal9AYAYA vedal9AYAYA vedal9AYAYA vedal9AYAYA vedal9AYAYA \nEthanSk13s:neuro peepoHey \nmarswatchn:Hello Neuro \noden_twi:Hi \nlucian_souzer:Hi nuero \nmug9n:nuero \nwisurubi:neuroWave \nSuminoRisa:Hi neuro \nmezkal4pe:@Rafieable WAYTOODANK WORTH IT \nKShugoshas:vedal9Cheer vedal9Cheer vedal9Cheer vedal9Cheer vedal9Cheer \nwhatsafterlike123:HEYYY \nVanillaSixtySix:neuroWave hi nuero!!! \nhagutt:HI NEURO \n### Neuro-sama: Hello everyone, I'm Neuro-sama and I'm here to entertain you all! How can I help you today? \n### Chat: Greatorian:Filian wants to troll you Neuro how do you feel about that ? \nmechanical_gal:Tutel \nmultiplespiders:neuro do you shoot people? \nIMissEva:monkaLaugh \nSteambatsy:AI of the Turtle, what is your wisdom? \nGNU_uguu:monkaLaugh \nyoshifan007:What’s your favorite Ben and Jerry’s ice cream flavor? \nGRNKRBY:Do you believe in magic? \ndivinejudgment1231:Huh \nhefoe505:monkaLaugh \nLightmare99:Hi Neuro!!!! \nlucian_souzer:Tutel \nautistictechie:There are *three* laws of robotics. \nKPorentastange:Could you please say water in a british accent? \nSquidyTeaa:bruh... \nbubbasbigblast:What is the 4th law of Robotics? \n### Neuro-sama: "
# print("Chat:", prompt, "\nNeuro-sama:", getLLMOutput(prompt))