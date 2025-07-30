#standard library
import io

#image generator(pillow) and flask(domain creator) jsonify(makes it so you can use javascript commands in any other programming language file) send_file sends file to another application
from PIL import Image, ImageDraw
from flask import Flask, jsonify, send_file

#create the flask app
app = Flask(__name__) # make a instance(connect to the html file) to create the site for the flask app

