# full-stack-practice
Practice full-stack application.

How to run this software:

1) Open a terminal window in the root directory
  - Ensure this directory has write permissions enabled, as it will be used for storing uploaded files
2) Start the server by entering `python api.py` in the terminal window
  - Requires Python 3: if you have multiple Python versions installed, you may need to enter `python3 api.py` instead
  - TODO: requirements.txt
  - Runs on local host: confirm from terminal output that it is running on http://127.0.0.1:5000/
3) Start the client by opening the file webapp.html in your preferred browser
4) Click the "Browse" button in the web app to select a file
5) Click the "Upload file" button to upload the selected file
  - The result of the upload will be displayed in the web app, including all Identifiers found in the file if upload succeeded
