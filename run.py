from rss_reader import app
from os import environ

app.run(debug=True, port=environ.get("PORT", 5000))
