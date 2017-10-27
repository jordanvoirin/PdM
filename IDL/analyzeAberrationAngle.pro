; Script to analyse the astigmatism data
;
;instanciate folderPath------------------------------------------------------------------------
sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\angle_study\cropped\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

;run phaseRetrieval----------------------------------------------------------------------------
Angles = []
results = list()
for iFol = 0, Nfolders-1 do begin
  results.add, phaseRetrieval(sFolderPaths[iFol]+'\',20,1,1)

  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
  sAngle = sepFolderPath[n_elements(sepFolderPath)-1]
  Angles = [Angles,double(sAngle)]
endfor

;get the zernike coefficient----------------------------------------------------------------------

a8res = []
a6res = []
a8zon = []
a6zon = []
defocAjres = []
defocAjzon = []
for iFol = 0, Nfolders-1 do begin
  a8res = [a5res,results[iFol].res.a_j[4]]
  a6res = [a6res,results[iFol].res.a_j[2]]
  a8zon = [a5zon,results[iFol].zon.a_j[4]]
  a6zon = [a6zon,results[iFol].zon.a_j[2]]
  defocAjres = [defocAjres,results[iFol].res.a_j[0]]
  defocAjzon = [defocAjzon,results[iFol].zon.a_j[0]]
endfor

sortedInd = sort(Angles)

aberrationsModel = (aberrationParallelPlateModel(1.49,1.4e-3,Angles[sortedInd]))*1e9
thZernikeCoef6 = aberrationsModel[*,0]/sqrt(6)/2
thZernikeCoef8 = aberrationsModel[*,1]/sqrt(8)/2
;plot aberrations vs. angle------------------------------------------------------------------------

rmseA6mod = RMSE(thZernikeCoef6,abs(a6res[sortedInd]*1000.d))
rmseA6zon = RMSE(thZernikeCoef6,abs(a6zon[sortedInd]*1000.d))

rmseA8mod = RMSE(thZernikeCoef8,abs(a8res[sortedInd]*1000.d))
rmseA8zon = RMSE(thZernikeCoef8,abs(a8zon[sortedInd]*1000.d))

pA6Angleres = plot(Angles[sortedInd],abs(a6res[sortedInd]*1000.d),'b-2',xtitle='Parallel Faces Angle [deg]',$
  ytitle = 'a6 [nm]',name='modal RMSE = '+string(rmseA6mod))
pA6Anglezon = plot(Angles[sortedInd],abs(a6zon[sortedInd]*1000.d),'r-2',name='zonal RMSE = '+string(rmseA6zon),/overplot)
pAstAnglemod = plot(Angles[sortedInd],thZernikeCoef6,'k-2',name='model',/overplot); factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
!null = LEGEND(target=[pA6Angleres,pA6Anglezon,pAstAnglemod],/DATA)

pA6Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatism_angle.pdf', BORDER=10, RESOLUTION=350
pA6Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatism_angle.png', BORDER=10, RESOLUTION=350

pA8Angleres = plot(Angles[sortedInd],abs(a8res[sortedInd]*1000.d),'b-2',xtitle='Parallel Faces Angle [deg]',$
  ytitle = 'a8 [nm]',name='modal RMSE = '+string(rmseA8mod))
pA8Anglezon = plot(Angles[sortedInd],abs(a8zon[sortedInd]*1000.d),'r-2',name='zonal RMSE = '+string(rmseA8zon),/overplot)
pComAnglemod = plot(Angles[sortedInd],thZernikeCoef8,'k-2',name='model',/overplot); factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
!null = LEGEND(target=[pA8Angleres, pA8Anglezon,pComAnglemod],/DATA)

pA8Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\coma_angle.pdf', BORDER=10, RESOLUTION=350
pA8Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\coma_angle.png', BORDER=10, RESOLUTION=350

; plot defocus coeff. vs. angle----------------------------------------------------------------------

pdefocAngleres = plot(Angles[sortedInd],defocAjres[sortedInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Defocus Coef [nm]',name='modal')
pdefocAnglezon = plot(Angles[sortedInd],defocAjzon[sortedInd]*1000.d,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pdefocAngleres, pdefocAnglezon],/DATA)
pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\defoc_angle.pdf', BORDER=10, RESOLUTION=350
pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\defoc_angle.png', BORDER=10, RESOLUTION=350


;Compare Phase and zernike modal vs. zonal-----------------------------------------------------------
nbrRows = Nfolders
nbrCol = 3

minValue = -thZernikeCoef6[Nfolders-1]/2
maxValue = thZernikeCoef6[Nfolders-1]/2

marge = 0.3
modwavefront = results[0].res.wavefront[*,*]*1000
zonwavefront = results[0].zon.wavefront[*,*]*1000
resDim = size(modwavefront,/dimension)
imres = image(modwavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],min_value=minvalue,max_value = maxValue, $
  title=string(long(Angles[0]))+ ' Modal', MARGIN=marge,layout=[nbrCol,nbrRows,1])
zonDim = size(zonwavefront,/dimension)
imzon = image(zonwavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],min_value=minvalue,max_value = maxValue $
  ,title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,2])
jmax = max(results[0].res.j)
pres = plot(results[0].res.j,results[0].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,3])
pzon = plot(results[0].zon.j,results[0].zon.a_j,'r-2',name='zonal',/overplot)
;!null = LEGEND(target=[pres, pzon])

for iFol = 1, Nfolders-1 do begin
  modwavefront = results[iFol].res.wavefront[*,*]*1000
  zonwavefront = results[iFol].zon.wavefront[*,*]*1000
  resDim = size(modwavefront,/dimension)
  imres = image(modwavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]]$
    ,title=string(long(Angles[iFol]))+ ' Modal', MARGIN=marge,min_value=minvalue,max_value = maxValue $
    ,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-2])
  zonDim = size(zonwavefront,/dimension)
  imzon = image(zonwavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],min_value=minvalue,max_value = maxValue, $
    title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-1])
  If iFol eq 1 then begin
    c = COLORBAR(TARGET=imres, ORIENTATION=1,TITLE='[nm]',range=[minValue,maxValue])
  Endif
  
  jmax = max(results[iFol].res.j)
  pres = plot(results[iFol].res.j,results[iFol].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)])
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j,'r-2',name='zonal',/overplot)
  
endfor

imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\phaseModZonZer.pdf', BORDER=10, RESOLUTION=350
imres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\phaseModZonZer.png', BORDER=10, RESOLUTION=350


end
