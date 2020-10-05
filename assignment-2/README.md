Multi-threaded file server
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

Open multiple terminal and from them try the following commands:

    $ python3 client.py upload file1.txt
    $ python3 client.py rename file1.txt file2.txt
    $ python3 client.py download file2.txt
    $ python3 client.py delete file2.txt

In windows, simply use the command python instead of python3.
The file that are being used should be in the same directory as the script files.
The uploaded files will be in the `uploads/` directory, and the downloaded
files will be in the `downloads/` directory.
