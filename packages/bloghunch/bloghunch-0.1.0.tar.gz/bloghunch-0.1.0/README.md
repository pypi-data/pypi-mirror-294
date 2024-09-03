# Bloghunch Python SDK

This is a Python SDK for interacting with the Bloghunch API. It provides an easy-to-use interface for accessing various Bloghunch features.

## Installation

You can install the Bloghunch python SDK using pip:

```
pip install bloghunch
```

## Usage

Here's a quick example of how to use the bloghunch SDK:

```python
from bloghunch import Bloghunch

# Initialize the Bloghunch client
client = Bloghunch(key="your_api_key", domain="your_domain")

# Get all posts
posts = client.get_all_posts()
print(posts)

# Get a specific post
post = client.get_post("post-slug")
print(post)

# Get comments for a post
comments = client.get_post_comments("post_id")
print(comments)

# Get all subscribers
subscribers = client.get_all_subscribers()
print(subscribers)

# Get all tags
tags = client.get_all_tags()
print(tags)
```

## Features

- Get all posts
- Get a specific post by slug
- Get comments for a post
- Get all subscribers
- Get all tags

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.