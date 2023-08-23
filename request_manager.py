#!/usr/bin/env python3
import datetime
import json
import os

import openai
import requests
from PIL import Image

import send_dalle_request
import send_gpt35_request
import user_inputs as inputs
import request_tools as req_tools

#global vars
deployment_name = ""
poem_writer_style_list = []

def main():
    #log the startime
    start_time = datetime.datetime.now()
    print("Script started:",start_time)

    #open exceptions at request
    dalle_errors = 0
    dalle_errors_list=[]

    #bool to call chatgpt to write poems
    write_poems = True
    show_images_runtime = True

    #load config
    path_to_file = os.path.join(os.getcwd(), "creds.json")
    with open(path_to_file) as f:
        config_data = json.load(f)

    # Set the directory where we'll store the image, create dir if not exist
    root_image_dir = os.path.join(os.curdir, 'images')
    generate_dir(root_image_dir)

    if write_poems:
        #set openai credentials
        set_chatgpt_credentials(config_data)
        #ask gpt to write poems
        poems_written_done = send_gpt35_request.send_request(root_image_dir, deployment_name, poem_writer_style_list)

        if poems_written_done is True:
            print("Finished writing poems."); print()
        else:
            print("Could not finish writing poems."); print()

    #scan poem dir into list
    poem_dir_fullpath_list = req_tools.get_subfolder_dir_paths(os.getcwd(), root_image_dir)
    print("dir list", poem_dir_fullpath_list)

    #set dalle credentials
    # set openai credentials
    set_dalle_credentials(config_data)

    #get poem content for each poem dir
    for poem_dir_path in poem_dir_fullpath_list:
        res, num = inputs.get_prompt()
        poem_tail_dir = req_tools.get_last_subdir_name(poem_dir_path)
        #set file extension to save according to scenario : use broker chatgtp to generate imaeg description or not
        poem_extension_used = inputs.poem_description_extension if inputs.use_poem_description else inputs.poem_extension
        poem_fn_path = os.path.join(poem_dir_path, poem_tail_dir + poem_extension_used)

        if os.path.exists(poem_fn_path):
            poem_desc = req_tools.read_file_into_title_and_poem(poem_fn_path)
            poem_text = ''.join(poem_desc)
            full_prompt = "\nImage Description:" + poem_text

            #create image dirs
            generate_dir(poem_dir_path)

            #request image
            for painter in inputs.painter_list:
                print("At painter:",painter)
                resp_data = send_dalle_request.send_request(full_prompt, res, num, openai, poem_writer_style_list, poem_tail_dir, painter)
                #print("***resp_data received",resp_data)

                #store and show image
                counter = 0
                image_name = os.path.basename(os.path.normpath(poem_dir_path))
                if "Error" not in resp_data:
                    for image in resp_data:
                        #print("***image in resp_data",image)
                        if "Error" not in image:
                            image_name = image_name + '_' + painter.replace(" ", "") + '_' + str(counter) + '.png'
                            #print("image_name",image_name)
                            image_path = os.path.join(poem_dir_path, image_name)
                            #print("Store image at " + image_path)

                            #download and store images for this poem
                            image_url = get_url(image)
                            if image_url != "":
                                store_image(image_url, image_path)
                                counter += 1
                                print(f"url {image_path}:", image_url)
                                # Open and display image
                                if show_images_runtime:
                                    image = Image.open(image_path)
                                    image.show(title=image_name)
                        else:
                            dalle_errors += 1
                            dalle_errors_list.append(image_name+"_"+painter)
                            print("Error getting this image -this img response" + image + " full response" + resp_data)
                else:
                    dalle_errors += 1
                    dalle_errors_list.append(image_name+"_"+painter)

    end_time = datetime.datetime.now()
    time_elapsed = end_time - start_time
    print("End of Script. Time elapsed:", time_elapsed, "Dalle errors:",dalle_errors, "at", dalle_errors_list)

def get_url(response):
    url = ""
    if 'url' in response:
        url = response['url']
    return url
def generate_dir(image_dir):
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

def store_image(image_url, image_path):
    generated_image = requests.get(image_url).content
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

def set_chatgpt_credentials(config_data):
    openai.api_version = config_data["chatgpt35_openai_api"]['OPENAI_API_VERSION']
    openai.api_type = config_data["chatgpt35_openai_api"]['OPENAI_API_TYPE']
    openai.api_base = config_data["chatgpt35_openai_api"]['OPENAI_API_BASE']
    openai.api_key = config_data["chatgpt35_openai_api"]['OPENAI_API_KEY']
    global deployment_name
    deployment_name = config_data["chatgpt35_openai_api"]['OPENAI_API_DEPLOYMENT_NAME']

def set_dalle_credentials(config_data):
    openai.api_version = config_data["dalle_openai_api"]['OPENAI_API_VERSION']
    openai.api_type = config_data["dalle_openai_api"]['OPENAI_API_TYPE']
    openai.api_base = config_data["dalle_openai_api"]['OPENAI_API_BASE']
    openai.api_key = config_data["dalle_openai_api"]['OPENAI_API_KEY']
    global deployment_name
    deployment_name = config_data["dalle_openai_api"]['OPENAI_API_DEPLOYMENT_NAME']

if __name__ == "__main__":
    main()
