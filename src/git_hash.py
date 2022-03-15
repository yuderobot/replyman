import git

def get_hash():
    repo = git.Repo(search_parent_directories=True)
    git_hash = repo.git.rev_parse(repo.head.object.hexsha, short=6)
    if git_hash == None:
        git_hash = "N/A"
    return git_hash