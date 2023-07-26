#!/usr/bin/env python3

def send_request(userprompt, res, num, openai, poem_style_list, poem_tail_dir, painter_style):
    #print("Dalle Send Code - Dalle Creds:", openai.api_version, openai.api_type, openai.api_base, openai.api_key)
    print("Sending request for userprompt:", userprompt, "\nres", res, "\nnum", num)

    #get image style
    poem_styles = [sublist for sublist in poem_style_list if sublist[0] == poem_tail_dir]
    img_style = f'Draw this poem {painter_style} style:'
    userprompt = img_style + userprompt
    #print("***Drawing this one with:", img_style)
    try:
        response = openai.Image.create(
            prompt=userprompt,
            size=res,
            n=num
        )
        response_data = response["data"]
        print("***Dalle res_data:", response_data)
        return response_data
    except openai.error.OpenAIError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

