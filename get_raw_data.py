import requests
from datetime import datetime, timedelta
from flask import Flask
from model import db, FinancialData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

API_KEY = "QK0QXJNWRK1UI9P3"  # Replace with your AlphaVantage API key

def get_financial_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    response = requests.get(url)

    data = []
    if response.status_code == 200:
        raw_data = response.json()['Time Series (Daily)']
        for date_str in raw_data:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date >= datetime.today().date() - timedelta(weeks=2):
                record = {
                    'symbol': symbol,
                    'date': date,
                    'open_price': float(raw_data[date_str]['1. open']),
                    'close_price': float(raw_data[date_str]['4. close']),
                    'volume': int(raw_data[date_str]['6. volume'])
                }
                data.append(record)

    return data

def insert_financial_data(data):
    for record in data:
        existing_record = FinancialData.query.filter_by(symbol=record['symbol'], date=record['date']).first()
        if existing_record:
            existing_record.open_price = record['open_price']
            existing_record.close_price = record['close_price']
            existing_record.volume = record['volume']
        else:
            new_record = FinancialData(
                symbol=record['symbol'],
                date=record['date'],
                open_price=record['open_price'],
                close_price=record['close_price'],
                volume=record['volume']
            )
            db.session.add(new_record)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        symbols = ['IBM', 'AAPL']
        for symbol in symbols:
            data = get_financial_data(symbol)
            insert_financial_data(data)

        print(FinancialData.query.all())