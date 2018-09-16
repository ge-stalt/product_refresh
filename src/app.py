from flask import Flask
from string import Template
import requests

app = Flask(__name__)
print("started application with app name: ", __name__)

HTML_TEMPLATE = Template("""
<h1>Hello ${place_name}!</h1>

<img src="https://maps.googleapis.com/maps/api/staticmap?size=700x300&markers=${place_name}" alt="map of ${place_name}">

<img src="https://maps.googleapis.com/maps/api/streetview?size=700x300&location=${place_name}" alt="street view of ${place_name}">
""")

@app.route('/')
def homepage():
    return """
    <!DOCTYPE html>
    <head>
        <title>My title</title>
        <link rel="stylesheet" href="http://stash.compjour.org/assets/css/foundation.css">
    </head>
    <body style="width: 880px; margin: auto;">  
        <h1>Visible stuff goes here</h1>
        <p>here's a paragraph, fwiw</p>
        <p>And here's an image:</p>
        <a href="https://www.flickr.com/photos/zokuga/14615349406/">
            <img src="http://stash.compjour.org/assets/images/sunset.jpg" alt="it's a nice sunset">
        </a>

        <p>Locations:</p>
        <a href="/places/newyork">new york</a><br/>
        <a href="/places/stanford">stanford</a><br/>
        <a href="/places/tokyo">tokyo</a><br/>

        <p>
            <iframe src="https://player.vimeo.com/video/105955605" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
            <p>
                <a href="https://vimeo.com/105955605">Mary live-codes a JavaScript game from scratch &ndash; Mary Rose Cook at Front-Trends 2014
                </a> from 
                <a href="https://vimeo.com/fronttrends">Front-Trends</a> on <a href="https://vimeo.com">Vimeo</a>.
            </p>

        </p>
    </body>
    """

@app.route('/videos/<vid>')
def videos(vid):
    youtube_url = 'https://www.youtube.com/watch?v={video_id}'.format(video_id=id)
    vidtemplate = Template("""
      <h2>
        YouTube video link: 
        <a href="https://www.youtube.com/watch?v=${youtube_id}">
          ${youtube_id}
        </a>
      </h2>
    
      <iframe src="https://www.youtube.com/embed/${youtube_id}" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    """)
    return vidtemplate.substitute(youtube_id=vid)


@app.route('/places/<place>')
def place(place):
    return(HTML_TEMPLATE.substitute(place_name=place))

@app.route('/weather/<weather>')
def weather(weather):
    return("I don't know what the weather is in {name}".format(name=weather))

@app.route('/what')
def homepage():
    return "Whatever", 404


if (__name__ == '__main__'):
    print("starting app")
    app.run(debug=True, use_reloader=True)
    print("app started")