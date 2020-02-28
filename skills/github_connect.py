from github import Github
import configparser


def get_api_key():
    config = configparser.ConfigParser()
    configFile = "/Users/kaitbyrne/Documents/Projects/chatbot-api/config/config.ini"
    config.read(configFile)
    return config['github']['api']


def github_repos(gitInstance):
    """
    Gets each repo from user's github and adds to a list
    :return: formatted string of all projects
    """
    repo_lst = []
    for repo in gitInstance.get_user().get_repos():
        repo_lst.append(str(repo.name))
    repo_str = "\n".join(repo_lst)
    return repo_str


def github_notifications(gitInstance):
    """
    Gets all notifications from user's github and adds to a list
    :return: formatted string of all notifications
    """
    notification_lst = []
    for notification in gitInstance.get_user().get_notifications():
        notification_lst.append(str(notification.name))
    notification_str = "\n".join(notification_lst)
    return notification_str


def github_helper(cmd):
    """
    Determines which github helper function to call
    :return: the result of the github helper function
    """

    # Github instance:
    gitInstance = Github(get_api_key())
    if 'project' or 'repo' in cmd:
        return github_repos(gitInstance)
    elif 'notification' in cmd:
        return github_notifications(gitInstance)


if __name__ == "__main__":
    print(github_helper('notifications'))
