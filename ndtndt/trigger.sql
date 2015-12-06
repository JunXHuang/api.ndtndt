CREATE TRIGGER RemoveFromStaffPicks
ON Auction
FOR UPDATE AS BEGIN
delete from staffpicks where auctionid=
(SELECT a.auctionid
  FROM auction a inner join staffpicks s on a.auctionid=s.auctionid
  WHERE a.sold=1)
END