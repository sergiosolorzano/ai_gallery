
# ai_gallery

<p align="center">
<img width="150" alt="star" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/3c0b02ea-9b11-401a-b6f5-c61b69ad651b">
</p>

Batch prompt from file for chatgpt 3.5-turbo to write poems inspired on a poet writing style and Dall-e to draw these inspired by the style of several artists. Requests to Azure OpenAI API.

---------------------------------------------

Visit Our [Blog at Tapgaze how we made it, poems and image collection: We ask ChatGPT To write Poems and Dall-E to paint them](https://tapgaze.com/blog/ai_poem_gallery/)

<img width="1883" alt="blog-aigallery2" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/7de6f1c7-54be-407f-8c97-530a85d16850">

---------------------------------------------

Batch image results available on augmented reality for iPhone at the [Tapgaze app](https://apps.apple.com/gb/app/tapgaze/id1534427791).

---------------------------------------------    

![code_snapshot-scaled copy](https://github.com/sergiosolorzano/ai_gallery/assets/24430655/ed5a5781-084d-43a1-b0df-1fe253039dcd)

<video src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/6962f72a-3057-4cac-9fbe-91c9e4f99be4" controls="controls" muted="muted" playsinline="playsinline">
      </video>

---------------------------------------------
```
Repo File Structure:
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

---------------------------------------------
