from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename = "scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/j")
def hello_world():
    return "<h1>HELLO WORLD : )<h1>"

@app.route("/", methods=["GET"]) #now whenever we are going to hit, our homepage will going to hit our index.html file
def homepage():
    return render_template("index.html")

@app.route("/review", methods=["POST", "GET"])
def index(): #simply inside this function I have to write all of this respective logic
    if request.method == "POST":
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uclient = uReq(flipkart_url)
            flipkartpage = uclient.read()
            flipkart_html = bs(flipkartpage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class" : "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productlink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productlink) 
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all("div", {"class" : "_16PBlm"})

            filename = searchString + ".csv" # Inga new ah search pandra name la csv file create aagum, but andha file la namma edhum store pandra conditions eludhala.
        
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class' : '_2sc7ZR _ZVSEMM'})[0].text

                except:
                    name = "No Name"
                    logging.info("name")
                
                try:
                    #rating.encode(encoding='utf-8)
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = "No Rating"
                    logging.info("rating")

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = "No Comment Heading"
                    logging.info("commentHead")

                try:
                    contag = commentbox.div.div.find_all('div', {'class' : ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = contag[0].div.text

                except Exception as e:
                    logging.info(e)

                mydict = {"Product" : searchString, "Name" : name, "Rating" : rating, "commentHead" : commentHead,
                          "Comment" : custComment}
                reviews.append(mydict)
                logging.info("log my final result {}".format(reviews))

            return render_template("result.html", reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            logging.info(e)
            return "something is wrong"
        #return render_template('result.html')

    else:
        return render_template('index.html')








if __name__ == "__main__":
    app.run(host = "127.0.0.1", port="5000")