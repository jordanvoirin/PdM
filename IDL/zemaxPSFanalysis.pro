;script to try diversity with zemax PSF

folderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\zemax\30\'

files = file_search(folderPath+'*.txt')

Nfiles = n_elements(files)
psfs=[]
deltaz = []
for ifile = 0, Nfiles-1 do begin
  sepFilePath = strsplit(files[ifile],'\',/EXTRACT)
  sFile = sepFilePath[n_elements(sepFilePath)-1]
  sepsFile = strsplit(sFile,"_.",/EXTRACT)
  deltaZ = [deltaZ,double(sepsFile[n_elements(sepsFile)-2])/100]
  
  rfileData = READ_ASCII(files[ifile], DATA_START=18)
  psfs = [[[psfs]],[[rfileData.Field001]]]
endfor

;Run diversity
lambda = 0.6375d ;microns
threshold = 1e-3
D1=3.2*1e-3
D2=0.d
jmax = jmax
pxSize = 5.45e-6
fdist = 80e-3
pxSizeArcSec = pxSize/fdist*!RADEG*3600.d

res = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'modal',d1=D1,d2=D2,jmax=jmax)
zon = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'zonal',d1=D1,d2=D2,jmax=jmax)

results = {res:res,zon:zon}

a8res = results.res.a_j[4]*1000
a6res = results.res.a_j[2]*1000
a8zon = results.zon.a_j[4]*1000
a6zon = results.zon.a_j[2]*1000
defocAjres = results.res.a_j[0]*1000
defocAjzon = results.zon.a_j[0]*1000


end
