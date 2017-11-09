; script to analyze the response of diversity to an error in DeltaZ
; 

folderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\angle_study\cropped\40'
fileExt = '*.fits'


sigmaZ = 0.005d

;Get all the filenames containing the PSF data
sFilePaths = file_search(folderPath,'*.fits')
Nfiles =  n_elements(sFilePaths)
deltaZ = DINDGEN(Nfiles)

imgSizes = getImgSize(sFilePaths)

minSize = min(imgSizes[where(imgSizes ge 118)])

if minSize mod 2 ne 0 then begin
  minSize = minSize - 1
endif

print, 'Image size = ' + string(minSize) + 'x' + string(minSize)

psf = readfits(sFilePaths[0])
psfDim = size(psf,/dimension)

psfs = []
deltaZ = []

if psfDim[0] ge minSize and psfDim[1] ge minSize then begin

  ;get the deltaZ which is written in the filename
  sepFilePath = strsplit(sFilePaths[0],'\',/EXTRACT)
  sFile = sepFilePath[n_elements(sepFilePath)-1]
  sepsFile = strsplit(sFile,"_.",/EXTRACT)
  deltaZ = [deltaZ,double(sepsFile[n_elements(sepsFile)-2])/100]

  psfs=[[[psfs]],[[psf[psfDim[0]/2-minSize/2:psfDim[0]/2+minSize/2-1,psfDim[1]/2-minSize/2:psfDim[1]/2+minSize/2-1]]]]

endif else begin
  print, 'img0 is to small and is not taken into account for the phase retrieval'
endelse

;Treat filenames to get the focused or defocused property of the PSFs and fill the vector deltaZ of dimension M for the diversity.pro
for i = 1, n_elements(sFilePaths)-1 do begin

  psf = readfits(sFilePaths[i])
  psfDim = size(psf,/dimension)

  if psfDim[0] ge minSize and psfDim[1] ge minSize then begin

    ;get the deltaZ which is written in the filename
    sepFilePath = strsplit(sFilePaths[i],'\',/EXTRACT)
    sFile = sepFilePath[n_elements(sepFilePath)-1]
    sepsFile = strsplit(sFile,"_.",/EXTRACT)
    deltaZ = [deltaZ,double(sepsFile[n_elements(sepsFile)-2])/100]

    psfs=[[[psfs]],[[psf[psfDim[0]/2-minSize/2:psfDim[0]/2+minSize/2-1,psfDim[1]/2-minSize/2:psfDim[1]/2+minSize/2-1]]]]
  endif else begin
    print, 'img'+string(i)+' is to small and is not taken into account for the phase retrieval'
  endelse

endfor

;create all the permutations of -2,-1,1,2,0 ------------------------------------------------------------------------------
dimDeltaZ = size(deltaZ,/Dimensions)
n = dimDeltaZ[0]
permutations = []
arr = [0.d,2.d,1.d,-1.d,-2.d]
data = fltarr(n,1)
ix = 0
deltaZs = permutationWrep(arr,permutations,data,n,ix)

Npermut = (size(deltaZs,/Dimensions))[1]

for ip = 0,Npermut-1 do begin
  for iz = 0,dimDeltaZ[0]-1 do begin
    deltaZs[iz,ip] = deltaZ[iz] + sigmaZ*deltaZs[iz,ip]
  endfor
endfor



;Run diversity ---------------------------------------------------------------------------------------------

lambda = 0.6375d ;microns
threshold = 1e-3
D1=3.2*1e-3
D2=0.d
jmax = 231
pxSize = 5.3e-6
fdist = 80e-3
pxSizeArcSec = pxSize/fdist*!RADEG*3600.d

modalResults = []
zonalResults = []

for ip = 0,Npermut-1 do begin
  modalResults = [[ModalResults],[diversity(psfs,deltaZs[*,ip],lambda,fdist,pxSizeArcSec,threshold,'modal',d1=D1,d2=D2,jmax=jmax)]]
  zonalResults = [[zonalResults],[diversity(psfs,deltaZs[*,ip],lambda,fdist,pxSizeArcSec,threshold,'zonal',d1=D1,d2=D2,jmax=jmax)]]
endfor

;compute relevant statistical parameter ---------------------------------------------------------------------

xticks = []
ajModal = []
ajZonal = []
for ij = 0, n_elements(modalResults[0].j)-1 do begin
  tmpAjModal = []
  tmpAjZonal = []
  for ip = 0, Npermut-1 do begin
    tmpAjModal = [[tmpAjModal],[modalResults[ip].a_j[ij]*1000]]
    tmpAjZonal = [[tmpAjZonal],[zonalResults[ip].a_j[ij]*1000]]
  endfor
  ajModal = [ajModal,tmpAjModal]
  ajZonal = [ajZonal,tmpAjZonal]
  xticks = [xticks,modalResults[0].j[ij]]
endfor

ajModalstds = stddev2(ajModal,2)
ajZonalstds = stddev2(ajZonal,2)
Ajstds = [transpose(ajModalstds),transpose(ajZonalstds)]


;plotting ---------------------------------------------------------------------------------------------------

loadct,19, NCOLORS=Npermut

marge = 0.12

mplot = plot(modalResults[0].j,modalResults[0].a_j*1000,'b-0.5',xtitle='j',$
  ytitle = 'a_j [nm]',name = 'modal',margin = marge)
zplot = plot(zonalResults[0].j,zonalResults[0].a_j*1000,'r-0.5',xtitle='j',$
  ytitle = 'a_j [nm]',name = 'zonal',margin = marge,/overplot)
!null = LEGEND(target=[mplot, zplot])
for ip=1,Npermut-1 do begin
  mplot = plot(modalResults[ip].j,modalResults[ip].a_j*1000,/overplot)
  zplot = plot(zonalResults[ip].j,zonalResults[ip].a_j*1000,/overplot)
endfor

;A_j Boxplot
boxDataAjM = CREATEBOXPLOTDATA(ajModal)
boxDataAjZ = CREATEBOXPLOTDATA(ajZonal)
mboxes = boxplot(boxDataAjM,XTITLE="j", YTITLE="a_j [nm]",xtickname=['5','25','50','75','100','125','150','175','200','225']$
  ,xtickvalues=[1,21,46,71,96,121,146,171,196,221],XTICKINTERVAL=25,FILL_COLOR='white',color='blue',name='Modal', BACKGROUND_COLOR="light gray"$
  ,XRANGE=[-5,228],yrange=[-20,10])
zboxes = boxplot(boxDataAjZ,FILL_COLOR='white',color='red',name='Zonal',/overplot)
mboxes.THICK = 2
!null = LEGEND(target=[mboxes, zboxes])


mboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\errorDeltaZStudy\Boxplot_Aj_j.pdf', BORDER=10, RESOLUTION=350
mboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\errorDeltaZStudy\Boxplot_Aj_j.png', BORDER=10, RESOLUTION=350

;Stds Boxplot
boxDataStdAj = CREATEBOXPLOTDATA(Ajstds)
stdAjboxes = boxplot(boxDataStdAj,ytitle = 'std(a_j) [nm]',XTICKNAME = ['Modal', 'Zonal'],XTICKVALUES = [0,1]$
  ,FILL_COLOR='white', BACKGROUND_COLOR="light gray")
stdAjboxes.THICK = 2

stdAjboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\errorDeltaZStudy\Boxplot_stdAj.pdf', BORDER=10, RESOLUTION=350
stdAjboxes.save ,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\errorDeltaZStudy\Boxplot_stdAj.png', BORDER=10, RESOLUTION=350

end