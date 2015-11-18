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

# the post request on this item will be called when we need to post an item.
# get with id will return the item associated with the auction[id]

class Auction(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sellerid', type = str, required=True, help='no SellerID provided')
        self.reqparse.add_argument('itemname', type = str, required=True, help='no item name provided.')
        self.reqparse.add_argument('category', type = str, required=True, help='no category type provided.')
        self.reqparse.add_argument('year', type = str, required=True, help='no YearManufactured provided')
        self.reqparse.add_argument('instock', type = str, required=True, help='no AmountInStock provided')
        self.reqparse.add_argument('openbid', type = str, required=True, help='no OpenBid amount provided')
        self.reqparse.add_argument('bidincrement', type = str, required=True, help='no BidIncrement provided')
        self.reqparse.add_argument('reservePrice', type = str, required=True, help='no ReservePrice provided')
        self.reqparse.add_argument('expiredate', type = str, required=True, help='no ExpireDates provided')
        super(Auction, self).__init__()
    def post(self):
        try:
            inputData = self.reqparse.parse_args()
            dbcursor = dbconnection.cursor()
            sqlcommand1 =('INSERT INTO Item (ItemName,ItemType,YearManufactured,AmountInStock) VALUES(?,?,?,?)')
            dbcursor.execute (sqlcommand1,(inputData['itemname'],inputData['category'],inputData['year'],inputData['instock']))
            sqlcommand2 =('INSERT INTO Auction (OpenBid,BidIncrement,ReservePrice,ItemName,SellerID) VALUES (?,?,?,?,?)')
            dbcursor.execute (sqlcommand2,(inputData['openbid'],inputData['bidincrement'],inputData['reservePrice'],inputData['itemname'],inputData['sellerid']))
            sqlcommand3 =('INSERT INTO Post (ExpireDates,PostDate,CustomerID,ItemName) VALUES (?,GETDATE(),?,?)')
            dbcursor.execute (sqlcommand3,(inputData['expiredate'],inputData['sellerid'],val1))
            dbcursor.commit()
            dbconnection.close()
        except Exception as e:
            return jsonify{'error': e}
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

"""
returns all the auction
class Auction(Resource):
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemid,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid, i.itemname,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemid=a.itemid and p.itemid=i.itemid and a.sold=0 '
                         'group by a.auctionid,i.itemid,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid, i.itemname,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates '
                         'order by a.currentBid desc for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            dbconnection.close()
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)
"""
class StaffPicks(Resource):
    def __init__(self):
        self.
    def delete(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('delete from staffpicks where auctionid=?')
            dbcursor.execute (sqlcommand,(id,))
            dbcursor.commit()
            dbconnection.close()
        except Exception as e:
            print(e)

    def post(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('insert into staffpicks (auctionid) values (?)')
            dbcursor.execute (sqlcommand,(id,))
            dbcursor.commit()
            dbconnection.close()
        except Exception as e:
            print(e)
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,a.openbid,a.bidincrement, '
                         'a.currentbid,a.itemid,a.sellerid,i.itemname, '
                         'i.itemtype,i.yearmanufactured,p.postdate, '
                         'p.expiredates from staffpicks s inner join '
                         'auction a on s.auctionid=a.auctionid '
                         'inner join item i on a.itemid=i.itemid '
                         'inner join post p on i.itemid=p.itemid '
                         'for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            dbconnection.close()
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

api.add_resource(TopSellerCategory, '/topcategory')
api.add_resource(Auction, '/getItem/<string:id>')
api.add_resource(StaffPicks,'/staffpicks')
