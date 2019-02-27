The `gists.py` script takes github username and checks for new published public gist. First time you run the script, it will register the new user and then will check for new gists on following executions.

Requirements:
1. You will need `Python 2.7.x` or `Python 3.4` or higher.
2. Make sure `pip` or `pip3` is installed.
3. Install the dependencies with pip or pip3. So run the following command: `pip install -r requirements.txt.`

To run the script, you will need to provide the github username as an option:
 `python gists.py -user github_username`. Example: `python gists.py -user charlie`
