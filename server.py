from flask import Flask, render_template, jsonify, send_from_directory , request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime

app = Flask(__name__)
engine = create_engine('postgresql://score:Rysherat2@shopscore.devman.org/shop')
session = Session(engine)
automap = automap_base()
automap.prepare(engine,reflect=True)
order = automap.classes.orders

@app.route('/')
def score():
    return render_template('score.html')

@app.route('/get_score')
def get_score():
    timedelta = 0
    now = datetime.datetime.now()
    last_not_confirmed = session.query(order).filter_by(status = 'DRAFT').order_by(order.created.asc()).first()
    if last_not_confirmed:
        timedelta = round((now.utcnow() - last_not_confirmed.created.utcnow()).total_seconds()/60)
    count_today = session.query(order).filter(order.created >= now.utcnow().date()).count()
    count_not_confirmed = session.query(order).filter_by(status='DRAFT').count()

    return jsonify(score = timedelta ,
                   count_today = count_today,
                   count_not_confirmed = count_not_confirmed)


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory('', request.path[1:])


if __name__ == "__main__":
    app.run()


