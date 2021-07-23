Wrote a multi-thread web server, capable of serving multiple requests in parallel. 

- A webpage index.html is stored on our server (assuming it is localhost).
- A process will be running on the server and listening to the specified port. We
assume it is 8080.
- In your web browser, if you type in http://localhost:8080/index.html, your web
server process shall fetch the index.html from the file system, compose the http
response, and send it back to the browser.
- 200, 301, 404 Status Codes are implemented as well.
