import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # get all businesses user has invested in
    symbols = db.execute("SELECT symbol FROM history WHERE id= :id GROUP BY symbol;", id=session['user_id'])

    # get current balance in account
    account_balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

    # grand total
    total = 0

    # history of user exists
    if len(symbols) != 0:

        # what will be sent to index.html
        stock_history = []

        for symbol in symbols:
            update_info = lookup(symbol['symbol'])
            num_shares = db.execute("SELECT SUM(shares) FROM history WHERE id= :id AND symbol = :symbol;",
                                    id=session['user_id'], symbol=update_info['symbol'])

            if num_shares[0]['SUM(shares)'] != 0:

                # in stock history, we will populate with dicts of stock_items for each type of business
                stock_item = {}

                stock_item['name'] = update_info['symbol']
                stock_item['symbol'] = update_info['symbol']
                stock_item['price'] = update_info['price']
                stock_item['shares'] = num_shares[0]['SUM(shares)']
                stock_item['total'] = stock_item['shares'] * update_info['price']

                stock_history.append(stock_item)

        # add up all the totals for each stock item
        for i in range(len(stock_history)):
            total += stock_history[i]['total']
        # plus the balance
        total += account_balance[0]['cash']

        # make all ints into usd
        for i in range(len(stock_history)):
            stock_history[i]['price'] = usd(stock_history[i]['price'])
            stock_history[i]['total'] = usd(stock_history[i]['total'])

        return render_template("index.html", stocks=stock_history, balance=usd(account_balance[0]['cash']), total=usd(total))

    # if user has no history
    else:
        total = usd(account_balance[0]['cash'])
        return render_template("index.html", balance=total, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        num_stocks = request.form.get("shares")

        # Ensure username was submitted
        if not symbol:
            return apology("must provide a business", 400)

        elif not num_stocks:
            return apology("must provide an amount of stock", 400)

        try:
            x = int(num_stocks)
        except:
            return apology("enter a positive integer", 400)

        if int(float(num_stocks)) < float(num_stocks) != int or float(num_stocks) <= 0:
            return apology("enter a positive integer", 400)

        info = lookup(symbol)
        # if symbol does not exist
        if info == None:
            return apology("business does not exist", 400)

        # check if user can afford
        balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        spent = balance[0]["cash"] - (info["price"] * int(num_stocks))
        if spent < 0:
            return apology("insufficient cash", 400)

        # user buys
        # update history
        a = db.execute("INSERT INTO history (id, symbol, shares, price, timestamp) VALUES( :id, :symbol, :shares, :price, CURRENT_TIMESTAMP)",
                       id=session["user_id"], symbol=symbol, shares=int(num_stocks), price=info["price"])

        # update balance
        b = db.execute("UPDATE users SET cash = :spent WHERE id = :id", spent=spent, id=session["user_id"])

        flash(str(num_stocks) + " " + symbol + " STOCK BOUGHT!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get all businesses user has invested in
    history = db.execute("SELECT * FROM history WHERE id= :id", id=session['user_id'])

    # what will be sent to history.html
    stock_history = []

    for log in history:

        # in stock history, we will populate with dicts of stock_items for each type of business
        stock_item = {}

        stock_item['symbol'] = log['symbol']
        stock_item['shares'] = log['shares']
        stock_item['price'] = usd(log['price'])
        stock_item['timestamp'] = log['timestamp']

        stock_history.append(stock_item)

    return render_template("history.html", stocks=stock_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":

        # if symbol is blank
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a symbol", 400)

        info = lookup(symbol)
        # if symbol does not exist
        if info == None:
            return apology("business does not exist", 400)

        return render_template("quoted.html", symbol=info["symbol"], cost=usd(info["price"]))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # require user to input a username, implement a text field whose name is username, render an apology if the user's input is blank, or already exists
    if request.method == "POST":

        # if username is blank
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # if username already exists
        # if no error, then
        # INSERT new user into users,
        # encrypt password
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash_ )",
                            username=request.form.get("username"), hash_=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))
        if not result:
            return apology("username already exists", 400)

        # if pasword is blank
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # if password repeat is blank
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # if password and confirmation do not match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        # log user in automatically
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        num_shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide a business", 400)

        elif not num_shares:
            return apology("must provide an amount of stock", 400)

        try:
            x = int(num_shares)
        except:
            return apology("enter a positive integer", 400)

        if int(float(num_shares)) < float(num_shares) != int or float(num_shares) <= 0:
            return apology("enter a positive integer", 400)

        info = lookup(symbol)
        # if symbol does not exist
        if info == None:
            return apology("business does not exist", 400)

        # check if user owns any
        amount = db.execute("SELECT SUM(shares) FROM history WHERE id = :id AND symbol = :symbol",
                            id=session["user_id"], symbol=symbol)
        amount_owned = amount[0]['SUM(shares)']
        if amount_owned == 0:
            string = "you don't own " + symbol + " stock"
            return apology(string, 400)

        # check if amount sold exists in user's history
        if int(num_shares) > amount_owned:
            string = "you don't own " + str(num_shares) + " of " + symbol + " stock"
            return apology(string, 400)

        # user sells success
        # update history
        a = db.execute("INSERT INTO history (id, symbol, shares, price, timestamp) VALUES( :id, :symbol, :shares, :price, CURRENT_TIMESTAMP)",
                       id=session["user_id"], symbol=symbol, shares=int(num_shares) * (-1), price=info["price"])

        # update balance
        past_balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        balance = info["price"] * int(num_shares) + int(past_balance[0]["cash"])
        b = db.execute("UPDATE users SET cash = :new WHERE id = :id", new=balance, id=session["user_id"])

        flash(str(num_shares) + " " + symbol + " STOCK SOLD!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        stocks = db.execute("SELECT symbol FROM history WHERE id = :id GROUP BY symbol", id=session["user_id"])
        return render_template("sell.html", stock_list=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """EXTRA PERSONALIZED TOUCH"""
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        check = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])

        if not check_password_hash(check[0]["hash"], old_password):
            return(apology("old passwords don't match", 403))

        db.execute("UPDATE users SET hash = :new WHERE id = :id", new=generate_password_hash(
            new_password, method='pbkdf2:sha256', salt_length=8), id=session["user_id"])

        flash("Password Changed")
        return redirect("/")
    else:
        return render_template("change_password.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
