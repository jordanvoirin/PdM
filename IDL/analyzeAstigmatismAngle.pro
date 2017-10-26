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
normAstAjres = []
normAstAjzon = []
a5res = []
a6res = []
a5zon = []
a6zon = []
defocAjres = []
defocAjzon = []
for iFol = 0, Nfolders-1 do begin
  a5res = [a5res,results[iFol].res.a_j[1]]
  a6res = [a6res,results[iFol].res.a_j[2]]
  a5zon = [a5zon,results[iFol].zon.a_j[1]]
  a6zon = [a6zon,results[iFol].zon.a_j[2]]
  normAstAjres = [astAjres,sqrt(results[iFol].res.a_j[1]*results[iFol].res.a_j[1]+results[iFol].res.a_j[2]*results[iFol].res.a_j[2])]
  normAstAjzon = [astAjzon,sqrt(results[iFol].zon.a_j[1]*results[iFol].zon.a_j[1]+results[iFol].zon.a_j[2]*results[iFol].zon.a_j[2])]
  defocAjres = [defocAjres,results[iFol].res.a_j[0]]
  defocAjzon = [defocAjzon,results[iFol].zon.a_j[0]]
endfor

sortedInd = sort(Angles)

OPDtot = (aberrationAstigmatismModel(1.49,1.4e-3,Angles[sortedInd]))*1e9

;plot Norm astigmatism vs. angle--------------------------------------------------------------------

pNAstAngleres = plot(Angles[sortedInd],normAstAjres[sortedInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Astigmatism Coef Norm [nm]',name='modal')
pNAstAnglezon = plot(Angles[sortedInd],normAstAjzon[sortedInd]*1000.d,'r-2',name='zonal',/overplot)
pNAstAnglemod = plot(Angles[sortedInd],OPDtot/sqrt(6)/2,'k-2',name='model',/overplot) ; factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
!null = LEGEND(target=[pNAstAngleres, pNAstAnglezon,pNastAnglemod],/DATA)
pNAstAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatismNorm_angle.pdf', BORDER=10, RESOLUTION=350
pNAstAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatismNorm_angle.png', BORDER=10, RESOLUTION=350

;plot astigmatism vs. angle------------------------------------------------------------------------

pA5Angleres = plot(Angles[sortedInd],abs(a5res[sortedInd]*1000.d),'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'astigmatism coef [nm]',name='a5 modal')
pA6Angleres = plot(Angles[sortedInd],abs(a6res[sortedInd]*1000.d),'b--2',name='a6 modal',/overplot)
pA5Anglezon = plot(Angles[sortedInd],abs(a5zon[sortedInd]*1000.d),'r-2',name='a5 zonal',/overplot)
pA6Anglezon = plot(Angles[sortedInd],abs(a6zon[sortedInd]*1000.d),'r--2',name='a6 zonal',/overplot)
pNAstAnglemod = plot(Angles[sortedInd],OPDtot/sqrt(6)/2,'k-2',name='model',/overplot); factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
!null = LEGEND(target=[pA5Angleres, pA6Angleres,pA5Anglezon,pA6Anglezon,pNAstAnglemod],/DATA)

pA5Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatism_angle.pdf', BORDER=10, RESOLUTION=350
pA5Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\astigmatism_angle.png', BORDER=10, RESOLUTION=350

; plot defocus coeff. vs. angle----------------------------------------------------------------------

pdefocAngleres = plot(Angles[sortedInd],defocAjres[sortedInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Defocus Coef [nm]',name='modal')
pdefocAnglezon = plot(Angles[sortedInd],defocAjzon[sortedInd]*1000.d,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pdefocAngleres, pdefocAnglezon],/DATA)
pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\defoc_angle.pdf', BORDER=10, RESOLUTION=350
pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\defoc_angle.png', BORDER=10, RESOLUTION=350


;Compare Phase and zernike modal vs. zonal-----------------------------------------------------------
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
;!null = LEGEND(target=[pres, pzon])

for iFol = 1, Nfolders-1 do begin
  
  resDim = size(results[iFol].res.wavefront,/dimension)
  imres = image(results[iFol].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title=string(long(Angles[iFol]))+ ' Modal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-2])
  zonDim = size(results[iFol].zon.wavefront,/dimension)
  imzon = image(results[iFol].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-1])
  
  jmax = max(results[iFol].res.j)
  pres = plot(results[iFol].res.j,results[iFol].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)])
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j,'r-2',name='zonal',/overplot)
  
endfor

imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\phaseModZonZer.pdf', BORDER=10, RESOLUTION=350
imres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study\phaseModZonZer.png', BORDER=10, RESOLUTION=350


end
