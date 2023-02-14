from io import BytesIO

import firebase_admin
from firebase_admin import storage, credentials, db
from flask import Flask
import json
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)


# Fetch the service account key JSON file contents
cred = credentials.Certificate(
{
  "type": "service_account",
  "project_id": "yashwebsitebalaji",
  "private_key_id": "d030e1c3b3b2dea792cc451688b6d7fec5f32c29",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDqBaIfD3TvnIs1\nrW2pT1/IOGE2jrxHBysWovBf/hbaO2eXawrML1CdtQha++OYmTmQMc3JCWuDKGo6\n/8j/ve5H/fpdDyhxrl6hoL3+jAeXG0Jm/KPJ6oiIyhBrDiD/bqhes8r4wINaCPvc\nQGfpVScubPe8GLJtPHaa3Q4RuaUI+HAceK8QFIP0bd9fTwnIQhPneFt5XWZw8+j6\n023uXUKCosOD1DrkhnTKH+qF5NMNuxChY7GsBe4CU5y/hGFAT4+7Xu1UJrQJUo2z\nwrLJvWtoeXIISXuJJniaQRd1hJ7qSiEH/cdxL/dcVKNS6SoTzcCjiE/uN1tGCxwH\nUG9Ma7kzAgMBAAECggEAGtHpdMN/Oc9y5C8g5b9bMVBGJ+FaMjkKlvi2hrHRPv0s\nOp4XFIk0T9awWJ5h75pZOVgpMZSQS0LwUHGsa07Xm6LqX2GTgi/N2EUv8RfC7kOU\nARyMIuHA+GL8AwuRUY+GNqWb/z/aQzvLWEB+CC+XospJ5rcyil1cab7S1B+MCp0X\njAUkFApKxAAuLNkb5gly0w+T1SZQYqSGw17Jk5Za29CiokJqKqcwRiCdec4quyQs\n54G8/R2GlM0xLcMcB+LVqPj6QhAril9iZevqatpa7q5qpeV0uY/Us7XGRUm4cLDd\nMEE5bCB4mWKbXKUh3Q0xV+vQY69+N1nudYA/XAbzAQKBgQD99HR6ma7GhxP9MT4C\nZqdXj3zPvb55HvBHMb3p4H0OAFMPhyJeJnF3iP6mhkf1bZznhiDXIRUbakJQ3+sP\n6LPiaq4wqrk3lna1rApmIA7oSAWI6AmJTIIiKXUhLwyr6jGsmEXDcoegFXA7c9Nc\n6Ii+0Q06+vk6oCr+HMdOgXIeMwKBgQDr6BXVnJN29yBmflMsBy89O33b0S3/4XFu\ncm3ei8vRqMrhC088nPOVavR1Y5lqk0+h0Jbh69dguZR4Py8BUBpThvbxPaf86nZi\nIOW6SnVdva6ks+1OIfgf2oDxjXAIr8Kimt3XyX1xrhGx8dNwfPM/pZkX+l1VulaC\nPrjW1/75AQKBgB86f1RQL7DUDX42HvT2oJ9g0q1NHO4SAuQOVtc6tsYQ/iXLrUs8\nmPllDEN4AcNJbmD+Gm258LmFUJBXaLV1HSG7kp4DcHFIfGKMvF6glJS1vpB+UCXl\nFZ+Tz4Z8HafKTb92niWRoOHroPh+nsAvDBnC5UiacilmZsMG0O9zdZAHAoGBAJ7z\na/LYY0wfS0eECop59MxvT2hTU4k73/ApTfpLe3OzJa/orOUMY9vjiv+lsnNq+pbv\nMxrai+5yXKWA/S0HShXJtI3rm0sAt+96dw/Ep7wX2JrFWTnyDXt5ALTBNiHEO4LQ\nknWZH9r/DJE3fd4ncscJz1OmsEjZGvz7QhQQyY4BAoGASOGBXn4s5YjGXbEZtxbP\n/QZ3pDfUgZDk1YfV8obifhpvvE9k7d/cyN4zO8WzkL9+g6UDq6gP4f5Z9uv/zUgT\n7pZZa30QO+UHGDYoW7um4oSxqZmY8VQ8iN3yclo6TV+349Me4CtGoqT5FUHC7ZWH\ndwj4DpfAu+jVcvNwhjLg0No=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-76bl1@yashwebsitebalaji.iam.gserviceaccount.com",
  "client_id": "108511309136263506605",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-76bl1%40yashwebsitebalaji.iam.gserviceaccount.com"
}

)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yashwebsitebalaji-default-rtdb.firebaseio.com/',
    'storageBucket' : 'yashwebsitebalaji.appspot.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference()

bucket = storage.bucket()




@app.route("/getMusic/<name>")
def music(name):
    txt = requests.get("https://www.youtube.com/results?search_query=" + name).text
    soup = BeautifulSoup(txt, "html.parser")

    youtubedataobj = soup.find_all("script")[33].text.split("var ytInitialData = ")[1].split("};")[0] + "}"
    raw = (
    json.loads(youtubedataobj)["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"][
        "contents"][0]["itemSectionRenderer"]["contents"])
    videos = []
    # v[1].videoRenderer.navigationEndpoint.commandMetadata.webCommandMetadata.url
    for i in range(len(raw)):
        try:
            # v[4].videoRenderer.title.runs[0].text ---title
            # v[4].videoRenderer.thumbnail.thumbnails[v[4].videoRenderer.thumbnail.thumbnails.length-1] -- thumbnail
            videos.append(
                {
                    "title": raw[i]["videoRenderer"]["title"]["runs"][0]["text"],
                    "thumbnail": raw[i]["videoRenderer"]["thumbnail"]["thumbnails"][
                        len(raw[i]["videoRenderer"]["thumbnail"]["thumbnails"]) - 1],
                    "video": raw[i]["videoRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"][
                        "url"]
                }
            )
        except:
            pass

    return str(json.dumps(videos))


@app.route("/download/<url>")
def downloadMusic(url):
    YoutubeObject = YouTube("https://music.youtube.com/watch?v="+url)
    buffer = BytesIO()
    video = YoutubeObject.streams.get_audio_only()
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    bucket = storage.bucket()
    upload = bucket.blob(video.title+".mp4")
    upload.upload_from_file(buffer)
    upload.make_public()
    return upload.public_url

@app.route("/play/<url>")
def play(url):
    YoutubeObject = YouTube("https://music.youtube.com/watch?v="+url)
    video = YoutubeObject.streams.get_audio_only().url
    return video

if __name__=="__main__":
    app.run()