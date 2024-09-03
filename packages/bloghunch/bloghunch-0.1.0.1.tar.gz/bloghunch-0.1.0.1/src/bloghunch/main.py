import requests

class Bloghunch:
    def __init__(self, key, domain):
        self.key = key
        self.domain = domain
        self.base_url = f"https://api.bloghunch.com/app/{self.domain}"

    def get_all_posts(self):
        url = f"{self.base_url}/posts"
        headers = {"Authorization": f"Bearer {self.key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["posts"]
        except requests.exceptions.RequestException as e:
            print(e)
            return []

    def get_post(self, slug):
        url = f"{self.base_url}/posts/{slug}"
        headers = {"Authorization": f"Bearer {self.key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["post"]
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_post_comments(self, post_id):
        url = f"{self.base_url}/comments/{post_id}"
        headers = {"Authorization": f"Bearer {self.key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return []

    def get_all_subscribers(self):
        url = f"{self.base_url}/subscribers"
        headers = {"Authorization": f"Bearer {self.key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return []

    def get_all_tags(self):
        url = f"{self.base_url}/tags"
        headers = {"Authorization": f"Bearer {self.key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return []