# github-new
## A Simple Way of Making a New Repository From the Command Line
**Current Version:** 1.0

**Last updated:** 6th June 2019

**Last tested version:** 1.0

### Important Notice
This program requires access to oauth/personal access tokens. The tokens are however stored in plaintext form in config.txt. Keep this security risk in mind before using it.

### Features:
* Cross-platform
* Easy installation
* Creating and Cloning feature built in
* Very lightweight 
* Easily readable code, approximately 100 lines

### Install/Uninstall:

#### Easy Installation:
1. Clone or download an archive of the repo.
2. Run the following command in the terminal:
```
python github-new.py -o TOKEN -s
```
**:warning: The token to be used by the program should be generated by going to [the Personal Access Tokens page on Github](https://github.com/settings/tokens)**.

3. (Windows only) Hereinafter, you may just run the gnew.bat file, however it auto-clones the created repo. Edit the batch file and remove the --local flag if you don't want to auto clone the repo.
