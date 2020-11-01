#! python3
# api.py - Upload, store and retrieve values from XML documents

# Import required modules: handle HTTP, parse XML, etc
from flask import Flask, request
from lxml import etree
from json import dumps
from time import time
import sys
import os

# Set up Flask app for handling client requests
app = Flask(__name__)

# Turn on debugging messages if desired
# app.config["DEBUG"] = True

# Avoid client crashing server by uploading overlarge file (>1MB)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

# Set (and create if required) directory in which uploaded files will be stored 
# Get the directory in which this script is running: in most cases sys.path[0] will suffice
storage_dir = os.path.join(sys.path[0], "storage")
if not os.path.isdir(storage_dir):
    os.makedirs(storage_dir)

# String constant for valid file root tag
TEST_ROOT = "test-root"
# String constant for Identifier tag
TEST_ID = "test-identifier"


# Check that file is valid XML with correct root
def validate_file(user_file):
    # Attempt to parse XML file and create file tree
    try:
        file_tree = etree.parse(user_file)
    except etree.XMLSyntaxError as err:
        # Trap parsing error and return to caller
        return False, err.msg
    # Check that file root is "test-root"
    file_root = file_tree.getroot()
    if file_root.tag == TEST_ROOT:
        return True, ""
    else:
        error_msg = "Document root is {0} instead of {1}".format(file_root.tag, TEST_ROOT)
        return False, error_msg


# Extract Identifiers from file at specified path
def get_identifiers(file_path):
    # Parse XML file and create file tree
    # We do not expect parsing to fail as file was validated on upload
    file_tree = etree.parse(file_path)
    # Extract all Identifier values to list
    id_list = []
    for element in file_tree.iter(TEST_ID):
        # Get value of element with Identifier tag
        id_list.append(element.text)
    # Convert list to JSON before returning
    return dumps(id_list)


# Create HTTP response with suitable attributes
def create_response(status_code, response_text):
    # Set up standard (JSON) Flask response from supplied arguments
    response = app.response_class(
        response=response_text,
        status=status_code,
        mimetype="application/json"
    )
    # Allow requests from all origins, for ease of testing
    # (not recommended in production as this is weak security)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response 


# Route for receiving uploaded documents
@app.route("/testapp", methods=["POST"])
def receive_doc():
    # Retrieve file uploaded by user
    user_file = request.files.get("uploadedfile")
    # Check that client submitted a file
    if user_file is None:
        # Fast-fail and return error
        return create_response(400, "No file selected")
    # Check that file format is valid
    file_valid, error_msg = validate_file(user_file)
    if file_valid:
        # Save file in storage directory, under unique ID
        # Get UID from timestamp: suitable for all but very busy servers
        file_uid = str(time())
        file_path = os.path.join(storage_dir, file_uid + ".xml")
        user_file.save(file_path)
        # Return success response containing UID
        return create_response(200, file_uid)
    else:
        # Return failure response containing error message
        return create_response(400, error_msg)


# Route for supplying Identifier values for document
@app.route("/testapp/identifiers", methods=["GET"])
def supply_values():
    # Extract document UID from client request
    file_uid = request.args.get("uid")
    if file_uid is None:
        # Fast-fail and return error
        return create_response(400, "No UID supplied")
    # Construct document file path from UID
    file_path = os.path.join(storage_dir, str(file_uid) + ".xml")
    # Check file exists for requested UID
    if os.path.isfile(file_path):
        # Extract Identifier values
        id_list = get_identifiers(file_path)
        # Return success response containing extracted values
        return create_response(200, id_list)
    else:
        # Return failure response containing error message
        return create_response(400, "File not found for UID {0}".format(file_uid))


# Launch server on starting script
if __name__ == "__main__":
    app.run()