select p.objid, p.pid1, p.pid2
from mydb.Pure as p
where p.objid not in (select objid from mydb.PureInfo)
