# Wellcome vision assistant

## Installation

You need Python and pip installed in your computer to follow the instructions

- `pip install -r requirements.txt`
- install tesseract by following the instructions [here](https://github.com/tesseract-ocr/tesseract)
- authenticate with google vision api by following the instructions [here](https://cloud.google.com/vision/docs/quickstart-client-libraries)

*Note that Google vision API requires a credit card but the first 1000 requests to the API are free and the next 1000 are 1.50$ in the unlikely scenario that you become addicted to this software.*

## Running the vision assistant

The vision assistant app is built using flask. Flask and the project needs some additional configuration before you are ready to go

- get a github oauth token by following these instructions [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
- initiate the following flask and github environment variables
```bash
export FLASK_APP=app/application.py
export GITHUB_USER=xxx
export GITHUB_REPO=xxx
export GITHUB_OAUTH_TOKEN=xxx
#export FLASK_ENV=development`
```
## Using the vision assistant

There are two functionalities offered by the assistant at the moment

### Mosaic scanner
Mosaic scanner endpoint `/`

Mosaic scanner allows you to find a mosaic artible in the web given a picture of a mosaic poster. Example pictures in data/mosaic

### Postit scanner
Postit scanner endpoint `/postit`

Postit scanner allows you to close github issues that are references in a picture of postits and have a reference to the github issue somewhere in the text, in the form of #issue_number. Example picture in data/postit

## Vision assistant in your phone
Vision assistant is also available in a web app so you can use it in your phone. At the moment the asistant functionalities are deployed in separate urls but in the future they will be part of the same app.

[Mosaic scanner](http://mosaic-env.ukymj23amx.us-east-2.elasticbeanstalk.com/)

[Postit scanner](http://postit-env.vrmmcmjm5h.us-east-2.elasticbeanstalk.com/)

## Notebooks
If you want to run the notebooks which were used during the development of this project you need to install some additional libraries by running `pip install -r notebooks/requirements.txt`
