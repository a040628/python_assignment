from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import db, FinancialData
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db.init_app(app)

@app.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')
        limit = int(request.args.get('limit', 5))
        page = int(request.args.get('page', 1))

        # Query all financial data with optional filters
        query = FinancialData.query
        if start_date:
            query = query.filter(FinancialData.date >= start_date)
        if end_date:
            query = query.filter(FinancialData.date <= end_date)
        if symbol:
            query = query.filter(FinancialData.symbol == symbol)
        
        query = query.order_by(FinancialData.date)
        
        # Pagination
        total_count = query.count()
        total_pages = math.ceil(total_count / limit)
        data = query.paginate(page=page, per_page=limit)
        
        # Format response
        response_data = [{
            'symbol': item.symbol,
            'date': item.date.strftime('%Y-%m-%d'),
            'open_price': str(item.open_price),
            'close_price': str(item.close_price),
            'volume': str(item.volume)
        } for item in data.items]
        response_pagination = {
            'count': total_count,
            'page': page,
            'limit': limit,
            'pages': total_pages
        }
        response_info = {'error': ''}
        response = {'data': response_data, 'pagination': response_pagination, 'info': response_info}
        return jsonify(response)
    except Exception as e:
        response_data = []
        response_pagination = {'count': 0, 'page': 0, 'limit': 0, 'pages': 0}
        response_info = {'error': str(e)}
        response = {'data': response_data, 'pagination': response_pagination, 'info': response_info}
        return jsonify(response)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        # Parse input parameters
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
        symbols = request.args.getlist('symbol')
        
        # Validate input parameters
        if start_date > end_date:
            raise ValueError('Start date must be before end date.')
        if not symbols:
            raise ValueError('At least one symbol must be provided.')
        
        # Query the database for the relevant data
        query = db.session.query(
            db.func.avg(FinancialData.open_price).label('avg_open_price'),
            db.func.avg(FinancialData.close_price).label('avg_close_price'),
            db.func.avg(FinancialData.volume).label('avg_volume')
        ).filter(
            FinancialData.symbol.in_(symbols),
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).first()
        
        # Prepare the response
        response_data = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'symbols': symbols,
            'average_daily_open_price': round(query.avg_open_price, 2),
            'average_daily_close_price': round(query.avg_close_price, 2),
            'average_daily_volume': int(round(query.avg_volume))
        }
        response_info = {'error': ''}
        response_status = 200
    
    except Exception as e:
        response_data = {}
        response_info = {'error': str(e)}
        response_status = 400
    
    return jsonify({'data': response_data, 'info': response_info}), response_status

if __name__ == "__main__":
    app.run(port=5000, debug=True)