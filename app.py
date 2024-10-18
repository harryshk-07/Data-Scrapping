from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from db import collection
from scraper import scrape_website
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)

# Scheduler to update the website every 5 minutes
def scheduled_scraping_job():
    scraped_data = scrape_website()
    
    if scraped_data:
        # Clear the collection and update with new data
        collection.delete_many({})
        collection.insert_many(scraped_data)
        print(f"Data updated at {datetime.now()}")

# Start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_scraping_job, 'interval', minutes=5)
scheduler.start()

@app.route('/data', methods=['GET'])
def get_data():
    data = collection.find()
    return dumps(data), 200

@app.route('/scrape', methods=['GET'])
def scrape_now():
    try:
        # Manually trigger a scrape and update the database
        scraped_data = scrape_website()

        if scraped_data:
            collection.delete_many({})  # Clear the collection
            collection.insert_many(scraped_data)  # Insert new data
            return jsonify({"message": "Data scraped and updated."}), 200
        else:
            return jsonify({"error": "Failed to scrape the website: No data returned"}), 500
    except Exception as e:
        print(f"Error while scraping: {e}")
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
