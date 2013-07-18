from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from apiclient import errors



import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow


# Copy your credentials from the APIs Console
CLIENT_ID = '323604963886.apps.googleusercontent.com'
CLIENT_SECRET = 'PLyJMbGiWiN33Oxj4LmLzNXR'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'http://127.0.0.1:8000/drive/list'

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)


def index(request):
	authorize_url = flow.step1_get_authorize_url()
	return redirect(authorize_url)


def list(request):
	code = request.GET.get('code')

	credentials = flow.step2_exchange(code)
	# # Create an httplib2.Http object and authorize it with our credentials
	http = httplib2.Http()
	http = credentials.authorize(http)

	drive_service = build('drive', 'v2', http=http)

	result = []
	page_token = None
	http_result = []
	while True:
		try:
			param = {}
			if page_token:
				param['pageToken'] = page_token
			files = drive_service.files().list(**param).execute()

			result.extend(files['items'])
			for res in result:
				http_result.append(res['title'])
				http_result.append('  <a href=\'https://www.googleapis.com/drive/v2/files/{}\'>Link</a>'.format(str(res['id'])) )
				# http_result.append(str(res['id']))
				# http_result.append(res['webContentLink'])
				http_result.append('<br/>')
			page_token = files.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print 'An error occured: %s' % error
			break

	return HttpResponse(http_result)
	# return HttpResponse(result)





# code = raw_input('Enter verification code: ').strip()


# # # Insert a file
# # media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
# # body = {
# #   'title': 'My document',
# #   'description': 'A test document',
# #   'mimeType': 'text/plain'
# # }

# file = drive_service.files().insert(body=body, media_body=media_body).execute()
# pprint.pprint(file)