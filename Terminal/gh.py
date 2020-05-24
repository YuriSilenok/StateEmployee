#!/usr/bin/python3.8
# coding=UTF-8

from github import Github
from datetime import datetime
import re

TOKEN = 'TOKEN'
ORG = 'Students-of-the-city-of-Kostroma'
REPO = 'trpo_automation'
TEAMLEADS = ['Svyat935', 'urec-programmec', 'avilova']
MILESTONES_PATTERN = r'(Backlog|Sprint \d{1,2} \(18-(IS|VT)bo-[12][ab]\))'

githib = Github(TOKEN)
org = githib.get_organization(ORG)
repo = org.get_repo(REPO)

incorect_branch = []
for branch in repo.get_branches():
    del_branch = True
    for item in ['master', 'dev', '18-', 'issue-']:
        if item in branch.name:
            del_branch = False
            break
    if del_branch:
        incorect_branch.append(branch.name)
if incorect_branch:
    print('Нарушено правило именования веток', incorect_branch)
    issue = repo.create_issue(
        title = 'Нарушено правило именования веток', 
        body = str(incorect_branch),
        assignees = TEAMLEADS,
        milestone = 'Backlog')

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

incorect_milestones = []
for milestone in repo.get_milestones(state='open'):
    if not  re.match(MILESTONES_PATTERN, milestone.title):
        incorect_milestones.append(milestone.title)
if incorect_milestones:
    print('Нарушено правило именования вех', incorect_milestones)
    issue = repo.create_issue(
        title = 'Нарушено правило именования вех', 
        body = str(incorect_milestones) + '\nПриведите имена вех в соответсвии с регулярным выражением `' + MILESTONES_PATTERN + '`',
        assignees = TEAMLEADS,
        milestone = 'Backlog')
        