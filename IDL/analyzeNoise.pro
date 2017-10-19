; Script to analyse the data
;

sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\noise_study\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

nbrImages = []
results = []
for iFol = 0, Nfolders-1 do begin

  results = [results,phaseRetrieval(sFolderPaths[iFol]+'\')]

;  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
;  snbrImages = sepFilePath[n_elements(sepFolderPath)-1]/100
;  nbrImages = [Angles,double(sAngle)]

  resDim = size(results[iFol].res.wavefront,/dimension)
  imres = image(results[iFol].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title='Modal', MARGIN=0,layout=[2,1,1])
  zonDim = size(results[iFol].zon.wavefront,/dimension)
  imzon = image(results[iFol].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=0,/current,layout=[2,1,2])

  pres = plot(results[iFol].res.j,result.res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax])
  pzon = plot(results[iFol].zon.j,result.zon.a_j,'r-2',name='zonal',/overplot)
  !null = LEGEND(target=[pres, pzon])

endfor

end
