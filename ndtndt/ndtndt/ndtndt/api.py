"""
Routes for the flask application.
"""
import logging
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
            sqlcommand = ('select top 10 i.itemname,i.itemtype,i.yearmanufactured,count(*) as itemsold '
                          'from auction a, item i '
                          'where a.itemname=i.itemname and sold=1 '
                          'group by i.itemname,i.itemtype,i.yearmanufactured '
                          'order by itemsold desc for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)
    def post(self, id):
        pass

# the post request on this item will be called when we need to post an item.
# get with id will return the item associated with the auction[id]

class CreateAuction(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sellerid', type = str, required=True, help='no SellerID provided', location='json')
        self.reqparse.add_argument('itemname', type = str, required=True, help='no item name provided.', location='json')
        self.reqparse.add_argument('category', type = str, required=True, help='no category type provided.', location='json')
        self.reqparse.add_argument('year', type = str, required=True, help='no YearManufactured pro,vided', location='json')
        self.reqparse.add_argument('instock', type = str, required=True, help='no AmountInStock provided',location='json')
        self.reqparse.add_argument('openbid', type = str, required=True, help='no OpenBid amount provided',location='json')
        self.reqparse.add_argument('bidincrement', type = str, required=True, help='no BidIncrement provided',location='json')
        self.reqparse.add_argument('reservePrice', type = str, required=True, help='no ReservePrice provided',location='json')
        self.reqparse.add_argument('expiredate', type = str, required=True, help='no ExpireDates provided',location='json')
        super(CreateAuction, self).__init__()
    def post(self):
        try:
            inputData = self.reqparse.parse_args()
            dbcursor = dbconnection.cursor()
            sqlcommand1 =('INSERT INTO Item (ItemName,ItemType,YearManufactured,AmountInStock) VALUES(?,?,?,?)')
            dbcursor.execute (sqlcommand1,(inputData['itemname'],inputData['category'],inputData['year'],inputData['instock']))
            sqlcommand2 =('INSERT INTO Auction (OpenBid,BidIncrement,ReservePrice,ItemName,SellerID) VALUES (?,?,?,?,?)')
            dbcursor.execute (sqlcommand2,(inputData['openbid'],inputData['bidincrement'],inputData['reservePrice'],inputData['itemname'],inputData['sellerid']))
            sqlcommand3 =('INSERT INTO Post (ExpireDates,PostDate,CustomerID,ItemName) VALUES (?,GETDATE(),?,?)')
            dbcursor.execute (sqlcommand3,(inputData['expiredate'],inputData['sellerid'],inputData['itemname']))
            dbcursor.commit()
        except Exception as e:
            return jsonify({'error': e})
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemname=a.itemname and p.itemname=i.itemname and a.auctionid=1 for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            print(rows)
            if(rows):
                row=str(rows)
                row="<root>"+row[3:-4]+"</root>"
                r=xmltodict.parse(row)
                return(r['root']['row'])
            else:
                return jsonify({'id': id + ' - is not found'})
        except Exception as e:
            print(e)
            return jsonify({'error': e})

class Auction(Resource):
    def post():
        pass
    def get(self, id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemname=a.itemname and p.itemname=i.itemname and a.auctionid=? for xml path')
            dbcursor.execute (sqlcommand,(str(id),))
            rows=dbcursor.fetchall()
            print(rows)
            if(rows):
                row=str(rows)
                row="<root>"+row[3:-4]+"</root>"
                r=xmltodict.parse(row)
                return(r['root']['row'])
            else:
                return jsonify({'id': id + ' - is not found'})
        except Exception as e:
            print(e)
            return jsonify({'error': e})
"""
returns all the auction
class Auction(Resource):
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid, i.itemname,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemname=a.itemname and p.itemname=i.itemname and a.sold=0 '
                         'group by a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid, i.itemname,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates '
                         'order by a.currentBid desc for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)
"""
class StaffPicks(Resource):
    def __init__(self):
        pass
    def delete(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('delete from staffpicks where auctionid=?')
            dbcursor.execute (sqlcommand,(id,))
            dbcursor.commit()
            
        except Exception as e:
            print(e)

    def post(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('insert into staffpicks (auctionid) values (?)')
            dbcursor.execute (sqlcommand,(id,))
            dbcursor.commit()
            
        except Exception as e:
            print(e)
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,a.openbid,a.bidincrement, '
                         'a.currentbid,a.itemname,a.sellerid,i.itemname, '
                         'i.itemtype,i.yearmanufactured,p.postdate, '
                         'p.expiredates from staffpicks s inner join '
                         'auction a on s.auctionid=a.auctionid '
                         'inner join item i on a.itemname=i.itemname '
                         'inner join post p on i.itemname=p.itemname '
                         'for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

api.add_resource(TopSellerCategory, '/topcategory')
api.add_resource(Auction, '/getitem/<string:id>')
api.add_resource(CreateAuction, '/createitem')
api.add_resource(StaffPicks,'/staffpicks')
