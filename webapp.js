/*
webapp.js
Logic for calling document store API
*/

// Upload file to document store
function upload_file()
{
    // Set up endpoint and method
    var endpoint = "/testapp";
    var method = "POST";

    // Set up HTTP request with specified parameters
    http_request = setup_request(method, endpoint);

    // Set up callbacks for server responses
    http_request.onload = function() {
        if (http_request.status === 200) {
            // Success: pass UID returned from server to worker
            retrieve_ids(http_request.response);
        }
        else {
            // Failure: display error returned from server
            document.getElementById("result").innerHTML = "Error: " + http_request.response;
        }
    }

    // Retrieve user's uploaded file from web page
    var uploaded_file = document.getElementById("upload").files[0];
    let request_body = new FormData();
    request_body.append("uploadedfile", uploaded_file);

    // Send request with file in body
    http_request.send(request_body);
}

// Retrieve Identifiers for document with specified UID
function retrieve_ids(file_uid){
    // Set up endpoint and method
    var endpoint = "/testapp/identifiers";
    var method = "GET";

    // Set up HTTP request with specified parameters
    // Supply UID as query parameter
    http_request = setup_request(method, endpoint + "?uid=" + file_uid);

    // Set up callbacks for server responses
    http_request.onload = function() {
        if (http_request.status === 200) {
            // Success: server should have returned requested values
            user_text = "Success: found Identifiers " + http_request.response;
        }
        else {
            // Failure: display error returned from server
            user_text = "Failure: " + http_request.response;
        }
        // Display result of call to user
        document.getElementById("result").innerHTML = user_text;
    }

    // Send request (no body required)
    http_request.send();
}

// Worker function for common HTTP request setup
function setup_request(method, endpoint)
{
    // Route via local host (not suitable for production)
    var local_host = "http://127.0.0.1:5000";

    // Always send request asynchronously to avoid blocking client
    // (this is the default, but specify it for safety)
    var async = true;

    // Set up HTTP request with specified parameters
    let http_request = new XMLHttpRequest();
    http_request.open(method, local_host + endpoint, async);

    // Set up callback in case of network error
    http_request.onerror = function() {
        console.error(http_request.statusText);
    }

    return http_request;
}