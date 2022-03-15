import git

def get_hash():
    repo = git.Repo(search_parent_directories=True)
    git_hash = repo.head.object.hexsha
    if git_hash == None:
        git_hash = "N/A"
    return git_hash