# WikipediaWordList
A simple tool to create a sorted list of most common words out of a set of pages picked randomly from Wikipedia.

## Dependencies
In order to use this, you'll need the [wikipedia Pyhton library](https://pypi.org/project/wikipedia/), installable with:

    pip install wikipedia

## Usage
Run the script with:

    wwl.py [OPTIONS]

### Options
- `-h, --help` Shows the help message.
- `-p, --pages` Sets the number of pages to process (default `100`).
- `-l, --lang` Sets the language of the pages to retrieve (default `en`).
- `-s, --special` Sets the special chars to use as splitters (the space is always used, default `\\!\"/()[]{}=?\'<>,;.:-—_+*@#«»`).
- `-m, --min` Sets the minimum length of the words to process (default `1`).
- `-M, --max` Sets the maximum length of the words to process (`0` for infinity, default `0`).
- `-t, --threads` Sets the maximum amount of threads working simultanously to retrieve pages (default `1`).
- `-T, --timeout` Sets the maximum time to wait for the threads to retrieve the pages once the last thread started (`0` for infinity, default `30`).
- `-o, --output` Specifies the output file location (default `output.txt`).
- `-w, --words` Specifies the maximum number of words to save (`0` for infinity, default `0`).
- `-d, --debug` Shows debug level logs.

### Example

    wwl.py -p 1000 -l it -m 8 -t 50 -w 100

Saves 100 most common words of 8 or more characters out of 1000 italian pages using 50 threads.

# License
**WikipediaWordList** is released under the *Apache License 2.0*.
