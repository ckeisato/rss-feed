from rss_reader import app
import os

port = int(os.environ.get('PORT', 5000))
app.run(debug=True, port=port)