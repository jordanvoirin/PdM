; Script to analyse the astigmatism data and comparison to the SHwfs
;
;
;instanciate folderPath------------------------------------------------------------------------
sPDwthfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\angle_study_2\wth\cropped\*'
sPDwoutfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\angle_study_2\wout\cropped\'

sSHwthfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\astigmatism\wth\*'
sSHwoutfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\astigmatism\wout\'

sPDwthFolderPaths = file_search(sPDwthfolderPath,/Test_Directory)
sSHwthFolderPaths = file_search(sSHwthfolderPath,/Test_Directory)

jmax = 66

;run phaseretrieval and readandaverage on wout files
PDwoutResult = phaseretrieval(sPDwoutfolderPath,jmax,1,1)
SHwoutResult = readAndAverageSHdata(sSHwoutfolderPath)

;run phaseRetrieval----------------------------------------------------------------------------
NPDfolders =  n_elements(sPDwthFolderPaths)
AnglesPD = []
resultsPD = list()
for iFol = 0, NPDfolders-1 do begin
  result = phaseRetrieval(sPDwthFolderPaths[iFol]+'\',jmax,1,1)
  result.res.a_j  = result.res.a_j - PDwoutResult.res.a_j
  result.res.wavefront  = result.res.wavefront - PDwoutResult.res.wavefront
  result.zon.a_j  = result.zon.a_j - PDwoutResult.zon.a_j
  result.zon.wavefront  = result.zon.wavefront - PDwoutResult.zon.wavefront
  resultsPD.add,result
  
  sepFolderPath = strsplit(sPDwthFolderPaths[iFol],'\',/EXTRACT)
  sAngle = sepFolderPath[n_elements(sepFolderPath)-1]
  AnglesPD = [AnglesPD,double(sAngle)]
endfor

;run SHwfs read and average----------------------------------------------------------------------
NSHfolders =  n_elements(sSHwthFolderPaths)
AnglesSH = []
resultsSH = list()
for iFol = 0, NSHfolders-1 do begin
  result = readAndAverageSHdata(sSHwthFolderPaths[iFol]+'\')
  result.zernike[3,*] = result.zernike[3,*] - SHwoutResult.zernike[3,*]
  result.wavefront = result.wavefront - SHwoutResult.wavefront
  result.zernike = toNoll(result.zernike)
  resultsSH.add,result
  
  sepFolderPath = strsplit(sSHwthFolderPaths[iFol],'\',/EXTRACT)
  sAngle = sepFolderPath[n_elements(sepFolderPath)-1]
  AnglesSH = [AnglesSH,double(sAngle)]
endfor


;get the PD zernike coefficient----------------------------------------------------------------------

a8res = []
a6res = []
a8zon = []
a6zon = []
defocAjres = []
defocAjzon = []
for iFol = 0, NPDfolders-1 do begin
  a8res = [a8res,resultsPD[iFol].res.a_j[4]]
  a6res = [a6res,resultsPD[iFol].res.a_j[2]]
  a8zon = [a8zon,resultsPD[iFol].zon.a_j[4]]
  a6zon = [a6zon,resultsPD[iFol].zon.a_j[2]]
  defocAjres = [defocAjres,resultsPD[iFol].res.a_j[0]]
  defocAjzon = [defocAjzon,resultsPD[iFol].zon.a_j[0]]
endfor

sortedPDInd = sort(AnglesPD)

;get the SH zernike coefficient----------------------------------------------------------------------

a8SH = []
a6SH = []
defocAjSH = []

for iFol = 0, NSHfolders-1 do begin
  a8SH = [a8SH,resultsSH[iFol].zernike[3,7]]
  a6SH = [a6SH,resultsSH[iFol].zernike[3,5]]
  defocAjSH = [defocAjSH,resultsSH[iFol].zernike[3,3]]
endfor

sortedSHInd = sort(AnglesSH)
;Zemax Data ------------------------------------------------------------------------------------------
AnglesModel = [10,20,30,40,50]

;aberrationsModel = (aberrationParallelPlateModel(1.49,1.4e-3,AnglesModel))*1e9

zemaxA6Aberration = [-0.00141287,-0.00556993,-0.01286776,-0.02344080,-0.03689211]*637.5
zemaxA8Aberration = [0.00057350,0.00118594,0.00187701,0.00268449,0.00364058]*637.5

;thZernikeCoef6 = aberrationsModel[*,0]/sqrt(6)/2; factor sqrt(6) to normalize to zernike and /2 to pass from P2V to coef
;thZernikeCoef8 = aberrationsModel[*,1]/sqrt(8)/2;


;search of a scale factor and offset of the SH data

fitResult = linfit(a6SH[sortedSHInd]*1000.d,zemaxA6Aberration, CHISQR = chisqr,covar = covar, prob = prob, sigma = sigma, yfit = yfit)

print, 'a, b:', fitResult
print, 'Chisqr: ', chisqr
print, 'standard errors: ', sigma 

;plot aberrations vs. angle------------------------------------------------------------------------

rmseA6mod = RMSE(zemaxA6Aberration,a6res[sortedPDInd]*1000.d)
rmseA6zon = RMSE(zemaxA6Aberration,a6zon[sortedPDInd]*1000.d)
rmseA6sh = RMSE(zemaxA6Aberration,a6SH[sortedSHInd]*1000.d)

rmseA8mod = RMSE(zemaxA8Aberration,a8res[sortedPDInd]*1000.d)
rmseA8zon = RMSE(zemaxA8Aberration,a8zon[sortedPDInd]*1000.d)
rmseA8sh = RMSE(zemaxA8Aberration,a8SH[sortedSHInd]*1000.d)

pA6Angleres = plot(AnglesPD[sortedPDInd],a6res[sortedPDInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',$
  ytitle = 'a6 [nm]',name='modal RMSE = '+string(rmseA6mod))
pA6Anglezon = plot(AnglesPD[sortedPDInd],a6zon[sortedPDInd]*1000.d,'r-2',name='zonal RMSE = ' + string(rmseA6zon),/overplot)
;pA6Anglesh = plot(AnglesSH[sortedSHInd],a6SH[sortedSHInd]*1000.d,'g-2',name='SH RMSE = ' + string(rmseA6sh),/overplot)
;pA6Angleshfit = plot(AnglesSH[sortedSHInd],yfit[sortedSHInd],'y-2',name='SH fitted',/overplot)

;pAstAnglemod = plot(AnglesModel,thZernikeCoef6,'k-2',name='model',/overplot); factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
pAstAnglezemax = plot(AnglesModel,zemaxA6Aberration,'k--2',name='zemax',/overplot)
!null = LEGEND(target=[pA6Angleres,pA6Anglezon],/DATA);,pA6Anglesh,pAstAnglezemax],/DATA)

pA6Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\astigmatism_angle.pdf', BORDER=10, RESOLUTION=350
pA6Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\astigmatism_angle.png', BORDER=10, RESOLUTION=350

pA8Angleres = plot(AnglesPD[sortedPDInd],abs(a8res[sortedPDInd]*1000.d),'b-2',xtitle='Parallel Faces Angle [deg]',$
  ytitle = 'a8 [nm]',name='modal RMSE = '+string(rmseA8mod))
pA8Anglezon = plot(AnglesPD[sortedPDInd],abs(a8zon[sortedPDInd]*1000.d),'r-2',name='zonal RMSE = '+string(rmseA8zon),/overplot)
pA8Anglesh = plot(AnglesSH[sortedSHInd],abs(a8SH[sortedSHInd]*1000.d),'g-2',name='SH RMSE = '+string(rmseA8sh),/overplot)
;pA8Anglemod = plot(Angles[sortedInd],thZernikeCoef8,'k-2',name='model',/overplot); factor sqrt(6) to pass from seidel to zernike and /2 to pass from P2V to coef
pA8Anglezemax = plot(AnglesModel,zemaxA8Aberration,'k--2',name='zemax',/overplot)
!null = LEGEND(target=[pA8Angleres, pA8Anglezon,pA8Anglesh,pA8Anglezemax],/DATA)

;pA8Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\coma_angle.pdf', BORDER=10, RESOLUTION=350
;pA8Angleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\coma_angle.png', BORDER=10, RESOLUTION=350

; plot defocus coeff. vs. angle----------------------------------------------------------------------

;pdefocAngleres = plot(AnglesPD[sortedPDInd],defocAjres[sortedPDInd]*1000.d,'b-2',xtitle='Parallel Faces Angle [deg]',ytitle = 'Defocus Coef [nm]',name='modal')
;pdefocAnglezon = plot(AnglesPD[sortedPDInd],defocAjzon[sortedPDInd]*1000.d,'r-2',name='zonal',/overplot)
;pdefocAnglesh = plot(AnglesSH[sortedSHInd],defocAjsh[sortedSHInd]*1000.d,'g-2',name='SH',/overplot)
;!null = LEGEND(target=[pdefocAngleres,pdefocAnglezon,pdefocAnglesh],/DATA)
;pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\defoc_angle.pdf', BORDER=10, RESOLUTION=350
;pdefocAngleres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\defoc_angle.png', BORDER=10, RESOLUTION=350


;Compare Phase and zernike modal vs. zonal-----------------------------------------------------------

marge = 0.3
;modwavefront = resultsPD[0].res.wavefront[*,*]*1000
;zonwavefront = resultsPD[0].zon.wavefront[*,*]*1000
;shwavefront = resultsSH[0].wavefront[*,*]*1000
;resDim = size(modwavefront,/dimension)
;imres = image(modwavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],min_value=minvalue,max_value = maxValue, $
;  title=string(long(AnglesPD[0]))+ ' Modal', MARGIN=marge,layout=[nbrCol,nbrRows,1])
;zonDim = size(zonwavefront,/dimension)
;imzon = image(zonwavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],min_value=minvalue,max_value = maxValue $
;  ,title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,2])
;shDim = size(shwavefront,/dimension)
;imsh = image(shwavefront,rgb_table=34,image_dimensions=shDim,xrange=[0,shDim[0]],yrange=[0,shDim[1]],min_value=minvalue,max_value = maxValue $
;    ,title='SH', MARGIN=marge,/current,layout=[nbrCol,nbrRows,3])
;jmax = max(resultsPD[0].res.j)
;pres = plot(resultsPD[0].res.j,resultsPD[0].res.a_j*1000,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j [nm]',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,4])
;pzon = plot(resultsPD[0].zon.j,resultsPD[0].zon.a_j*1000,'r-2',name='zonal',/overplot)
;psh = plot(resultsSH[0].zernike[0,*],resultsSH[0].zernike[3,*]*1000,'k-2',name='sh',/overplot)

;!null = LEGEND(target=[pres, pzon])


folderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\zemax\wavefronts\'

files = file_search(folderPath+'*.txt')

Nfiles = n_elements(files)
zemaxWavefronts=[]
zemaxAngle = []
for ifile = 0, Nfiles-1 do begin
  sepFilePath = strsplit(files[ifile],'\',/EXTRACT)
  sFile = sepFilePath[n_elements(sepFilePath)-1]
  sepsFile = strsplit(sFile,"_.",/EXTRACT)
  zemaxAngle = [zemaxAngle,double(sepsFile[n_elements(sepsFile)-2])/100]

  rfileData = READ_ASCII(files[ifile], DATA_START=16)
  zemaxWavefronts = [[[zemaxWavefronts]],[[rfileData.Field001*637.5]]]
endfor

for iFol = 0, NPDfolders-1 do begin
  modwavefront = resultsPD[iFol].res.wavefront[*,*]*1000
  ;zonwavefront = resultsPD[iFol].zon.wavefront[*,*]*1000
  zemaxwavefront = zemaxWavefronts[iFol]
  minValue = min([modwavefront,zemaxwavefront])
  maxValue = max([modwavefront,zemaxwavefront])
  resDim = size(modwavefront,/dimension)
  imres = image(modwavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]]$
    ,title='Modal, angle = '+string(long(AnglesPD[iFol])), MARGIN=marge,min_value=minvalue,max_value = maxValue $
    ,/current,layout=[3,1,1])
  zemaxDim = size(zemaxwavefront,/dimension)
  imzemax = image(zemaxwavefront,rgb_table=34,image_dimensions=shDim,xrange=[0,shDim[0]],yrange=[0,shDim[1]],min_value=minvalue,max_value = maxValue $
    ,title='Zemax', MARGIN=marge,/current,layout=[3,1,2])
  diffim = image(modwavefront-zemaxwavefront,rgb_table=34,image_dimensions=shDim,xrange=[0,shDim[0]],yrange=[0,shDim[1]],min_value=minvalue,max_value = maxValue $
    , MARGIN=marge,/current,layout=[3,1,3])
  c = COLORBAR(TARGET=imres, ORIENTATION=1,TITLE='[nm]',range=[minValue,maxValue])

endfor

;imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\phaseModZonZer.pdf', BORDER=10, RESOLUTION=350
;imres.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\astigmatism\angle_study_2\phaseModZonZer.png', BORDER=10, RESOLUTION=350


end
