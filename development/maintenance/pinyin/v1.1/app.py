from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route('/')
def home():
    rss_feed = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
    articles = []
    for entry in rss_feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'media_content': entry.get('media_content', []),
            'media_thumbnail': entry.get('media_thumbnail', []),
        }
        print(f"Article: {article['title']}")
        print(f"Media Content: {article['media_content']}")
        print(f"Media Thumbnail: {article['media_thumbnail']}")
        articles.append(article)
    return render_template('index.html', articles=articles)

@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/subscribe', methods=['POST'])
def process_subscription():
    name = request.form['name']
    email = request.form['email']
    plan = request.form['plan']
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']
    conn = None
    try:
        # Store the information in the SQLite database
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO subscribers (name, email, plan, card_number, expiry_date, cvv)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, plan, card_number, expiry_date, cvv))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10002)
