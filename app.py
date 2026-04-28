from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/notams')
def get_notams():
    station = request.args.get('station', 'MMMX')
    stations = station.split(',')
    url = "https://notams.aim.faa.gov/notamSearch/search"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    results = []
    for s in stations:
        data = {"retrieveLocId": s, "actionType": "notamRetrievalByICAOs", "reportType": "RAW"}
        try:
            r = requests.post(url, data=data, headers=headers, timeout=10)
            results.append("=== " + s + " ===")
            results.append(r.text[:2000])
        except:
            results.append("=== " + s + " - NO DATA ===")
    return "\n".join(results)

if __name__ == '__main__':
    app.run()
