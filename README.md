# full-stack-practice
Practice full-stack application. Allows user to browse for an XML file via the web client and upload it to the server. Server checks that the file is valid XML and the root node is named `test-root`. On successful upload, web client displays values of any `test-identifier` tags in the file; on failure, displays relevant error message.

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
