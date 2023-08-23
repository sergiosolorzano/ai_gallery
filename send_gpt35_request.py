#!/usr/bin/env python3
import os
import json
import user_inputs as inputs
import request_tools as req_tools
import openai

def decorator_chatgpt_send_request(func):
    #get poem
    def wrapper(*args):
        root_image_dir, deployment_name, poem_style = args
        poem_description_list = get_text_from_file()
        print("At Wrapper: Number poems to process:", len(poem_description_list))
        for desc in poem_description_list:
            this_conversation = []
            writer_style = desc[0]
            poem_folder = desc[1]
            poem_description = desc[2]
            poem_style.append([poem_folder, writer_style])
            print(); print("-" * 30)
            print("At Wrapper: Send Request to Write Poem: Writer Style", writer_style, "Poem Folder:", poem_folder + ".",
                  " Poem Description:", poem_description)

            # check poem does not exist
            if check_poem_exists(os.path.join(root_image_dir, poem_folder, poem_folder + inputs.poem_extension)):
                print(); print("Skip: Poem", os.path.join(root_image_dir, poem_folder, poem_folder + inputs.poem_extension), "exists")
                print()
                continue

            system_message = {"role": "system",
                              "content": f"You are a modern 21st century poem writer very similar to {writer_style} style. You response with a JSON object and do not add any other text to your response."}
            this_conversation.append(system_message)
            content_to_gpt = f'Write a poem of no more than {inputs.poem_tokens} tokens as per this description: {poem_description} .Return JSON Object that has two elements, Title with the title of your poem, and Poem with the content of your poem. Do not add any other text.'
            this_conversation.append({"role": "user", "content": content_to_gpt})

            # Call sub-method and wait for the response
            response, error = make_openai_request(this_conversation, deployment_name)

            if error is not None:
                print(f"1;31m[WARNING]\033[0mAn OpenAI error occurred:\033[0m ", str(error),
                      "received " + response['choices'][0]['message']['content'])
                exit(1)

            print("GPT Poem Received", response['choices'][0]['message']['content'])
            try:
                resp_json = json.loads(response['choices'][0]['message']['content'])
                poem_title = resp_json["Title"]
                poem_desc = resp_json["Poem"]
                write_response_to_file(root_image_dir, poem_folder, poem_title, poem_desc, inputs.poem_extension)
            except Exception as e:
                print(f"Skip: Failed to parse json.{poem_folder}", e)

        #request
        if (inputs.use_poem_description):
            func(root_image_dir, deployment_name, poem_style)
        return True
    return wrapper

@decorator_chatgpt_send_request
def send_request(root_image_dir, deployment_name, poem_style):
    #get description of poem
    poem_dir_fullpath_list = req_tools.get_subfolder_dir_paths(os.getcwd(), root_image_dir)
    for poem_dir_path in poem_dir_fullpath_list:
        this_conversation = []
        poem_tail_dir = req_tools.get_last_subdir_name(poem_dir_path)
        poem_fn_path = os.path.join(poem_dir_path, poem_tail_dir + inputs.poem_extension)
        if os.path.exists(poem_fn_path):
            poem_content = req_tools.read_file_into_title_and_poem(poem_fn_path)
            poem_title = poem_content[0].strip()
            poem_text = ''.join(poem_content[1:])
            print(); print("-"*30); print("Send Request to Get Image Description of Poem:" + poem_text)

            #check poem description does not exist
            if check_poem_desc_exists(os.path.join(root_image_dir, poem_tail_dir, poem_tail_dir + inputs.poem_description_extension)):
                print();print("Skip: Poem Description",os.path.join(root_image_dir, poem_tail_dir, poem_tail_dir + inputs.poem_description_extension), "exists"); print()
                continue

            system_message = {"role": "system", "content": f"You are an expert interpreter of poetry and canvas art. You respond with a JSON object that has one element, Description, and you do not add any other text to your response."}
            this_conversation.append(system_message)
            example_for_gpt = ""#"Suppose the poem you read talks about a winter evening in a quiet village. Here's how you can describe the image: A tranquil winter scene unfolds with a cabin glowing warm amber against a backdrop of deep blue sky and silver snow. Frost-coated trees stand sentinel, framing a frozen pond that reflects the moonlight, while snowflakes gently swirl in the air."
            content_to_gpt = f'Write a description for an image that captures the main idea and emotions conveyed by the following poem. Be descriptive of the image as if someone is painting what you say, don not explain what each element in the image means. {example_for_gpt} Your response returns a JSON Object that has one element, Description. Do not add any other text. This is the poem:{poem_text}'
            #maurizio style podcast: content_to_gpt = f'Describe an abstract image for this poem. Do not use names of people or persons. Do not say in the description it is an image of a person. The center or protagonist of the image you describe is not a person. Do not explain the image you describe, only describe the image. Your response returns a JSON Object that has one element, Description. Do not add any other text. This is the poem:{poem_text}'
            this_conversation.append({"role": "user", "content": content_to_gpt})

            #print("\n\nChatGPT System_Message Request Prompt:" + system_message['content'])
            #print("\n\nChatGPT Description Request Prompt:" + content_to_gpt)

            # Call sub-method and wait for the response
            response, error = make_openai_request(this_conversation, deployment_name)

            if error is not None:
                print(f"1;31m[WARNING]\033[0mAn OpenAI error occurred:\033[0m ", str(error),
                      "received " + response['choices'][0]['message']['content'])
                exit(1)

            print("GPT Poem Description Received",response['choices'][0]['message']['content'])
            try:
                resp_json = json.loads(response['choices'][0]['message']['content'])
                poem_desc = resp_json["Description"]
                write_response_to_file(root_image_dir, poem_tail_dir, poem_title, poem_desc, inputs.poem_description_extension)
            except Exception as e:
                print(f"Skip: Failed to parse json.{poem_tail_dir}", e)

    return True

def make_openai_request(this_conversation, deployment_name):
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=this_conversation,
            temperature=0.7,
            max_tokens=3000,
        )
        return response, None
    except openai.OpenAIError as e:
        return None, e

def get_text_from_file():
    # get text from file for prompt
    txt_filepath = inputs.user_description_input_filename
    description_list = []
    skip_first_line = True
    with open(txt_filepath, 'r') as file:
        for line in file:
            if skip_first_line:
                skip_first_line = False
                continue
            elements = line.strip().split(":")
            this_poem_list = []
            for e in elements:
                this_poem_list.append(e)
            description_list.append(this_poem_list)

    return description_list

def write_response_to_file(root_image_dir, poem_folder, poem_title, poem_desc, file_extension):
    poem_dir_path = os.path.join(root_image_dir, poem_folder)
    poem_text_path = os.path.join(root_image_dir, poem_folder, poem_folder+file_extension)
    generate_dir(poem_dir_path)
    with open(poem_text_path, 'w') as file:
        file.write(poem_title+"\n\n")
        file.write(poem_desc)

def check_poem_exists(poem_text_path):
    if os.path.exists(poem_text_path):
        return True
    else:
        return False

def check_poem_desc_exists(poem_text_path):
    if os.path.exists(poem_text_path):
        return True
    else:
        return False

def generate_dir(image_dir):
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)