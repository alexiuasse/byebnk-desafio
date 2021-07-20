# byebnk-desafio

## Considerações

Apesar do teste ser somente a criação de API eu fiz um sistema com um frontend, criei 3 usuários sendo eles:

1. *admin* *admin123* - superusuário
2. *teste1* *T35t31234* - usuário comum
3. *teste2* *T35t31234* - usuário comum

A api se encontra em:

-financial
    - rest_views.py
    - test.py
    - models.py
    - serializers.py

### A respeitos do item 1 (Cadastrar ativos)

Eu adicionei a normalização do nome do ativo, sendo que a primeira letra será em maiúsculo e o resto em minúsculo. Tamém adicionei a verificação de um ativo já estar cadastrado a api retornará um erro informando que já tem um ativo com mesmo nome cadastrado.

### A respeito do item 3 (Visualizar o saldo da sua carteira de investimentos) 

Eu coloquei a carteira para ser mostrada na página do Dashboard com um gráfico em pizza.
