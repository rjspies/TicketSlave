import os
import sys

from atlassian import Jira
from git import Repo, RemoteReference


def __create_git_branch_and_push_to_remote(branch_name: str):
    onetouch_repository = Repo("~/AndroidStudioProjects/Daedalus")
    branch = onetouch_repository.create_head(branch_name)
    onetouch_repository.remote().push(branch.name)
    remote_branch = RemoteReference(onetouch_repository, "refs/remotes/origin/{}".format(branch_name))
    branch.set_tracking_branch(remote_branch)


def __get_branch_prefix_for_issue(issue: dict):
    issue_type = issue["fields"]["issuetype"]["name"]
    match issue_type:
        case "Developer Story":
            return "Feature"
        case "User Story":
            return "Feature"
        case "Spike":
            return "Feature"
        case "Bug":
            return "Bugfix"
        case _:
            sys.exit("Issue type not recognized: {}".format(issue_type))


def __get_branch_name_for_issue(issue: dict):
    issue_key = issue["key"]
    summary = issue["fields"]["summary"]
    formatted_summary = summary.replace(" ", "_").replace("/", "_")
    branch_prefix = __get_branch_prefix_for_issue(issue)
    branch_name = "{0}/{1}+{2}".format(branch_prefix, issue_key, formatted_summary)
    return branch_name


def __load_jira_issue(ticket_id: str):
    jira = Jira(
        url="https://aresid.atlassian.net/",
        username=os.getenv("JIRA_TICKET_SLAVE_USERNAME"),
        password=os.getenv("JIRA_TICKET_SLAVE_TOKEN")
    )
    return jira.get_issue(ticket_id)


def main(arguments):
    ticket_id = arguments[0]
    issue = __load_jira_issue(ticket_id)
    branch_name = __get_branch_name_for_issue(issue)
    __create_git_branch_and_push_to_remote(branch_name)


if __name__ == "__main__":
    main(sys.argv[1:])
