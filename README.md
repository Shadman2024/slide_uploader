it just automates the slide upload from my desktop to google slides , well ,
I dont use powerpoint because I am a linux user and 
since the slides were created using either google slides or powerpoint
 so the slides feels a bit bloated when opened on libre office ,
 and uploading to google slides feels a lot of work

Here is the thing , to run this you need to do a lot of work 
Go to Google Cloud Console(https://console.cloud.google.com/), create a project.
Enable the Google Drive API for that project.
Under APIs & Services -> Credentials, create an OAuth client ID of type Desktop app. Download the JSON and save it next to your script as credentials.json.
Under OAuth consent screen, add your Google account as a test user (otherwise Google blocks the login).
Install the libraries(after creating a python environment ,say google_libraries then activate it):
pip install google-auth google-auth-oauthlib google-api-python-client


finally you are good to go 

