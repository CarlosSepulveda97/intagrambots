import requests

class Downloader:
    fileName = ""
    url = ""

    def download(self, url):
        self.url = url
        self.fileName = "go.jpg"
        imagen = requests.get(self.url).content
        with open(self.fileName, 'wb') as handler:
            handler.write(imagen)