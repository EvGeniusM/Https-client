import requests
r = requests.get('https://stackoverflow.com/questions/16523939/how-to-write-and-save-html-file-in-python')
print(r.content)