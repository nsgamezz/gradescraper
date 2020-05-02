import requests
from lxml import html
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)
#USERNAME = "rajasgan3603"
#PASSWORD = "Apple7877tond"

LOGIN_URL = "https://ipe-hac.eschoolplus.powerschool.com/HomeAccess/Account/LogOn"
URL = "https://ipe-hac.eschoolplus.powerschool.com/HomeAccess/Home/WeekView"


@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html', title='Home')

@app.route("/grades", methods=['POST'])
def grades():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)

    USERNAME = request.form['username']
    PASSWORD = request.form['password']

    # Create payload
    payload = {
        'SCKTY00328510CustomEnabled': 'False',
        'Database': '10',
        'LogOnDetails.UserName': USERNAME,
        'tempUN': '',
        'tempPW': '',
        'LogOnDetails.Password': PASSWORD,
        'login': '',
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    soup = BeautifulSoup(result.text, "html.parser")

    classes_info = {}
    finalMessage = ''

    classNames = soup.find_all('a', {"class": "sg-font-larger"})
    classAverages = soup.find_all('a', {"class":"sg-font-larger-average"})

    for x in range(0, len(classNames)):
        finalMessage = finalMessage+str(classNames[x].text)+" "+str(classAverages[x].text)
    
    return render_template('grades.html', title='Grades', classNames=classNames, classAverages=classAverages, length=len(classNames))
   
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
