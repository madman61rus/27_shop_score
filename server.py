from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime

app = Flask(__name__)
engine = create_engine('postgresql://score:Rysherat2@shopscore.devman.org/shop')
session = Session(engine)
automap = automap_base()
automap.prepare(engine,reflect=True)
Order = automap.classes.orders

@app.route('/')
def score():
    print (session.query(Order).filter(Order.confirmed.is_(None)) \
        .order_by(Order.created.asc()).first())
    return render_template('score.html')

@app.route('/get_score',methods=['POST'])
def get_score():
    now = datetime.datetime.now()
    tomorow = now.utcnow().date()
    orders_not_confirmed = session.query(Order).filter(Order.confirmed.is_(None)).order_by(Order.created.asc()).first()
    timedelta = round((now - orders_not_confirmed.created).total_seconds()/60)
    count_today = session.query(Order).filter( Order.created >= now.utcnow().date()).count()
    count_not_confirmed = session.query(Order).filter(Order.confirmed.is_(None)).count()
    count_not_confirmed_today = session.query(Order).filter( Order.created >= now.utcnow().date(),
                                                             Order.confirmed.is_(None)).count()

    return jsonify(score = timedelta ,
                   count_today = count_today,
                   count_not_confirmed = count_not_confirmed,
                   count_not_confirmed_today=count_not_confirmed_today)



if __name__ == "__main__":
    app.run()
