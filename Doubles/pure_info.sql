select p.objid, 
  p.pid1, 
      pz1.z as "photoZ1", pz1.zErr as 'photoZ_err1', gs1.z as 'schlegelZ1', gs1.z_err as 'schlegelZ_err1', pz1.absMagR as 'absMagR1',
      po1.u as 'u1', po1.g as 'g1', po1.r as 'r1', po1.i as 'i1', po1.z as 'z1',
  p.pid2, 
      pz2.z as "photoZ2", pz2.zErr as 'photoZ_err2', gs2.z as 'schlegelZ2', gs2.z_err as 'schlegelZ_err2', pz2.absMagR as 'absMagR2',
      po2.u as 'u2', po2.g as 'g2', po2.r as 'r2', po2.i as 'i2', po2.z as 'z2'
from mydb.Pure as p
  INNER JOIN photoZ pz1
  on pz1.objID = p.pid1
  INNER JOIN photoZ pz2
  on pz2.objID = p.pid2
  INNER JOIN photoObjAll po1
  on p.objid = po1.objID
  INNER JOIN photoObjAll po2
  on p.objid = po2.objID
  LEFT JOIN galSpecInfo gs1
  on gs1.specObjID = po1.specObjID
  LEFT JOIN galSpecInfo gs2
  on gs2.specObjID = po2.specObjID
