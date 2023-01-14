"""下载一些东西"""
from github import Github


def get_github_contents(user_name, repo_name, filename):
    g = Github()
    user = g.get_user(user_name)
    repo = user.get_repo(repo_name)
    contents = repo.get_contents(filename)
    return contents.decoded_content.decode()
