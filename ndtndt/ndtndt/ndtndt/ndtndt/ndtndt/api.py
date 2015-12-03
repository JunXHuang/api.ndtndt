﻿"""
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
          
class StaffPicks(Resource):
    def __init__(self):
        pass
    def delete(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('delete from staffpicks where auctionid=?')
            dbcursor.execute (sqlcommand,(id,))
            dbcursor.commit()
            dbconnection.close()
        except Exception as e:
            print(e)

    def post(self,id):
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

class Insert(Resource):
    def get(self):
        try:
            val1=''
            val2=''
            val3=''
            val4=''
            val5=''
            val6=''
            val7=''
            val8=''
            val9=''
            val10=''
            dbcursor = dbconnection.cursor()
            sqlcommand1 =('INSERT INTO Item (ItemName,ItemType,YearManufactured,AmountInStock) VALUES(?,?,?,?)')
            dbcursor.execute (sqlcommand1,(val1,val2,val3,val4))
            sqlcommand2 =('INSERT INTO Auction (OpenBid,BidIncrement,ReservePrice,ItemName,SellerID) VALUES (?,?,?,?,?)')
            dbcursor.execute (sqlcommand2,(val5,val6,val7,val1,val8))
            sqlcommand3 =('INSERT INTO Post (ExpireDates,PostDate,CustomerID,ItemName) VALUES (?,GETDATE(),?,?)')
            dbcursor.execute (sqlcommand3,(val9,val10,val1))
            dbcursor.commit()
            dbconnection.close()
        except Exception as e:
            print(e)


api.add_resource(TopSellerCategory, '/topcategory')
api.add_resource(Item, '/item/<string:id>')
api.add_resource(Auction,'/auction/lowest')
api.add_resource(StaffPicks,'/staffpicks')
