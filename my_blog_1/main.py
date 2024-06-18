from flask import Flask, render_template
from post import Post
import requests

posts = requests.get("https://api.npoint.io/5abcca6f4e39b4955965").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)

             ############OR############
from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

# Fetch data from the API and convert JSON response to Python dictionary
response = requests.get("https://api.npoint.io/5abcca6f4e39b4955965")
posts = response.json()

# Iterate through the list of posts and create Post objects
post_objects = []
for post in posts:
    # Ensure post is a dictionary before accessing its keys
    if isinstance(post, dict):
        post_obj = Post(post.get('id', ''), post.get('title', ''), post.get('subtitle', ''), post.get('body', ''))
        post_objects.append(post_obj)
    else:
        print("Error: Invalid post data format")

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next((post for post in post_objects if post.id == index), None)
    if requested_post:
        return render_template("post.html", post=requested_post)
    else:
        return "Post not found!"

if __name__ == "__main__":
    app.run(debug=True)
