function toNoll, m

zeze = indzer(1,66)
zeze = fix(zeze)
zeze[2,2] = -zeze[2,2]
zeze[2,4] = -zeze[2,4]
zeze[2,6] = -zeze[2,6]
zeze[2,8] = -zeze[2,8]
zeze[2,12] = -zeze[2,12]
zeze[2,14] = -zeze[2,14]
zeze[2,16] = -zeze[2,16]
zeze[2,18] = -zeze[2,18]
zeze[2,20] = -zeze[2,20]
zeze[2,22] = -zeze[2,22]
zeze[2,24] = -zeze[2,24]
zeze[2,26] = -zeze[2,26]
zeze[2,28] = -zeze[2,28]
zeze[2,30] = -zeze[2,30]
zeze[2,32] = -zeze[2,32]
zeze[2,34] = -zeze[2,34]
zeze[2,38] = -zeze[2,38]
zeze[2,40] = -zeze[2,40]
zeze[2,42] = -zeze[2,42]
zeze[2,44] = -zeze[2,44]
zeze[2,46] = -zeze[2,46]
zeze[2,48] = -zeze[2,48]
zeze[2,50] = -zeze[2,50]
zeze[2,52] = -zeze[2,52]
zeze[2,54] = -zeze[2,54]
zeze[2,56] = -zeze[2,56]
zeze[2,58] = -zeze[2,58]
zeze[2,60] = -zeze[2,60]
zeze[2,62] = -zeze[2,62]
zeze[2,64] = -zeze[2,64]

mtmp = m

for iZer = 0, 65 do begin
  
  ind = where(mtmp[1,*] eq zeze[1,iZer] and mtmp[2,*] eq zeze[2,iZer])
  
  m[1,iZer] = zeze[1,iZer]
  m[2,iZer] = zeze[2,iZer]
  m[3,iZer] = mtmp[3,ind]
endfor


return, m
end