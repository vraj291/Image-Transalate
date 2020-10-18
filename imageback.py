from flask import Flask, render_template, request, redirect, url_for
from googletrans import Translator
import numpy as np
import pytesseract
from gtts import gTTS
from pytesseract import Output
from PIL import Image
import cv2

app = Flask(__name__)  
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
@app.route('/frontend')  
def upload():  
    return render_template("image.html")  
 
@app.route('/backend', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        img=cv2.imread(f.filename)
        new_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        new_img=cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        d=pytesseract.image_to_data(new_img, config=custom_config, output_type=Output.DICT)
        trans=Translator()
        text=" ".join(d["text"]).strip()
        lang=trans.detect(text).lang
        new_text=trans.translate(text,src=lang,dest="en").text
        speak = gTTS(text=new_text, lang="en", slow= False)  
        speak.save("static/captured_voice.mp3") 
        return render_template("success.html")  
  
if __name__ == '__main__':  
    app.run(debug = True)      