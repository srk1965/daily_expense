from pymongo import MongoClient
from json import dumps, loads
import traceback
import json


#######################################
#                                     #
#        create class Mdb             #
#                                     #
#######################################
class Mdb:
    def __init__(self):
        conn_str = "mongodb://localhost:27017/admin"
        client = MongoClient(conn_str)
        self.db = client['user_expense']
        print("connection is set")

    #######################################
    #                                     #
    #     check user_name exist or not    #
    #                                     #
    #######################################
    def user_exist(self, user_name):
        return self.db.user.find({'user_name': user_name}).count() > 0

    #######################################
    #                                     #
    # check user_name & pass exist or not #
    #                                     #
    #######################################
    def user_exists(self, user_name, password):
        return self.db.user.find({'user_name': user_name,
                                  'password': password}).count() > 0

    #######################################
    #                                     #
    #         add user_signup data        #
    #                                     #
    #######################################
    def signup_data(self, first_name, last_name, user_name, password):
        try:
            rec = {
                'first_name': first_name,
                'last_name': last_name,
                'user_name': user_name,
                'password': password,

            }
            self.db.user.insert(rec)
        except Exception as exp:
            print("[Mdb] :: signup_data() :: Got exception: %s" % exp)
            print(traceback.format_exc())

    #######################################
    #                                     #
    #         add user_signup data        #
    #                                     #
    #######################################
    def daily_expense_user_data(self, title, amount, date):
        rec = {
            'title': title,
            'amount': amount,
            'date': date
        }
        self.db.daily_expense_user_data.insert(rec)

    #######################################
    #                                     #
    #      get user expense data          #
    #                                     #
    #######################################
    def get_daily_expense_data(self):
        collection = self.db["daily_expense_user_data"]
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret

    #######################################
    #                                     #
    #     delete user expense data        #
    #                                     #
    #######################################
    def delete_by_id(self, text):
        ret = []
        collection = self.db["daily_expense_user_data"]
        collection.remove({"title": text})
        result = collection.find({})
        for data in result:
            ret.append(data)
        return ret

    #######################################
    #                                     #
    #     get update user expense data    #
    #                                     #
    #######################################
    def get_update_by_id(self, text):
        result = self.db.daily_expense_user_data.find({"title": text})
        ret = []
        for data in result:
            ret.append(data)
        return ret

    #######################################
    #                                     #
    #       update user expense data      #
    #                                     #
    #######################################
    def update_daily_expense(self, title, amount, date):
        self.db.daily_expense_user_data.update(
            {'title': title}, {'$set': {'amount': amount, 'date': date}})

#######################################
#                                     #
#  (Main) Starting Point of Program   #
#                                     #
#######################################
if __name__ == '__main__':
    mdb = Mdb()
    # mdb.daily_expense('T-Shirt', 500, '2017-12-10')
    # mdb.get_daily_expense()
