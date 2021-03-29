#!/usr/bin/python3.8
# coding=UTF-8

from github import Github
from datetime import datetime
import re

TOKEN = 'TOKEN'
ORG = 'Students-of-the-city-of-Kostroma'
REPO = 'trpo_automation'
TEAMLEADS = ['Svyat935', 'urec-programmec', 'avilova', 'AnastasiVokhmyanina28']
MILESTONES_PATTERN = r'(Backlog|Sprint \d{1,2} \(18-(IS|VT)bo-[12][ab]\))'

githib = Github(TOKEN)
org = githib.get_organization(ORG)
repo = org.get_repo(REPO)

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

backlog_milestone = None
for milestone in repo.get_milestones(state='open'): 
    if milestone.title == 'Backlog': 
        backlog_milestone = milestone
        break

if backlog_milestone is None:
    issue = repo.create_issue(
        title = 'Не найдена веха Backlog', 
        body = 'Добавить веху Backlog',
        assignees = TEAMLEADS
    )
else:
    incorect_milestones = []
    for milestone in repo.get_milestones(state='open'):
        if not  re.match(MILESTONES_PATTERN, milestone.title):
            incorect_milestones.append(milestone.title)
    if incorect_milestones:
        print('Нарушено правило именования вех', incorect_milestones)
        faind = False
        for issue in repo.get_issues(creator='YuriSilenok'):
            if issue.title == 'Нарушено правило именования вех':
                if issue.state == 'close':
                    issue.edit(
                        state='open',
                        assignees = TEAMLEADS
                    )
                issue.create_comment(str(incorect_milestones) + '\n\nПриведите имена вех в соответсвии с регулярным выражением \n`' + MILESTONES_PATTERN + '`')
                faind = True
                break
        if not faind:
            issue = repo.create_issue(
                title = 'Нарушено правило именования вех', 
                body = str(incorect_milestones) + '\n\nПриведите имена вех в соответсвии с регулярным выражением \n`' + MILESTONES_PATTERN + '`',
                assignees = TEAMLEADS,
                milestone = backlog_milestone
            )
    else:
        for issue in repo.get_issues(state ='open', creator='YuriSilenok'):
            if issue.title == 'Нарушено правило именования вех':
                issue.create_comment('Все вехи корректны')
                issue.edit(
                    state='close'
                )

    incorect_branch = []
    for branch in repo.get_branches():
        del_branch = True
        for item in ['master', 'dev', '18-', 'issue-', 'merge']:
            if branch.name.find(item) == 0:
                del_branch = False
                break
        if del_branch:
            incorect_branch.append(branch.name)
        if branch.name.find('issue-') == 0:
            days = (datetime.now() - datetime.strptime(repo.get_branches()[5].commit.commit.last_modified,'%a, %d %B %Y %I:%M:%S GMT')).days
            if days >= 7:
                print('В ветке '+ branch.name +' давно не было активности')
                try:
                    issue_number = int(branch.name[6:])
                    issue = repo.get_issue(issue_number)
                    issue.create_comment('В ветке '+ branch.name +' давно не было активности')
                except:
                    print('Неправильный формат ветки', branch.name)

    if incorect_branch:
        print('Нарушено правило именования веток', incorect_branch)
        issue = repo.create_issue(
            title = 'Нарушено правило именования веток', 
            body = str(incorect_branch),
            assignees = TEAMLEADS,
            milestone = backlog_milestone
        )


     