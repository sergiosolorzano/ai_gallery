#!/usr/bin/env python3
import os
import json
import user_inputs

def send_request(root_image_dir, openai, deployment_name, poem_style):
    this_conversation = []
    poem_description_list = get_text_from_file()
    print("Number poems to process:", len(poem_description_list))
    for desc in poem_description_list:
        writer_style = desc[0]
        poem_folder = desc[1]
        poem_description = desc[2]
        poem_style.append([poem_folder, writer_style])
        print(); print("-"*30); print("Send Request to Write Poem: Writer Style", writer_style, "Poem Folder:", poem_folder + ".", " Poem Description:", poem_description)

        #check poem does not exist
        if check_poem_exists(os.path.join(root_image_dir, poem_folder, poem_folder+".txt")):
            print();print("Skip: Poem",os.path.join(root_image_dir, poem_folder, poem_folder+".txt"), "exists"); print()
            continue

        try:
            system_message = {"role": "system", "content": f"You are a modern 21st century poem writer very similar to {writer_style} style. You response with a JSON object and do not add any other text to your response."}
            this_conversation.append(system_message)
            content_to_gpt = f'Write a poem of no more than {user_inputs.poem_tokens} tokens as per this description: {poem_description} .Return JSON Object that has two elements, Title with the title of your poem, and Poem with the content of your poem. Do not add any other text.'
            this_conversation.append({"role": "user", "content": content_to_gpt})

            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=this_conversation,
                temperature=0.7,
                max_tokens=3000,
            )
            print("GPT Poem Received",response['choices'][0]['message']['content'])
            try:
                resp_json = json.loads(response['choices'][0]['message']['content'])
                poem_title = resp_json["Title"]
                poem_desc = resp_json["Poem"]
                write_response_to_file(root_image_dir, poem_folder, poem_title, poem_desc)
            except Exception as e:
                print(f"Skip: Failed to parse json.{poem_folder}", e)

        except openai.OpenAIError as e:
            # Handle connection error or timeout here
            print(f"1;31m[WARNING]\033[0mAn OpenAI error occurred:\033[0m ", str(e), "received " + response['choices'][0]['message']['content'])
            exit(1)

    return True

def get_text_from_file():
    # get text from file for prompt
    txt_filepath = "descriptions.txt"
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
                #print("**element", e)
                this_poem_list.append(e)
            description_list.append(this_poem_list)

    return description_list

def write_response_to_file(root_image_dir, poem_folder, poem_title, poem_desc):
    poem_dir_path = os.path.join(root_image_dir, poem_folder)
    poem_text_path = os.path.join(root_image_dir, poem_folder, poem_folder+".txt")
    generate_dir(poem_dir_path)
    with open(poem_text_path, 'w') as file:
        file.write(poem_title+"\n\n")
        file.write(poem_desc)

def check_poem_exists(poem_text_path):
    if os.path.exists(poem_text_path):
        return True
    else:
        return False

def generate_dir(image_dir):
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)