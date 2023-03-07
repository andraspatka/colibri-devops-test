# Notes about the proposed solution

- The version information from the scripts was extracted using a regex. Since there isn't always a '.' delimiter, a simple 'split' method can not be used. The proposed regex looks like this: `'0?(\d+)'`:
  - The first 0 is optional. It's specified so that if it's there it doesn't enter into the capturing group.
  - The capturing group captures one or more digits.
- I had some issues with running the containers on an M1 mac (it couldn't install the powershell apt package). Adding the `platform: linux/amd64` explicitly to docker-compose solved it. I assume that the powershell package is maybe not compiled for arm64 yet.
- I added some checks to ensure that the DB is up before running the scripts.
- I used the python context manager for the DB connection, so that there is no need to manually add "commit" and the "rollback" is done automatically if something goes wrong.
- There is an optional '-d' flag, which turns on the debug log level.
- I added the `WORKDIR /submissionscript` line to `Dockerfile.exec` for convenience.
- Running the script: `python3 migrate_db.py /scripts/ dev mysql_container devopstt 123456 -d`
