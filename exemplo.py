from omie import Omie


exemplo = Omie("EmpresaTeste").ListarContasPagar


exemplo.registros_por_pagina = 2
exemplo.pagina = 5

exec = exemplo.executar()

print(exec)

