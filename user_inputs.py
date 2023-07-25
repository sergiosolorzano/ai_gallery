#!/usr/bin/env python3

#dalle
resolution = '1024x1024'
number_imgs = 1
#gpt writer
poem_tokens = 700
painter_list = ["Vincent van Gogh", "Gustave Courbet", "Grant Wood", "Leonardo da Vinci", "Jacques-Louis David", "Sandro Botticelli", "Henri Matisse", "Peter Paul Rubens", "Pierre-Auguste Renoir", "Johannes Vermeer", "Edvard Munch", "Salvador Dali"]

def get_prompt():
    return resolution, number_imgs