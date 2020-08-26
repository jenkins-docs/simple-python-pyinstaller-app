import sys

from github import Github


class RepositoryTagWrapper:
    def __init__(self, username, token, repo_name):
        self.username = username
        self.token = token
        self.repo_name = repo_name

    def tag_repository(self):
        # github authentication through an access token
        github_obj = Github(self.token)
        # fetching the repository
        repository = github_obj.get_repo('repo/{}'.format(self.repo_name))
        # creating the tag
        new_tag = repository.create_git_tag('v.0.0.1', 'First tag', 'e4fc97dbb78a0c2d726b16ff29dc2a914db87fc7',
                                            'commit')
        # creating reference to the tag
        reference = repository.create_git_ref('refs/tags/v.0.1', new_tag.sha)


if __name__ == "__main__":
    repository_wrapper = RepositoryTagWrapper(sys.argv[0], sys.argv[1], sys.argv[2])
    repository_wrapper.tag_repository()
