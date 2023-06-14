from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def fetch_post_by_id(post_id):
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None
def update_post(post_id, post_content):
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    for post in blog_posts:
        if post["id"] == post_id:
            post["content"] = post_content
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)

@app.route('/')
def index():
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('data.json', 'r') as f:
            blog_posts = json.load(f)
            post_id = len(blog_posts) + 1
            author = request.form.get('name')
            title = request.form.get('title')
            content = request.form.get('content')
            new_post = {
                'id': post_id,
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

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    elif request.method == 'POST':
        content = request.form.get('content')
        update_post(post_id, content)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
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

