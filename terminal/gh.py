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
BRANCHES_PATTERN = r'(master|dev|(merge[_\-])?18-(IS|VT)bo-[12][ab]|issue-\d{1,4})'

GITHUB = Github(TOKEN)
ORG = GITHUB.get_organization(ORG)
REPO = ORG.get_repo(REPO)

def check_issue(repo):
    for issue in repo.get_issues():
        if issue.state == 'open' and (datetime.now() - issue.updated_at).days >= 7:
            mess = 'Какие есть обновления по этой задаче?'
            print(mess, issue)
            issue.create_comment(mess)
        if issue.body == '':
            mess = 'Пожалуйста, добавьте описание к этой задаче'
            print(mess, issue)
            if issue.state == 'close':
                issue.edit(
                    state = 'open'
                )
            issue.create_comment(mess)
        if issue.milestone is None:
            mess = 'Пожалуйста, добавьте веху к этой задаче'
            print(mess, issue)
            if issue.state == 'close':
                issue.edit(
                    state = 'open'
                )
            issue.create_comment(mess)
        if issue.assignee is None:
            mess = 'Пожалуйста, добавьте ответсвенного на эту задачу'
            print(mess, issue)
            if issue.state == 'close':
                issue.edit(
                    state = 'open'
                )
            issue.create_comment(mess)
def get_backlog_milestone(repo):
    for milestone in repo.get_milestones():
        if milestone.title == 'Backlog':
            if milestone.state == 'close':
                milestone.edit(state='open')
            return milestone
    print('Веха Backlog не найдена')
    return repo.create_issue(
        title = 'Не найдена веха Backlog',
        body = 'Добавить веху Backlog',
        assignees = TEAMLEADS
    )
def get_incorrect_milestones(repo, milestone_patterns):
    result = []
    for milestone in repo.get_milestones(state='open'):
        if not re.match(milestone_patterns, milestone.title):
            result.append(milestone.title)
    if len(result) > 0:
        print('Найдены некорректные вехи', result)
    return result
def get_incorrect_branches(repo, branches_pattern):
    result = []
    for branch in repo.get_branches():
        if not re.match(branches_pattern, branch.name):
            result.append(branch.name)
    if len(result) > 0:
         print('Найдены некорректные ветки', result)
    return result
def create_comment_for_incorrect(repo, teamleads, title, comment):
    faind = False
    for issue in repo.get_issues(creator='YuriSilenok'):
        if issue.title == title:
            print('Найдено совпадение', issue)
            faind = True
            if issue.assignees != teamleads:
                print('Назначены тимлиды',teamleads)
                issue.edit(
                    assignees = teamleads
                )
            if issue.state == 'close':
                issue.edit(
                    state='open'
                )
            print('Добавлен комментарий', comment)
            issue.create_comment(comment)
            break
    if not faind:
        print('Создана задача',title, comment)
        issue = repo.create_issue(
            title = title,
            body = comment,
            assignees = teamleads,
            milestone = backlog_milestone
        )
def check_branch_at_update(repo, teamleads):
    for branch in repo.get_branches():
        if branch.name.find('issue-') == 0:
            last_modified = branch.commit.commit.last_modified
            print(last_modified)
            days = (datetime.now() - datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S GMT')).days
            if days > 0 and days % 7 == 0:
                mess = 'В ветке '+ branch.name +' давно не было активности'
                print(mess)
                try:
                    issue_number = int(branch.name[6:])
                    issue = repo.get_issue(issue_number)
                    if issue.state == 'close':
                        issue.edit(state = 'open')
                        issue.create_comment('Кажется, вы не удалили ветку '+ branch.name +' и закрыли задачу')
                    else:
                        issue.create_comment(mess)
                except:
                    print('Неправильный формат ветки', branch.name)
check_issue(
    repo=REPO
)
backlog_milestone = get_backlog_milestone(
    repo=REPO
)
incorrect_milestone = get_incorrect_milestones(
    repo=REPO,
    milestone_patterns=MILESTONES_PATTERN
)
if len(incorrect_milestone) > 0:
    create_comment_for_incorrect(
        repo=REPO,
        teamleads=TEAMLEADS,
        title='Нарушено правило именования вех',
        comment=str(incorrect_milestone) + '\n\nПриведите имена вех в соответсвии с регулярным выражением \n`' + MILESTONES_PATTERN + '`'
    )
incorrect_branches = get_incorrect_branches(
    repo=REPO,
    branches_pattern=BRANCHES_PATTERN
)
if len(incorrect_branches) > 0:
    create_comment_for_incorrect(
        repo=REPO,
        teamleads=TEAMLEADS,
        title='Нарушено правило именования веток',
        comment=str(incorrect_branches) + '\n\nПриведите имена веток в соответсвие'
    )
check_branch_at_update(
    repo=REPO,
    teamleads=TEAMLEADS
)