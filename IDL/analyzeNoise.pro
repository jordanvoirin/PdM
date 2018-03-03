; Script to analyse the noise data
;

;instanciate folderPath------------------------------------------------------------------------
sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\noise_study\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

;get the vector of nbrImgAveraging-------------------------------------------------------------
nbrImgAveraging = []
for iFol = 0, Nfolders-1 do begin
sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
snbrImages = sepFolderPath[n_elements(sepFolderPath)-1]
nbrImgAveraging = [nbrImgAveraging,long(snbrImages)]
endfor

indSorted = sort(nbrImgAveraging)
nbrImgAveraging = nbrImgAveraging[indSorted]

;run phaseRetrieval----------------------------------------------------------------------------
results = []
for iFol = 0, Nfolders-1 do begin
  results = [results,phaseRetrieval(sFolderPaths[indsorted[iFol]]+'\', 200,1,1)]
endfor



;Compare Phase and zernike modal vs. zonal------------------------------------------------------
nbrRows = Nfolders
nbrCol = 3

marge = 0.0

resDim = size(results[0].res.wavefront,/dimension)
imres = image(results[0].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
  yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[0]))+ ' Modal', MARGIN=marge,layout=[nbrCol,nbrRows,1])
zonDim = size(results[0].zon.wavefront,/dimension)
imzon = image(results[0].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],$
  yrange=[0,zonDim[1]],title='Zonal', MARGIN=marge,/current,layout=[nbrCol,nbrRows,2])

jmax = max(results[0].res.j)
pres = plot(results[0].res.j,results[0].res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j',$
  name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,3])
pzon = plot(results[0].zon.j,results[0].zon.a_j,'r-2',name='zonal',/overplot)
!null = LEGEND(target=[pres, pzon])

for iFol = 1, Nfolders-1 do begin
  resDim = size(results[iFol].res.wavefront,/dimension)
  imres = image(results[iFol].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
    yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[iFol])), MARGIN=marge,/current,$
    layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-2])
  zonDim = size(results[iFol].zon.wavefront,/dimension)
  imzon = image(results[iFol].zon.wavefront,rgb_table=34,image_dimensions=zonDim,xrange=[0,zonDim[0]],$
    yrange=[0,zonDim[1]], MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)-1])

  jmax = max(results[iFol].res.j)
  pres = plot(results[iFol].res.j,results[iFol].res.a_j,'b-2',xtitle='Zernike polynome j',$
    ytitle = 'a_j',name='modal',xrange = [4,jmax], MARGIN=marge,/current,layout=[nbrCol,nbrRows,(iFol+1)*2+(iFol+1)])
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j,'r-2',name='zonal',/overplot)
endfor


;Compare zernike coefficient between all different averaging image number ----------------------------
pres = plot(results[0].res.j,results[0].res.a_j*1000,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j [nm]',$
 name='modal',xrange = [4,jmax])
pzon = plot(results[0].zon.j,results[0].zon.a_j*1000,'r-2',name='zonal',xrange = [4,jmax],/overplot)
!null = LEGEND(target=[pres, pzon])
iFol = 0
for iFol = 1, Nfolders-1 do begin
  pres = plot(results[iFol].res.j,results[iFol].res.a_j*1000,'b-2',/current,/overplot)
  pzon = plot(results[iFol].zon.j,results[iFol].zon.a_j*1000,'r-2',/current,/overplot)
endfor

;Boxplot 

xticks = []
ajModal = []
ajZonal = []
for ij = 0, n_elements(results[0].res.j)-1 do begin
  tmpAjModal = []
  tmpAjZonal = []
  for iFol = 0, Nfolders-1 do begin
    tmpAjModal = [[tmpAjModal],[results[iFol].res.a_j[ij]*1000]]
    tmpAjZonal = [[tmpAjZonal],[results[iFol].zon.a_j[ij]*1000]]
  endfor
  ajModal = [ajModal,tmpAjModal]
  ajZonal = [ajZonal,tmpAjZonal]
  xticks = [xticks,results[0].res.j[ij]]
endfor

ajModalstds = stddev2(ajModal,2)
ajZonalstds = stddev2(ajZonal,2)
Ajstds = [transpose(ajModalstds),transpose(ajZonalstds)]

;A_j Boxplot
boxDataAjM = CREATEBOXPLOTDATA(ajModal)
boxDataAjZ = CREATEBOXPLOTDATA(ajZonal)
mboxes = boxplot(boxDataAjM,XTITLE="j", YTITLE="aj [nm]",xtickname=['5','25','50','75','100','125','150','175','200','225']$
  ,xtickvalues=[1,21,46,71,96,121,146,171,196,221],XTICKINTERVAL=25,FILL_COLOR='white',color='blue',name='Modal', BACKGROUND_COLOR="light gray")
zboxes = boxplot(boxDataAjZ,FILL_COLOR='white',color='red',name='Zonal',/overplot)
mboxes.THICK = 2
!null = LEGEND(target=[mboxes, zboxes])

mboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\Boxplot_Aj_j_jmax200.pdf', BORDER=5, RESOLUTION=350
mboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\Boxplot_Aj_j_jmax200.png', BORDER=5, RESOLUTION=350


;Compare wavefront 
resDim = size(results[0].res.wavefront,/dimension)
imres = image(results[0].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
  yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[0]))+ ' Modal', MARGIN=marge,layout=[2,1,1])
resDim = size(results[NFolders-5].res.wavefront,/dimension)
imres = image(results[NFolders-5].res.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
  yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[NFolders-5])), MARGIN=marge,/current,$
  layout=[2,1,2])
  
;imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\WavefrontCompModaljmax30.pdf', BORDER=10, RESOLUTION=350
;imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\WavefrontCompModaljmax30.png', BORDER=10, RESOLUTION=350

zonDim = size(results[0].zon.wavefront,/dimension)
imzon = image(results[0].zon.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
  yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[0]))+ ' Zonal', MARGIN=marge,layout=[2,1,1])
zonDim = size(results[NFolders-5].zon.wavefront,/dimension)
imzon = image(results[NFolders-5].zon.wavefront,rgb_table=34,image_dimensions = resDim,xrange=[0,resDim[0]],$
  yrange=[0,resDim[1]],title=string(long(nbrImgAveraging[NFolders-5])), MARGIN=marge,/current,$
  layout=[2,1,2])
  
;imzon.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\WavefrontCompZonaljmax30.pdf', BORDER=10, RESOLUTION=350
;imres.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\noise_study\WavefrontCompZonaljmax30.png', BORDER=10, RESOLUTION=350

end
