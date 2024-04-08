import requests
import json

def get_data(url):
    response = requests.get(url)
    return json.loads(response.text)

posts_data = get_data("http://jsonplaceholder.typicode.com/posts")
comments_data = get_data("http://jsonplaceholder.typicode.com/comments")

average_comments_per_user = {}

for post in posts_data:
    user_id = post["userId"]
    
    if user_id not in average_comments_per_user:
        average_comments_per_user[user_id] = {
            "count_posts": 0,
            "sum_comments": 0
        }
    
    post_comments = [comment for comment in comments_data if comment["postId"] == post["id"]]

    average_comments_per_user[user_id]["count_posts"] += 1
    average_comments_per_user[user_id]["sum_comments"] += len(post_comments)

for user_id, data in average_comments_per_user.items():
    average_comments_per_post = data["sum_comments"] / data["count_posts"]
    print(f"User {user_id}: {average_comments_per_post:.2f}")