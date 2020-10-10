Simple single-threaded file server
==================================


Project team members
--------------------

- Manish Munikar
- Hamza Reza Pavel


Requirements
------------

- Python >= 3.6


Usage
-----

First start the server in a terminal:

    $ python3 server.py

Then, in another terminal, run the client:

    $ python3 client.py upload file1.txt
    $ python3 client.py rename file1.txt file2.txt
    $ python3 client.py download file2.txt
    $ python3 client.py delete file2.txt

The file to upload used should be in the same directory as the script files.
The uploaded files will be in the `uploads/` directory, and the downloaded
files will be in the `downloads/` directory.
