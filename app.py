from flask import Flask, render_template, request, jsonify
import stock_api

app = Flask(__name__)

# Render Index Homepage
@app.route('/')
def index():
    return render_template('index.html')


# Comparison page
@app.route('/compare')
def compare():
    return render_template('compare.html')


# End Point for getting net price for StashAway data based on from date
# URL will look like /getNetPrice?stockdate=YYYYMMDD
@app.route('/getNetPrice')
def get_Net_Price():
    dp = []
    if request.args:
        stockdate = int(request.args['stockdate'])
        dp = stock_api.getNetPrice('SA', stockdate)   
    dp['title'] = 'StashAway 14%'
    return jsonify(dp)


# Endpoint for getting stock and bond data based on date and percentage
# URL will look like /getStockBond?stock=20&bond=80&stockdate=YYYYMMDD
@app.route('/getStockBond')
def get_Stock_Bond_Data():
    dp = []
    if request.args:
        stock = int(request.args['stock'])
        bond = int(request.args['bond'])
        stockdate = int(request.args['stockdate'])
        dp = stock_api.getPerformance(stockdate, stock, bond)
    return jsonify(dp)


if __name__ == '__main__':
    app.run(debug=True)
