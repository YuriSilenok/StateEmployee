#!/usr/bin/python3.8
# coding=UTF-8

from github import Github
from datetime import datetime

TOKEN = 'TOKEN'
ORG = 'Students-of-the-city-of-Kostroma'
REPO = 'trpo_automation'
TEAMLEADS = ['Svyat935','urec-programmec', 'avilova']

githib = Github(TOKEN)
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
    print('Нарушено правило именования веток', del_branch_list)
    issue = repo.create_issue(title = 'Нарушено правило именования веток', body = str(del_branch_list))
    issue.add_to_assignees(TEAMLEADS)

for issue in repo.get_issues(state='open'):
    if issue.state == 'open' and (datetime.now() - issue.updated_at).days >= 7:
        print('Какие есть обновления по этой задаче?', issue)
        issue.create_comment('Какие есть обновления по этой задаче?')
    if issue.body == '':
        print('Пожалуйста, добавьте описание к этой задаче', issue)
        issue.create_comment('Пожалуйста, добавьте описание к этой задаче')
    if issue.milestone is None:
        print('Пожалуйста, добавьте веху к этой задаче', issue)
        issue.create_comment('Пожалуйста, добавьте веху к этой задаче')
    if issue.assignee is None:
        print('Пожалуйста, добавьте ответсвенного на эту задачу', issue)
        issue.create_comment('Пожалуйста, добавьте ответсвенного на эту задачу')
