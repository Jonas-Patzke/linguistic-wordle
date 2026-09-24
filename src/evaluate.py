import gspread
from google.oauth2.service_account import Credentials
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory to find our txt

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "../data/credentials.json",
    scopes=scopes
)

client = gspread.authorize(creds)
sheet = client.open_by_url(
"https://docs.google.com/spreadsheets/d/1A2AqtIRgllnj0LVhDF0N7CrbK-haPZxRQNYx09a9gTQ/edit?gid=0#gid=0"
).sheet1

sheet.append_row(["test", 1, True, 60, "first test"])