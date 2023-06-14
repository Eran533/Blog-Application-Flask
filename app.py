import uuid

from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def read_blog_post():
    with open('data.json', 'r') as file:
        blog_posts = json.load(file)
    return blog_posts

def fetch_post_by_id(post_id):
    """
    Fetches a blog post by its ID from a JSON file.

    Args:
        post_id (int): The ID of the blog post to fetch.

    Returns:
        dict or None: A dictionary representing the blog post if found,
                      or None if the post with the given ID doesn't exist.

    """
    blog_posts = read_blog_post()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None

def update_post(post_id, post_content):
    blog_posts = read_blog_post()
    for post in blog_posts:
        if post["id"] == post_id:
            post["content"] = post_content
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)

@app.route('/')
def index():
    blog_posts = read_blog_post()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = read_blog_post()
        author = request.form.get('name')
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = {
            'id': str(uuid.uuid4()),
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
            }
        blog_posts.append(new_post)
        with open('data.json', 'w') as f:
            json.dump(blog_posts, f)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<string:post_id>', methods=['POST'])
def delete(post_id):
    flag = True
    blog_posts = read_blog_post()
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            flag = True
            break
        else:
            flag = False
    if not flag:
        raise Exception("Sorry, post does not exist")
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)
    return redirect(url_for('index'))

@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    elif request.method == 'POST':
        content = request.form.get('content')
        update_post(post_id, content)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

@app.route('/like/<string:post_id>', methods=['POST'])
def like(post_id):
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
        for post in blog_posts:
            if post['id'] == post_id:
                post["likes"] += 1
                break
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug = True)
