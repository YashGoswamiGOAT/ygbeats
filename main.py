from flask import Flask
import json
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/getMusic/<name>")
def music(name):
    txt = requests.get("https://www.youtube.com/results?search_query=" + name).text
    soup = BeautifulSoup(txt, "lxml")

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


if __name__=="__main__":
    app.run(debug=True)