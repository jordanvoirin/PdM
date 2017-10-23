; Script to analyse the data
;

sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\angle_study\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

Angles = []
results = []
for iFol = 0, Nfolders-1 do begin
  results = [results,phaseRetrieval(sFolderPaths[iFol]+'\')]

  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
  sAngle = sepFolderPath[n_elements(sepFolderPath)-1]
  Angles = [Angles,double(sAngle)]
endfor

astAjres = []
astAjzon = []
for iFol = 0, Nfolders-1 do begin
  astAjres = [astAjres,sqrt(results[iFol].res.a_j[5]*results[iFol].res.a_j[5]+results[iFol].res.a_j[6]*results[iFol].res.a_j[6])]
  astAjzon = [astAjzon,sqrt(results[iFol].zon.a_j[5]*results[iFol].zon.a_j[5]+results[iFol].zon.a_j[6]*results[iFol].zon.a_j[6])]
endfor

sortedInd = sort(Angles)

;plot Norm astigmatism vs. angle

pAstAngleres = plot(Angles[sortedInd],astAjres[sortedInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Astigmatism Coef Norm [nm]',name='modal')
pAstAnglezon = plot(Angles[sortedInd],astAjzon[sortedInd]*1000.d,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pAstAngleres, pAstAnglezon])

; plot defocus coeff. vs. angle

pAstAngleres = plot(Angles[sortedInd],results[sortedInd].res.a_j[4]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Defocus Coef [nm]',name='modal')
pAstAnglezon = plot(Angles[sortedInd],results[sortedInd].zon.a_j[4]*1000.d,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pAstAngleres, pAstAnglezon])

nbrRows = Nfolders
nbrCol = 3

marge = 0.3

resDim = size(results[0].res.wavefront,/dimension)
imres = image(results[0].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title=string(long(Angles[0]))+ ' Modal', MARGIN=marge,layout=[nbrCol,nbrRows,1])
zonDim = size(results[0].zon.wavefront,/dimension)
imzon = image(results[0].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,2])

jmax = max(results[0].res.j)
pres = plot(results[0].res.j,results[0].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,3])
pzon = plot(results[0].zon.j,results[0].zon.a_j,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pres, pzon])

for iFol = 1, Nfolders-1 do begin
  
  resDim = size(results[iFol].res.wavefront,/dimension)
  imres = image(results[iFol].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title=string(long(Angles[iFol]))+ ' Modal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-2])
  zonDim = size(results[iFol].zon.wavefront,/dimension)
  imzon = image(results[iFol].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-1])
  
  jmax = max(results[iFol].res.j)
  pres = plot(results[iFol].res.j,results[iFol].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)])
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j,'r-2',name='zonal',/overplot)
  
endfor

end
