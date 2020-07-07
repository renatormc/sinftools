cmd /c "$($args[0])"
if($?) {
   Write-Output "SINF: Processo finalizado com sucesso!"
}else {
   Write-Output "SINF: Erro!"
}
exit