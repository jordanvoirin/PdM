; Script to analyse the data
;

sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\noise_study\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

nbrImgAveraging = []
results = []
for iFol = 0, Nfolders-1 do begin
  results = [results,phaseRetrieval(sFolderPaths[iFol]+'\')]

  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
  snbrImages = sepFolderPath[n_elements(sepFolderPath)-1]
  nbrImgAveraging = [nbrImgAveraging,long(snbrImages)]
endfor


nbrRows = Nfolders
nbrCol = 3

marge = 0.3

resDim = size(results[0].res.wavefront,/dimension)
imres = image(results[0].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[0]))+ ' Modal', MARGIN=marge,layout=[nbrCol,nbrRows,1])
zonDim = size(results[0].zon.wavefront,/dimension)
imzon = image(results[0].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,2])

jmax = max(results[0].res.j)
pres = plot(results[0].res.j,results[0].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,3])
pzon = plot(results[0].zon.j,results[0].zon.a_j,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pres, pzon])

for iFol = 1, Nfolders-1 do begin

  resDim = size(results[iFol].res.wavefront,/dimension)
  imres = image(results[iFol].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[iFol]))+ ' Modal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,iFol*2+iFol-2])
  zonDim = size(results[iFol].zon.wavefront,/dimension)
  imzon = image(results[iFol].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,iFol*2+iFol-1])

  jmax = max(results[iFol].res.j)
  pres = plot(results[iFol].res.j,results[iFol].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,iFol*2+iFol])
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j,'r-2',name='zonal',/overplot)

endfor

end
