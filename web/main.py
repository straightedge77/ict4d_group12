from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL


def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'ict_user'
    app.config['MYSQL_PASSWORD'] = 'ict4d'
    app.config['MYSQL_DB'] = 'ict'
    return app

app = create_app()
mysql = MySQL(app)

# stats page are used to display the database information, also need to login to access
@app.route('/')
def sell():
    cursor = mysql.connection.cursor()
    # get all records from the database
    cursor.execute("SELECT * FROM sell_list")
    db_sells = cursor.fetchall()
    cursor.close()

    # reflect in the html page
    return render_template('sell.html', sells=db_sells)

# edit the record, to edit it, user need to login
@app.route('/sell/<int:id>/edit/', methods=["GET"])
def sell_edit(id):
    return render_template('sell_edit.html')

@app.route('/sell/<int:id>/edit/', methods=["POST"])
def sell_change(id):
    cursor = mysql.connection.cursor()
    # in the edit page
    # get the url from the text line
    new_seed = request.form['seed']
    # check whether the new url satisfies the need
    if not new_seed:
        flash('New seed is required!')
        return redirect(url_for('sell_edit', id=id))
    # update the database
    new_weight = request.form['weight']
    if not new_weight:
        flash('New weight is required!')
        return redirect(url_for('sell_edit', id=id))
    new_price = request.form['price']
    if not new_price:
        flash('New price is required!')
        return redirect(url_for('sell_edit', id=id))
    cursor.execute('UPDATE sell_list SET seed = %s, weight = %s, price = %s WHERE id = %s', (new_seed, new_weight, new_price, id))
    mysql.connection.commit()
    cursor.close()
    # redirect to the stats page
    return redirect(url_for('sell'))

# if want to delete a record from the database
@app.route('/sell/<int:id>/delete/', methods=('POST',))
def sell_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM sell_list WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('sell'))

# if want to clear all records from the database
@app.route('/sell/clear/', methods=('POST',))
def sell_clear():
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM sell_list')
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('sell'))

# stats page are used to display the database information, also need to login to access
@app.route('/exchange')
def exchange():
    cursor = mysql.connection.cursor()
    # get all records from the database
    cursor.execute("SELECT * FROM exchange_list")
    db_exchanges = cursor.fetchall()
    cursor.close()

    # reflect in the html page
    return render_template('exchange.html', exchanges=db_exchanges)

# edit the record, to edit it, user need to login
@app.route('/exchange/<int:id>/edit/', methods=["GET"])
def exchange_edit(id):
    return render_template('exchange_edit.html')

@app.route('/exchange/<int:id>/edit/', methods=["POST"])
def exchange_change(id):
    cursor = mysql.connection.cursor()
    # in the edit page
    # get the url from the text line
    new_seed1 = request.form['seed1']
    # check whether the new url satisfies the need
    if not new_seed1:
        flash('New seed1 is required!')
        return redirect(url_for('exchange_edit', id=id))
    # update the database
    new_seed2 = request.form['seed2']
    if not new_seed2:
        flash('New seed2 is required!')
        return redirect(url_for('exchange_edit', id=id))
    cursor.execute('UPDATE exchange_list SET seed1 = %s, seed2 = %s WHERE id = %s', (new_seed1, new_seed2, id))
    mysql.connection.commit()
    cursor.close()
    # redirect to the stats page
    return redirect(url_for('exchange'))

# if want to delete a record from the database
@app.route('/exchange/<int:id>/delete/', methods=('POST',))
def exchange_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM exchange_list WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('exchange'))

# if want to clear all records from the database
@app.route('/exchange/clear/', methods=('POST',))
def exchange_clear():
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM exchange_list')
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('exchange'))

# stats page are used to display the database information, also need to login to access
@app.route('/report')
def report():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM report_list")
    # get all records from the database
    db_reports = cursor.fetchall()
    cursor.close()

    # reflect in the html page
    return render_template('report.html', reports=db_reports)

# edit the record, to edit it, user need to login
@app.route('/report/<int:id>/edit/', methods=["GET"])
def report_edit(id):
    return render_template('report_edit.html')

@app.route('/report/<int:id>/edit/', methods=["POST"])
def report_change(id):
    cursor = mysql.connection.cursor()
    # in the edit page
    # get the url from the text line
    new_seed = request.form['seed']
    # check whether the new url satisfies the need
    if not new_seed:
        flash('New seed is required!')
        return redirect(url_for('report_edit', id=id))
    # update the database
    new_weight = request.form['weight']
    if not new_weight:
        flash('New weight is required!')
        return redirect(url_for('report_edit', id=id))
    new_price = request.form['price']
    if not new_price:
        flash('New price is required!')
        return redirect(url_for('report_edit', id=id))
    cursor.execute('UPDATE report_list SET seed = %s, weight = %s, price = %s WHERE id = %s', (new_seed, new_weight, new_price, id))
    mysql.connection.commit()
    cursor.close()
    # redirect to the stats page
    return redirect(url_for('report'))

# if want to delete a record from the database
@app.route('/report/<int:id>/delete/', methods=('POST',))
def report_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM report_list WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('report'))

# if want to clear all records from the database
@app.route('/report/clear/', methods=('POST',))
def report_clear():
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM report_list')
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('report'))
