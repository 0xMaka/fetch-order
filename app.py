from flask import Flask, render_template
import requests 
import random

from forms import FetchOrder
from config import get_secret
from fetch_order import fetch_and_index

app = Flask(__name__)
app.secret_key = get_secret('SECRET')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = FetchOrder()
  if form.validate_on_submit():
    totals, pending, other = fetch_and_index(
      form.address.data,  
      int(form.chainId.data)
    )
    heading = ' '
    return render_template(
      'response.html', 
      heading=heading, 
      totals=totals,
      pending=pending,
      other=other,
      form=form
    )
  heading = ' '
  quote = 'Returns pending and historical orders for a user if any.'
  return render_template(
    'base.html', 
    heading=heading, 
    quote=quote,
    form=form
  )
