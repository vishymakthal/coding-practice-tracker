from dotenv import load_dotenv
import datetime
import pickle
import os
import GoogleSuite
import time

def create_reminder_event(tasks, task_list, subject):
    body = {
        'status': 'needsAction',
        'title' : subject,
        'due' : datetime.datetime.utcnow().isoformat('T')  + 'Z'

    }
    created_event = tasks.tasks().insert(tasklist=task_list['id'],body=body).execute()
    print("Reminder created! ", created_event['id'], "->", subject)

def main():

    # Load environment vars
    load_dotenv()    

    sheet_list = os.getenv('PROBLEM_SHEETS').split(',')

    sheet = GoogleSuite.get_sheets_service()
    tasks = GoogleSuite.get_tasks_service()

    for ps in sheet_list:
        result = sheet.values().get(
            spreadsheetId=os.getenv("SHEET_ID"), range='{}!A2:H'.format(ps)).execute()

        review_items_sheet = result['values']
        
        task_list = tasks.tasklists().list().execute()['items'][0]

        # 1. Create empty due item list
        items_due = []

        # 2. Grab the current date in MM/DD format
        today = datetime.datetime.now()
        current_date = '{}/{}'.format(today.month,today.day)

        # 3. Create for loop
        for item in review_items_sheet:

            # 4. Check if the item is due for review Today
            if current_date in item:

                # 5. Construct a review item string and append to the items list
                item_str = ' - '.join(item[0:3])
                items_due.append(item_str)
                create_reminder_event(tasks, task_list, item_str)
                time.sleep(0.1)

        print('Items due: ', items_due)
    
if __name__ == '__main__':
    main()