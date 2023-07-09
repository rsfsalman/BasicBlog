"""
main.py - A Flask application for managing blog posts.

This module defines a Flask application with routes and functions to manage blog posts.
It imports the necessary modules and functions from Flask and globals.py.

Routes:
    - '/post/<int:post_id>': Displays a blog post based on its ID.
    - '/update/<int:post_id>': Updates a blog post based on its ID.
    - '/delete/<int:post_id>': Deletes a blog post based on its ID.
    - '/like/<int:post_id>': Increments the likes count of a blog post based on its ID.
    - '/add': Adds a new blog post.
    - '/': Displays the index page with a list of blog posts.

Functions:
    - fetch_post_by_id(post_id): Fetches a blog post from a list of blog posts based on its ID.
    - view_post(post_id): Displays a blog post based on its ID.
    - update(post_id): Updates a blog post based on its ID.
    - delete(post_id): Deletes a blog post based on its ID.
    - like(post_id): Increments the likes count of a blog post based on its ID.
    - add_post(): Adds a new blog post.
    - index(): Displays the index page with a list of blog posts.

Note:
    - The file_path variable should be set to the desired file path for saving the JSON file.
    - The list of dictionaries blog_posts should be defined with the desired blog posts.
"""


from flask import (Flask, render_template,
                   request, redirect, url_for)

from globals import (load_from_json, save_to_json)

app = Flask(__name__)

# Define the list of dictionaries in the following format:
# blog_posts = [
#     {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.''likes': 0},
#     {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.', 'likes': 10}
#     # Add more blog posts here if needed
# ]

# Define the file path where you want to save the JSON file
file_path = 'blog_posts.json'

# save_to_json(blog_posts, file_path)


def fetch_post_by_id(post_id):
    """
    Fetches a blog post from a list of blog posts based on its ID.

    :param post_id: (int) The ID of the blog post to fetch.

    :return: tuple, A tuple containing the blog post and its index in the list if found,
                otherwise returns None and -1.
    """
    blog_posts = load_from_json(file_path)
    for idx, post in enumerate(blog_posts):
        if post['id'] == post_id:
            return post, idx
    return None, -1


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """
    Displays a blog post based on its ID.

    :param post_id: (int) The ID of the blog post to display.

    :return: str or flask.Response: If the blog post is found, returns the rendered template 'post.html'
                                    with the blog post passed as a parameter. If the blog post is not found,
                                    returns a string message 'Post not found' with HTTP status code 404.

    """
    # Retrieve the post from the dictionary based on the post_id
    print("Post is opened!")  # Optional print statement for debugging purposes

    the_post, _ = fetch_post_by_id(post_id)
    print(the_post)  # Optional print statement for debugging purpose
    if the_post is None:
        return "Post not found", 404

    return render_template('post.html', post=the_post)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Updates a blog post based on its ID.

    :param post_id: (int) The ID of the blog post to update.

    :return: flask.Response or werkzeug.wrappers.Response:
                    If the HTTP method is POST and the update is successful,
                    redirects to the 'index' route. If the blog post is not found,
                    returns a string message 'Post not found' with HTTP status code 404.
                    If the HTTP method is GET, returns the rendered template 'update.html'
                    with the blog post passed as a parameter.
    """

    post, idx = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        author = request.form['author']
        content = request.form['content']
        title = request.form['title']
        print(post['id'])  # Optional print statement for debugging purposes
        updated_post = {'id': post['id'],
                        'author': author,
                        'title': title,
                        'content': content}
        if 'likes' in post:
            updated_post['likes'] = post['likes']

        blog_posts = load_from_json(file_path)
        blog_posts[idx] = updated_post
        save_to_json(blog_posts, file_path)
        return redirect(url_for('index'))

    print("its is a get method")  # Optional print statement for debugging purposes
    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Deletes a blog post based on its ID.

    :param post_id: (int): The ID of the blog post to delete.

    :return:  flask.Response or werkzeug.wrappers.Response: Redirects to the 'index' route after deleting
                                                            the blog post from the list of blog posts.

    """
    print("Delete")  # Optional print statement for debugging purposes
    blog_posts = load_from_json(file_path)

    post_found = False
    for idx, post in enumerate(blog_posts):
        if post['id'] == post_id:
            post_found = True
            del blog_posts[idx]
            break
    if post_found:
        save_to_json(blog_posts, file_path)
        return redirect(url_for('index'))
    else:
        return "Post not found", 404


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """
    Increases the likes count of a blog post based on its ID.

    :param post_id: (int) The ID of the blog post to increase the likes count.

    :return: flask.Response or werkzeug.wrappers.Response:
                    Redirects to the 'index' route after increasing
                    the likes count of the blog post.
    """

    print(post_id)  # Optional print statement for debugging purposes
    blog_posts = load_from_json(file_path)
    post_found = False
    for post in blog_posts:
        reg_id = post.get('id')
        if reg_id == post_id:
            post_found = True
            post['likes'] = post.get('likes', 0) + 1
            break
    if post_found:
        save_to_json(blog_posts, file_path)
        return redirect(url_for('index'))
    else:
        return "Post not found", 404


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Adds a new blog post.

    :return: flask.Response or werkzeug.wrappers.Response:
                                    If the HTTP method is POST and the addition is successful,
                                    redirects to the 'index' route. If the HTTP method is GET,
                                    returns the rendered template 'add.html'.

    """
    if request.method == 'POST':
        blog_posts = load_from_json(file_path)

        if len(blog_posts) == 0:
            post_id = 1
        else:
            post_id = blog_posts[-1]['id'] + 1
        author = request.form['author']
        content = request.form['content']
        title = request.form['title']
        new_post = {'id': post_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)

        save_to_json(blog_posts, file_path)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/')
def index():
    """
    Displays the index page with a list of blog posts.

    :return: flask.Response or werkzeug.wrappers.Response:
                                    Renders the template 'index.html' with the list of blog posts
                                    passed as a parameter.

    """
    # add code here to fetch the job posts from a file
    blog_posts = load_from_json(file_path)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
