############# TASK TRACKER LOGIC ####################
import gspread
import threading
import base64
import os
import json
from flask import Blueprint, render_template, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials

task_tracker_bp = Blueprint('task_tracker', __name__)


# Your Google Sheets functions
def connect_to_sheets():
    """Connect to Google Sheets with credentials"""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    encoded = os.environ.get("CREDENTIAL_JSON_BASE64")

    if not encoded:
        raise ValueError("Missing credential JSON environment variable.")

    # Decode base64 to JSON string
    json_str = base64.b64decode(encoded).decode("utf-8")

    # Load JSON into dictionary
    credentials = json.loads(json_str)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    return client

def get_sheet_data(sheet_name, worksheet_name):
    """Get all data from a specific worksheet"""
    client = connect_to_sheets()
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet.get_all_values()

def print_sheet_data(all_rows, sheet_name):
    """Print all rows from sheet"""
    print(f"All rows from {sheet_name}:")
    for i, row in enumerate(all_rows):
        print(f"Row {i+1}: {row}")

# Example usage with different timeout methods
def run_with_timeout(func, args=(), kwargs=None, timeout_seconds=10):
    """
    Run a function with a timeout using threading
    """
    if kwargs is None:
        kwargs = {}
    
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        print(f"Function timed out after {timeout_seconds} seconds")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

###########################################################

@task_tracker_bp.route('/tracker', strict_slashes=False, methods=["GET", "POST"])
def tracker():
    """ Endpoint to render the tracker page """
    if request.method == "POST":
        # Define the scope and credentials
        tasks_info = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Automated Tracker'),
        timeout_seconds=15
        )
        
        tasks_headers = tasks_info[0]
        tasks_rows = tasks_info[1:]

        list_of_tasks = []

        for row in tasks_rows:
            row_dict = dict(zip(tasks_headers, row))
            list_of_tasks.append(row_dict)

        
        username_email_mapping = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Username-email mapping'),
        timeout_seconds=15
        )
        
        username_email_mapping_headers = username_email_mapping[0]
        username_email_mapping_rows = username_email_mapping[1:]

        list_of_usernames = []

        for row in username_email_mapping_rows:
            row_dict = dict(zip(username_email_mapping_headers, row))
            list_of_usernames.append(row_dict)

        team_structure = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Team Structure'),
        timeout_seconds=15
        )
        
        team_headers = team_structure[0]
        team_rows = team_structure[1:]

        list_of_teams = []

        for row in team_rows:
            row_dict = dict(zip(team_headers, row))
            list_of_teams.append(row_dict)
        return jsonify({
            'status': 'success',
            'tasks_info': list_of_tasks,
            'username_email_mapping': list_of_usernames,
            'team_structure': list_of_teams
        }), 200
        
    return render_template('task_tracker.html')
