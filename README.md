# ai_gallery

Batch prompt from file for chatgpt 3.5-turbo to write poems inspired on a poet writing style, describe what an image looks like for this poem, and Dall-e to draw these inspired by the style of several artists. Requests to Azure OpenAI API.

<p align="center">
<img width="150" alt="star" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/3c0b02ea-9b11-401a-b6f5-c61b69ad651b">
</p>

---------------------------------------------

The original project code has been enhanced by adding an intermediate step after a poem is generated, by also asking chatgpt to generate a description of what an image looks like for the abstract poem words.

<img width="1460" alt="image" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/769771f5-ad24-4bd1-9f1d-eb8ef829477c">

To read about the original two-step approach visit Our [Blog at Tapgaze how we made it, poems and image collection: We ask ChatGPT To write Poems and Dall-E to paint them](https://tapgaze.com/blog/ai_poem_gallery/)

To read about the enhanced three-step approach and rationale visit Our [Blog at Tapgaze how we made it, poems and image collection: We ask ChatGPT To write Poems and Dall-E to paint them](https://tapgaze.com/blog/chained-ai-models/)

<img width="1297" alt="image" src="https://github.com/sergiosolorzano/ai_gallery/assets/24430655/27c9dfdc-29d6-4117-99fe-de55912beeb6">

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

N.B: At user_inputs.py set bool <use_poem_description> for Chatgpt to generate a description of an image for each poem. If false, chatgpt generates each poem and Dall-e generates the image:
use_poem_description = True

---------------------------------------------
