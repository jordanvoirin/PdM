function Power, number, power
tmpnumber = number
for ip = 1,power-1 do begin
  tmpnumber = tmpnumber*number
endfor

return, tmpnumber

end