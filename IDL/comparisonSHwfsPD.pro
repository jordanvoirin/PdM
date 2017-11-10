;script to compare the SH wfs results and the PD results
;

PDwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wth\cropped\'
PDwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wout\cropped\'

SHwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wth\'
SHwthPSfilePath = file_search('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wth\*.csv')
SHwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wout\'
SHwoutPSfilePath = file_search('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wout\*.csv')


jmax = 66
PDwthPSresult = phaseretrieval(PDwthPSfolderPath,jmax,1,1)
PDwoutPSresult = phaseretrieval(PDwoutPSfolderPath,jmax,1,1)

pdPSresult = PDwthPSresult

SHwthPSresult = readshwfsdata(SHwthPSfilePath)
SHwoutPSresult = readshwfsdata(SHwoutPSfilePath)

shPSresult = SHwthPSresult

;Correct for background aberration ------------------------------------------------------------------------------

pdPSresult.res.a_j = (PDwthPSresult.res.a_j -  PDwoutPSresult.res.a_j)*1000
pdPSresult.zon.a_j = (PDwthPSresult.zon.a_j -  PDwoutPSresult.zon.a_j)*1000

pdPSresult.res.wavefront = (PDwthPSresult.res.wavefront -  PDwoutPSresult.res.wavefront)*1000
pdPSresult.zon.wavefront = (PDwthPSresult.zon.wavefront -  PDwoutPSresult.zon.wavefront)*1000

shPSresult.zernike.coefficient = (SHwthPSresult.zernike.coefficient-SHwoutPSresult.zernike.coefficient)*1000
shPSresult.wavefront = (SHwthPSresult.wavefront-SHwoutPSresult.wavefront)*1000
;plotting --------------------------------------------------------------------------------
marge = 0.12

;Zernike

pdMplot = plot(pdPSresult.res.j,pdPSresult.res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j [nm]',$
  name='PD modal',xrange = [4,jmax], MARGIN=marge)
pdZplot = plot(pdPSresult.zon.j,pdPSresult.zon.a_j,'r-2',/overplot,$
  name='PD zonal')
pdSHplot = plot(shPSresult.zernike.index,shPSresult.zernike.coefficient,'k-2',/overplot,$
    name='SH')

; Wavefront

abmin=-500
abmax=500


pdMim = image(PDPSresult.res.wavefront,rgb_table=34,min_value=abmin,max_value = abmax,title='PD Modal',position=[0.05,0.55,0.45,0.95])
pdZim = image(PDPSresult.zon.wavefront,rgb_table=34,min_value=abmin,max_value = abmax,title='PD Zonal',/current,position=[0.55,0.55,.95,.95])
pdSHim = image(flipmatrix(shPSresult.wavefront),rgb_table=34,min_value=abmin,max_value = abmax,title='SH',/current,position=[0.33,0.05,.73,.45])
c = COLORBAR(TARGET=pdMim, ORIENTATION=1,position=[.52,.55,.545,.95],TITLE='[nm]',range=[abmin,abmax])

end