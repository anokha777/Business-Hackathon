# pip install lxml
from flask import Flask,render_template,url_for,request,jsonify
from urllib.parse import urlparse
import requests
import bs4

app = Flask(__name__)

@app.route('/scrap')
def home():
  url  = request.args.get('url', None)
  # get domain 
  parsed_uri = urlparse(url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
  print(domain)

  page = requests.get(url,  headers={'User-Agent': 'Mozilla/5.0'})
  soup = bs4.BeautifulSoup(page.content, 'html.parser')
  # https://www.dealerrater.com/directory/Nevada/Service-Center/CODA/
  if domain == 'https://www.dealerrater.com/':
    # rawReview = soup.select("p.review-content")
    rawReview = soup.select("p.review-snippet")
  elif domain == 'https://www.surecritic.com/':
    rawReview = soup.select("div.review-text")
  # https://www.autocarindia.com/car-reviews
  elif domain == 'https://www.autocarindia.com/':
    rawReview = soup.select("p.text-justify")
  # http://overdrive.in/reviews/cars/
  elif domain == 'http://overdrive.in/':
    rawReview = soup.select("a h3")
  # https://www.team-bhp.com/forum/official-new-car-reviews/?pp=25&sort=dateline&order=desc&daysprune=-1
  elif domain == 'https://www.team-bhp.com/':
    rawReview = soup.select("tbody tr td div a")

  # get actual text list form rawReview
  reviewTextList = []
  for review in rawReview:
    reviewTextList.append(review.text)

  # print(len(reviewTextList))
  return jsonify(
      rewiews = reviewTextList
  )

if __name__ == '__main__':
	app.run(debug=True)