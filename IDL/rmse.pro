function RMSE, estimator,true

Nestimator = n_elements(estimator)
Ntrue = n_elements(true)


MSE = 0
if Nestimator eq Ntrue then begin
  for ie = 0,Nestimator-1 do begin
    MSE += (estimator[ie]-true[ie])*(estimator[ie]-true[ie])
  endfor
endif

return, sqrt(MSE/Nestimator)
end