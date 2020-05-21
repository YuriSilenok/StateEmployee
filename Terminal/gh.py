from github import Github
import vk

USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
ORG = 'Students-of-the-city-of-Kostroma'
REPO = 'trpo_automation'

githib = Github(USERNAME, PASSWORD)
org = githib.get_organization(ORG)
repo = org.get_repo(REPO)

del_branch_list = []
for branch in repo.get_branches():
    del_branch = True
    for item in ['master', 'dev', '18-', 'issue-']:
        if item in branch.name:
            del_branch = False
            break
    if del_branch:
        del_branch_list.append(branch.name)
if del_branch_list:
    repo.create_issue(title="Нарушено правило именования веток",body=str(del_branch_list))

for issue in repo.get_issues():
    if issue.body == '':
        issue.create_comment('Пожалуйста, добавьте описание к этой задаче')
