select count(*) 
from mydb.PureInfo
where photoZ1 <> -9999 and photoZ2 <> -9999 and schlegelZ1 is not NULL and schlegelZ2 is not NULL
