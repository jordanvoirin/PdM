; Script to analyse the effect of jmax on the retrieval
;

sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\noise_study\5000'

jmax = (make_array(231, 1, /INTEGER, /INDEX))[4:230] + 1
Njmax = n_elements(jmax)
results = []


result =  phaseRetrieval(sfolderPath+'\', jmax[0],1,0)
pres = plot(result.res.j,result.res.a_j*1000,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j')
for iJmax = 1, Njmax-1 do begin
  
  if iJmax ne Njmax-1 then begin
    result =  phaseRetrieval(sfolderPath+'\', jmax[iJmax],1,0)
    pres = plot(result.res.j,result.res.a_j*1000,'b-2', MARGIN=0,/overplot)
  endif else if iJmax eq Njmax-1 then begin
    result =  phaseRetrieval(sfolderPath+'\', jmax[iJmax],1,1)
    pres = plot(result.res.j,result.res.a_j*1000,'b-2', MARGIN=0,name='modal',/overplot)
    pzon = plot(result.zon.j,result.zon.a_j*1000,'r-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='zonal', /overplot)
    !null = LEGEND(target=[pres, pzon])
  endif
endfor

end