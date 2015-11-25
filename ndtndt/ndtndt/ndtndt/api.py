"""
Routes for the flask application.
"""
import logging
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json, xmltodict
from binascii import *
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
        self.reqparse.add_argument('year', type = str, required=True, help='no YearManufactured provided', location='json')
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
# Returns information for one item given auctionID
class Auction(Resource):
    def post():
        pass
    def get(self, id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                        'a.sellerid,i.itemtype, i.yearmanufactured, p.postdate, '
                        'p.expiredates,pp.firstname,pp.lastname,i.itemimg, count(b.auctionid) as TotalBidders '
                        'from auction a inner join item i on i.itemname=a.itemname '
                        'inner join post p on p.itemname=i.itemname inner join person pp on pp.ssn=a.sellerid '
                        'inner join bid b on b.auctionid=a.auctionid '
                        'where a.auctionid=? '
                        'group by a.auctionid,i.itemname,a.openbid,a.bidincrement, '
                        'a.currentbid, a.sellerid,i.itemtype, i.yearmanufactured, '
                        'p.postdate, p.expiredates,pp.firstname,pp.lastname,i.itemimg for xml path')
            dbcursor.execute (sqlcommand,(str(id),))
            rows=dbcursor.fetchall()
            #print(rows)
            if(rows):
                row=str(rows)
                row="<root>"+row[3:-4]+"</root>"
                r=xmltodict.parse(row)
                #print(r['root']['row']['itemimg'])
                f = open('ndtndt/temp.jpg','wb')
                f.write(a2b_base64(r['root']['row']['itemimg']))
                r['root']['row']['itemimg']='temp.jpg'

                return(r['root']['row'])
            else:
                return jsonify({'id': id + ' - is not found'})
        except Exception as e:
            print(e)
            return jsonify({'error': e})

class AuctionAll(Resource):
    def post():
        pass
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select a.auctionid,i.itemname,a.openbid,a.bidincrement, a.currentbid, '
                         'a.sellerid,i.itemtype, i.yearmanufactured, p.postdate, '
                         'p.expiredates from auction a,item i,post p '
                         'where i.itemname=a.itemname and p.itemname=i.itemname and a.auctionid=p.auctionid for xml path')
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

# montly sales report 
class SalesReport(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('SELECT YEAR(p.ExpireDates) as SalesYear, '
                        'MONTH(p.ExpireDates) as SalesMonth, '
                        'SUM(a.currentBid) AS TotalSales '
                        'FROM Auction a ,post p where a.sold=1 and p.auctionid=a.auctionid '
                        'GROUP BY YEAR(p.ExpireDates), MONTH(p.ExpireDates) '
                        'ORDER BY YEAR(p.ExpireDates), MONTH(p.ExpireDates) '
                         'for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# Best list of items base on amount sold
class BestItemList(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('SELECT a.itemname as ItemName,count(a.itemname) as AmountSold '
                         'from auction a where a.sold=1 group by a.itemname order by count(a.itemname) desc '
                         'for xml path')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# get auction history given auction id
class AuctionHistory(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('select * from '
                        '(select i.itemname,i.itemtype,i.yearmanufactured,i.itemimg,pp.ssn '
                        'as sellerid,pp.firstname as sellerfirstname, pp.lastname as sellerlastname, '
                        'a.auctionid,a.openbid,a.currentbid,p.postdate,p.ExpireDates,b.biddate '
                        'from item i inner join auction a on i.itemname=a.itemname inner join bid b on a.auctionid=b.auctionid '
                        'inner join post p on p.auctionid=a.auctionid inner join person pp on pp.ssn=p.customerid '
                        'where a.auctionid=? and a.sold=1) as res1, '
                        '(select pp.ssn as buyerid,pp.firstname as buyerfirstname, pp.lastname as buyerlastname '
                        'from person pp inner join bid b on b.customerid=pp.ssn inner join auction a on b.auctionid=a.auctionid '
                        'where a.auctionid=? and a.sold=1) as res2 '
                        'for xml path')
            dbcursor.execute (sqlcommand,(str(id),str(id)))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# returns the revenue generated by an item
class RevenueByItem(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('SELECT a.itemname as ItemName,SUM(a.currentbid) as TotalSales FROM Auction a '
                         'WHERE a.sold=1 and a.itemname=? '
                         'group by a.itemname '
                        'for xml path')
            dbcursor.execute (sqlcommand,(id,))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# returns the revenue generated by item type
class RevenueByType(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('SELECT i.itemtype as ItemType,SUM(a.currentbid) as TotalSales FROM Auction a,item i '
                        'WHERE a.sold=1 and a.itemname=i.itemname and i.itemtype =? '
                        'group by i.itemtype '
                        'for xml path')
            dbcursor.execute (sqlcommand,(id,))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# returns the revenue generated by seller id
class RevenueBySellerID(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('SELECT p.firstname as FirstName,p.lastname as LastName,SUM(a.currentbid) as TotalSales FROM Auction a,person p '
                        'WHERE a.sold=1 and a.sellerid=p.ssn and p.ssn =? '
                        'group by p.firstname,p.lastname '
                        'for xml path')
            dbcursor.execute (sqlcommand,(id,))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# A history of all current and past auctions a customer has taken part in
class CustomerAuctionHistory(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('''select * from
                         (select i.itemname,i.itemtype,i.yearmanufactured,i.itemimg,pp.ssn as sellerid,pp.firstname as sellerfirstname, pp.lastname as sellerlastname,
                        a.auctionid,a.openbid,a.currentbid,p.postdate,p.ExpireDates,b.biddate
                        from item i inner join auction a on i.itemname=a.itemname inner join bid b on a.auctionid=b.auctionid 
                        inner join post p on p.auctionid=a.auctionid inner join person pp on pp.ssn=p.customerid
                        where pp.ssn=?) as res1,
                        (select pp.ssn as buyerid,pp.firstname as buyerfirstname, pp.lastname as buyerlastname
                        from person pp inner join bid b on b.customerid=pp.ssn inner join auction a on b.auctionid=a.auctionid
                        where pp.ssn=?) as res2 
                        for xml path''')
            dbcursor.execute (sqlcommand,(id,id))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# item suggestions for a given customer (based on that customers past purchases
class ItemSuggestions(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('''select i.itemname from item i
                            where i.itemtype=( select i.itemtype 
                            from bid b inner join auction a on b.auctionid=a.auctionid inner join item i on a.itemname=i.itemname
                            where a.sold=1 and b.customerid=? )
                        for xml path''')
            dbcursor.execute (sqlcommand,(id,))
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# customer representative generated most total revenue
class StaffRevenue(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            dbcursor = dbconnection.cursor()
            sqlcommand =('''select p.firstname,p.lastname,sum(a.currentbid) as generatedrevenue
                        from person p inner join auction a on p.ssn=a.monitor
                        where a.sold=1
                        group by p.firstname,p.lastname
                        order by sum(a.currentbid) desc
                        for xml path''')
            dbcursor.execute (sqlcommand)
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            return(r['root']['row'])
        except Exception as e:
            print(e)

# Creating a new user
class CreateUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ssn', type = str, required=True, help='no CustomerID provided', location='json')
        self.reqparse.add_argument('lastname', type = str, required=True, help='no Last name provided.', location='json')
        self.reqparse.add_argument('firstname', type = str, required=True, help='no First name provided.', location='json')
        self.reqparse.add_argument('address', type = str, required=True, help='no Address provided', location='json')
        self.reqparse.add_argument('city', type = str, required=True, help='no City provided',location='json')
        self.reqparse.add_argument('state', type = str, required=True, help='no State provided',location='json')
        self.reqparse.add_argument('zipcode', type = str, required=True, help='no Zip Code provided',location='json')
        self.reqparse.add_argument('telephone', type = str, required=True, help='no Telephone number provided',location='json')
        self.reqparse.add_argument('userpassword', type = str, required=True, help='no Password provided',location='json')
        self.reqparse.add_argument('creditcardnum', type = str, required=True, help='no Credit Card Number provided',location='json')
        super(CreateUser, self).__init__()
    def post(self):
        try:
            inputData = self.reqparse.parse_args()
            dbcursor = dbconnection.cursor()
            sqlcommand1 =('INSERT INTO Person (SSN,LastName,FirstName,Address,City,State,ZipCode,Telephone,UserPassword) VALUES(?,?,?,?,?,?,?,?,?)')
            dbcursor.execute (sqlcommand1,(inputData['ssn'],inputData['lastname'],inputData['firstname'],inputData['address'],inputData['city'],inputData['state'],inputData['zipcode'],inputData['telephone'],inputData['userpassword']))
            sqlcommand2 =('INSERT INTO Customer (Rating,CreditCardNum,CustomerID) VALUES(1,?,?)')
            dbcursor.execute (sqlcommand2,(inputData['creditcardnum'],inputData['ssn']))
            dbcursor.commit()
            return jsonify({'sucess'})
        except Exception as e:
            return jsonify({'failed - error': e})

class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ssn', type = str, required=True, help='no ID provided', location='json')
        self.reqparse.add_argument('userpassword', type = str, required=True, help='no Password provided.', location='json')
        super(Login, self).__init__()
    def post(self):
        try:
            inputData = self.reqparse.parse_args()
            dbcursor = dbconnection.cursor()
            sqlcommand =('select * from person where ssn=? and userpassword=?')
            dbcursor.execute(sqlcommand,(inputData['ssn'],inputData['userpassword']))
            if dbcursor.rowcount == 0:
                return jsonify({'failed': 'failed'})
            # checking if the user login is an employee
            sqlcommand=('select MagLevel from Employee where EmployeeID=?')
            dbcursor.execute(sqlcommand,(inputData['ssn'],))
            # return success if the user is not employee
            if dbcursor.rowcount == 0:
                return jsonify({'success': 'ok'})
            rows=dbcursor.fetchall()
            row=str(rows)
            row="<root>"+row[3:-4]+"</root>"
            r=xmltodict.parse(row)
            # returning employee base on maglevel. 1 = manager and 2 = customer rep
            return(r['root']['row'])
        except Exception as e:
            return jsonify({'failed - error': e})

api.add_resource(TopSellerCategory, '/topcategory')
api.add_resource(Auction, '/getitem/<string:id>', endpoint="auction")
api.add_resource(AuctionAll, '/getitem', endpoint="auctionAll")
api.add_resource(CreateAuction, '/createitem')
api.add_resource(StaffPicks,'/staffpicks')
api.add_resource(SalesReport,'/salesreport')
api.add_resource(BestItemList,'/bestitemlist')
api.add_resource(AuctionHistory,'/auctionhistory/<string:id>')
api.add_resource(RevenueByItem,'/revenuebyitem/<string:id>')
api.add_resource(RevenueByType,'/revenuebytype/<string:id>')
api.add_resource(RevenueBySellerID,'/revenuebysellerid/<string:id>')
api.add_resource(CustomerAuctionHistory,'/customerauctionhistory/<string:id>')
api.add_resource(ItemSuggestions,'/itemsuggestions/<string:id>')
api.add_resource(StaffRevenue,'/staffrevenue')
api.add_resource(CreateUser,'/createuser')
api.add_resource(Login,'/login')