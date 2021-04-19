from flask import Flask, render_template, redirect, url_for, request,request, jsonify
from datetime import datetime, timedelta
from similarity_v1 import assess_answer

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')

def func():
   info = assess_answer('I am a good Boy.The car is awesome','I am a bad Boy. I have a BMW.',5)
   print(info)
   return jsonify(info)
#    render_template('display.html', info=info['data'])
#    return res

app.run()
# if __name__ == "__main__":
#      app.debug = False
#      port = int(os.environ.get('PORT', 33507))
#      waitress.serve(app, port=port)
#      app.run()
