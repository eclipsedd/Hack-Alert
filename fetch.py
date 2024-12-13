import requests


def loader(url, path):
    r = requests.get(url)
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)


# url = "https://www.hackerearth.com/challenges/?filters=competitive%2Chackathon%2Cuniversity"
# path = "data.html"

# loader(url, path)
