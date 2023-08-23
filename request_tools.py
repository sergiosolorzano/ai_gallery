#!/usr/bin/env python3
import os

def get_subfolder_dir_paths(parent_folder, sub_folder):
    # Combine the parent_folder and sub_folder to form the complete path
    sub_folder_path = os.path.join(parent_folder, sub_folder)

    # Check if the sub-folder path exists
    if not os.path.exists(sub_folder_path) or not os.path.isdir(sub_folder_path):
        print("Sub-folder not found.")
        return []

    # Get all the items (files and directories) in the sub-folder
    items = os.listdir(sub_folder_path)

    # Filter out only the directory names
    directory_full_paths = [os.path.join(sub_folder_path, item) for item in items if os.path.isdir(os.path.join(sub_folder_path, item))]

    return directory_full_paths

def get_last_subdir_name(full_path):
    dirs = full_path.split(os.sep)
    last_subdir_name = dirs[-1]
    return last_subdir_name

def read_file_into_title_and_poem(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines