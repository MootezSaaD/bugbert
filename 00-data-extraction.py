
import logging
import pandas as pd
import itertools
import collections
from collections import Counter, defaultdict
import statistics
import itertools
import re
import math
from pprint import pprint
from bs4 import BeautifulSoup as Soup
import datetime
import pymongo as pym

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_issue_csv(project):
    client = pym.MongoClient("mongodb://localhost:27017/")
    db = client['JiraRepos']
    source_collection = db[project]
    cursor = source_collection.find({})

    d = {'issue_id': [],
         'type': [],
         'status': [],
         'priority': [],
         'resolution': [],
         'projectid': [],
         'created':[],
         'updated':[],
         'description': [],
         'title': [],
         'components': [],
         }

    i = 0

    for issue in cursor:
        try:
            issue_key = issue['key']
            logging.info(issue_key)

            try:
                issuetype = issue['fields']['issuetype']['name']
            except Exception:
                issuetype = 'None'

            try:
                status = issue['fields']['status']['name']
            except Exception:
                status = 'None'
            try:
                priority = issue['fields']['priority']['name']
            except Exception:
                priority = 'None'
            projectid = issue['fields']['project']['name']
            try:
                resolution = issue['fields']['resolution']['name']
            except Exception:
                resolution = 'Open'

            try:
                componentsArray = issue['fields']['components']
                component = ""
                for i in range(0, len(componentsArray)):
                    component = component + i['name']

            except Exception:
                component = ''

            try:
                created = issue['fields']['created']
            except Exception:
                created = 'No creation date'
            try:
                updated = issue['fields']['updated']
            except Exception:
                updated = 'No update date'

            try:
                description = issue['fields']['description']
            except Exception:
                description = ''
            try:
                title = issue['fields']['summary']
            except Exception:
                title = ''

            d['issue_id'].append(issue_key)

            d['type'].append(issuetype)
            d['status'].append(status)
            d['priority'].append(priority)
            d['resolution'].append(resolution)
            d['projectid'].append(projectid)
            d['components'].append(component)

            d['created'].append(created)
            d['updated'].append(updated)

            d['description'].append(description)
            d['title'].append(title)

            logging.info("SUCCESS")

            i += 1
            logging.info(i)

        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass
    logging.info(f'Creating csv.')
    df = pd.DataFrame.from_dict(d)
    filename = 'issues_'+project.lower()+'.csv'
    logging.info(filename)
    df.to_csv(filename, sep=';', index=False)
    return None

def extract_links_csv(project):
    """
    Extract the links from the JSON in the MongoDB
    :return: csv of all links.
    """
    client = pym.MongoClient("mongodb://localhost:27017/")
    db = client['JiraRepos']
    source_collection = db[project]
    cursor = source_collection.find({})

    d = {'name':[],
         'linktype': [],
         'issue_id_1': [],
         'issue_id_2': [],
         }
    epiclinkfield_dict = { 'Apache': 'customfield_12311120',
        'Hyperledger': 'customfield_10006',
        'IntelDAOS': 'customfield_10092',
        'JFrog': 'customfield_10806',
        'Jira':    'customfield_12931',
        'JiraEcosystem': 'customfield_12180',
        'MariaDB':    'customfield_10600',
        'MindVille':    'customfield_10000',
        'MongoDB':    'customfield_10857',
        'Qt':    'customfield_10400',
        'Redhat':    'customfield_12311140',
        'Sakai':    'customfield_10772',
        'SecondLife':    'customfield_10871',
        'Sonatype':    'customfield_11500',
        'Spring':    'customfield_10680'
        }

    for issue in cursor:
        try:
            issue_key = issue['key']
            logging.info(issue_key)

            if project=='RedHat':
                try:
                    parent = issue['fields']['customfield_12313140']
                    inwardIssue = issue_key
                    outwardIssue = parent
                    linktype = 'Parent-Relation'
                    name = inwardIssue + "_" + outwardIssue

                    d['name'].append(name)
                    d['linktype'].append(linktype)
                    d['issue_id_1'].append(inwardIssue)
                    d['issue_id_2'].append(outwardIssue)
                except Exception:
                    logging.info("no parents")

                try:
                    feature = issue['fields']['customfield_12318341']
                    inwardIssue = issue_key
                    outwardIssue = feature
                    linktype = 'Feature-Relation'
                    name = inwardIssue + "_" + outwardIssue

                    d['name'].append(name)
                    d['linktype'].append(linktype)
                    d['issue_id_1'].append(inwardIssue)
                    d['issue_id_2'].append(outwardIssue)
                except Exception:
                    logging.info("no features")

            try:
                epic = issue['fields'][epiclinkfield_dict[project]]
                inwardIssue = issue_key
                outwardIssue = epic
                linktype = 'Epic-Relation'
                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)
            except Exception:
                logging.info("no epics")

            issuelinks = issue['fields']['issuelinks']

            for i in range(0, len(issuelinks)):
                issuelink = issuelinks[i]
                type = issuelink['type']
                linktype = type['name']
                try:
                    outwardIssue = issuelink['outwardIssue']['key']
                    inwardIssue = issue_key
                except Exception:
                    inwardIssue = issuelink['inwardIssue']['key']
                    outwardIssue = issue_key

                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)

                logging.info("SUCCESS")

            issuest = issue['fields']['subtasks']

            for i in range(0, len(issuest)):
                issuesubtask = issuest[i]
                linktype = 'Subtask'
                outwardIssue = issuesubtask['key']
                inwardIssue = issue_key

                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)

                logging.info("SUCCESS")
        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass
    logging.info(f'Creating csv.')
    df = pd.DataFrame.from_dict(d)
    filename = 'links_' + project.lower() + '.csv'
    df.to_csv(filename, sep=';',index=False)
    return None


if __name__ == '__main__':

    name = 'Hyperledger'
    extract_issue_csv(name)
    extract_links_csv(name)

    name = 'Jira'
    extract_issue_csv(name)
    extract_links_csv(name)

    name = 'MongoDB'
    extract_issue_csv(name)
    extract_links_csv(name)