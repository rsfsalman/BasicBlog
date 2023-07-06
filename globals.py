"""
globals.py - A module for handling JSON data.

This module provides functions to load data from a JSON file and save data as JSON to a file.

Functions:
    - load_from_json(file_path): Load data from a JSON file.
    - save_to_json(data, file_path): Save a list of dictionaries as JSON to a file.
"""
import json
# import textwrap


def load_from_json(file_path):
    """
    Load data from a JSON file.

    Args:
        file_path (str): The file path of the JSON file to load.

    Returns:
        list: The loaded data as a list of dictionaries.

    Raises:
        IOError: If there is an error while reading the JSON file.
        JSONDecodeError: If there is an error decoding the JSON data.

    Example:
        file_path = 'blog_posts.json'
        posts = load_from_json(file_path)
    """
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except IOError as e:
        raise IOError(f"Error while reading the JSON file: {str(e)}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON data: {str(e)}", e.doc, e.pos)


def save_to_json(data, file_path):
    """
    Save a list of dictionaries to a JSON file.

    Args:
        data (list): The list of dictionaries to be saved as JSON.
        file_path (str): The file path where the JSON file will be saved.

    Returns:
        None

    Raises:
        IOError: If there is an error while writing the JSON file.

    Example:
        blog_posts = [
            {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
            {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
            # Add more blog posts here if needed
        ]

        file_path = 'blog_posts.json'
        save_to_json(blog_posts, file_path)
    """

    # for item in data:
    #    item['content'] = textwrap.fill(item['content'], width=80)

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        # json.dump(data, json_file, indent=4, separators=(',', ': '))

    print(f"Data saved to {file_path}")
