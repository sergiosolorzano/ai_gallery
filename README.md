# ai_gallery
Prompt chatgpt 3.5-turbo to write a poem and Dall-e to draw it inspired by the style of several artists.

Visit Our [Blog at Tapgaze how we made it, poems and image collection: We ask ChatGPT To write Poems and Dall-E to paint them](https://tapgaze.com/blog/ai_poem_gallery/)

<img width="1913" alt="blog-aigallery" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/ab348373-5d1b-4241-9ecb-f777aafee288">

Batch image results available on augmented reality for iPhone at the [Tapgaze app](https://apps.apple.com/gb/app/tapgaze/id1534427791).
    
    
Repo File Structure:
![code_snapshot-scaled copy](https://github.com/sergiosolorzano/ai_gallery/assets/24430655/6ed05cc1-7aae-4ba4-8602-895a2b57bb50)

---------------------------------------------
```
.
├── creds.json            #enter your Azure OpenAI API credentials, sample below
├── descriptions.txt      #poem description
├── images                #poem and dalle output
├── LICENSE    
├── README.md
├── request_manager.py    #manager calling scripts to send requests to chatgpt3.5 and dalle models
├── send_dalle_request.py #Azure OpenAI send request method to dalle
├── send_gpt35_request.py #Azure OpenAI send request method to gpt3.5_turbo
└── user_inputs.py        #request inputs

Complete creds.json with your Azure OpenAI credentials:
{
    "chatgpt35_openai_api": {
        "OPENAI_API_KEY": "",
        "OPENAI_API_VERSION": "",
        "OPENAI_API_BASE": "",
        "OPENAI_API_TYPE": "",
        "OPENAI_API_DEPLOYMENT_NAME": ""
    },
    "dalle_openai_api": {
        "OPENAI_API_KEY": "",
        "OPENAI_API_VERSION": "",
        "OPENAI_API_BASE": "",
        "OPENAI_API_TYPE": "",
        "OPENAI_API_DEPLOYMENT_NAME": "DOES_NOT_APPLY_NA"
    }
}
---------------------------------------------
```

Inputs at:
user_inputs.py and creds.json
