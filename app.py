from flask import Flask, request, render_template, url_for
import traceback
from db import Mdb
from flask_login import LoginManager, UserMixin, login_user, login_required, \
    logout_user, current_user

#######################################
#                                     #
#       Create Flask Object           #
#                                     #
#######################################
app = Flask(__name__)
mdb = Mdb()
login_manager = LoginManager()
login_manager.init_app(app)



#######################################
#                                     #
#          login manager              #
#                                     #
#######################################
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(id):
    print '[%s]' % db.session.query(User).get(id)
    return db.session.query(User).get(id)


# Flask-Login integration
def is_authenticated(self):
        return True


def is_active(self):
        return True


def is_anonymous(self):
        return False


def get_id(self):
        return self.id

@app.route('/logout')
@login_required
def user_logout():
    logout_user()
    return redirect('/login')


#######################################
#                                     #
#           starting root             #
#                                     #
##############################s#########
@app.route('/')
def index():
    return render_template('/index.html')


#######################################
#                                     #
#             get signup              #
#                                     #
#######################################
@app.route("/get_signup", methods=['GET'])
def get_signup_data():
    return render_template('signup.html')


#######################################
#                                     #
#             add signup              #
#                                     #
#######################################
@app.route("/add_signup", methods=['POST'])
def add_signup_data():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        password = request.form['password']
        if mdb.user_exist(user_name):
            print("User already Exist!")
            return render_template('/already_user.html')
        else:
            mdb.signup_data(first_name, last_name, user_name, password)
            return render_template('/done_signup.html')
    except Exception as exp:
        print("add_signup_data() :: Got exception: %s" % exp)
        print(traceback.format_exc())
        return render_template('/signup.html')


#######################################
#                                     #
#             get login               #
#                                     #
#######################################
@app.route("/get_login", methods=['GET'])
def get_login_data():
    return render_template('login.html')


#######################################
#                                     #
#             add login               #
#                                     #
#######################################
@app.route('/add_login', methods=['POST'])
def login():
    try:
        user_name = request.form['user_name']
        password = request.form['password']
        if mdb.user_exists(user_name, password):
            print("username and password is right!")
            return render_template('user_panel.html')
            login_user(user)
        else:
            print('Login Failed, Id/password are wrong!')
            return render_template('invalid_user.html')
    except Exception as exp:
        print(traceback.format_exc())
    return render_template('login.html')


#######################################
#                                     #
#        get_add_expense path         #
#                                     #
#######################################
@app.route("/get_add_expense", methods=['GET'])
def get_user_profile():
    return render_template('add_expense.html')


#######################################
#                                     #
#        get user home panel          #
#                                     #
#######################################
@app.route("/home", methods=['GET'])
def get_home():
    return render_template('user_panel.html')


#######################################
#                                     #
#          add user expense           #
#                                     #
#######################################
@app.route("/add_user_expense", methods=['POST'])
def add_daily():
    try:
        title = request.form['title']
        amount = request.form['amount']
        date = request.form['date']
        mdb.daily_expense_user_data(title, amount, date)
        return render_template('/done_expense_data.html')
    except Exception as exp:
        print("add_daily() :: Got exception: %s" % exp)
        print(traceback.format_exc())
        return render_template('/add_expense.html')


#######################################
#                                     #
#       get user expense data         #
#                                     #
#######################################
@app.route("/get_expense_data", methods=['GET'])
def get_expense():
    data = mdb.get_daily_expense_data()
    templateData = {'title': 'GET EXPENSE', 'data': data}
    return render_template('show_expense.html', **templateData)


#######################################
#                                     #
#       delete user expense data      #
#                                     #
#######################################
@app.route("/delete", methods=['GET'])
def delete():
    try:
        text = request.args.get("id")
        data = mdb.delete_by_id(text)
        templateData = {'data': data}
        return render_template('show_expense.html', **templateData)
    except Exception as exp:
        print("delete() :: Got exception: %s" % exp)
        print(traceback.format_exc())
        return render_template('/show_expense.html')


#######################################
#                                     #
#     get update user expense data    #
#                                     #
#######################################
@app.route("/update", methods=['GET'])
def update():
    try:
        text = request.args.get("id")
        data = mdb.get_update_by_id(text)
        templateData = {'title': 'UPDATE EXPENSE', 'data': data}
        return render_template('/update_expense.html', **templateData)
    except Exception as exp:
        print("update() :: Got exception: %s" % exp)
        print(traceback.format_exc())
        return render_template('/update_expense.html')


#######################################
#                                     #
#     update user expense data        #
#                                     #
#######################################
@app.route("/update_data", methods=['POST'])
def update_data():
    try:
        title = request.form["title"]
        amount = request.form["amount"]
        date = request.form["date"]
        mdb.update_daily_expense(title, amount, date)
        return render_template('/done_update_expense_data.html')
    except Exception as exp:
        print("update_data() :: Got exception: %s" % exp)
        print(traceback.format_exc())
        return render_template('/update_expense.html')

#######################################
#                                     #
#  (Main) Starting Point of Program   #
#                                     #
#######################################
if __name__ == '__main__':
    app.run(debug=True)
