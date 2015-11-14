"""
Routes for the flask application.
"""

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json, xmltodict

from ndtndt import app, dbconnection
api = Api(app)
auth = HTTPBasicAuth()

# dummy, just to see that it works
@app.route('/')
def default():
    try:
        return jsonify({'init': 'api.ndtndt, call some resource uri'})
    except Exception as e:
        print(e)

# there is no post on this
# get returns top seller category
class TopSellerCategory(Resource):
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand = ('select top 10 i.itemid,i.itemtype,i.yearmanufactured,count(*) as itemsold '
                          'from auction a, item i '
                          'where a.itemid=i.itemid and sold=1 '
                          'group by i.itemid,i.itemtype,i.yearmanufactured '
                          'order by itemsold desc for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            dbconnection.close()
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)
    def post(self, id):
        pass

#the post request on this item will be called when we need to post an item.
#get with id will return the item associated with the auction[id]
class Item(Resource):
    def __init__(self):
        pass
    def post(self):
        pass
    def get(self, id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemid,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid, i.itemname,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemid=a.itemid and p.itemid=i.itemid and a.auctionid=? for xml path')
            dbcursor.execute (sqlcommand,list(id))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            dbconnection.close()
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)


api.add_resource(TopSellerCategory, '/topcategory')
api.add_resource(Item, '/item/<string:id>')
