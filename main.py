from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def getTaskListIDByName(taskListName: str, service):
    all_task_lists = service.tasklists().list().execute()

    if not all_task_lists['items']:
        print("Nothing found")
    else:
        for task_list in all_task_lists['items']:
            if task_list['title'] == taskListName:
                return task_list['id']


def checkCMDArgs():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        task_list_name_param = input("Please enter the name of the task list: ")
        return task_list_name_param
         

def main():
    task_list_name_param = checkCMDArgs()

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('tasks', 'v1', credentials=creds) 

    task_list_name = getTaskListIDByName(task_list_name_param, service)

    tasks = service.tasks().list(tasklist=task_list_name).execute()

    for task in tasks['items']:
        print(task['title'])

if __name__ == "__main__":
    main()
    
