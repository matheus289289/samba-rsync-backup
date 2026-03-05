# Automação de Backup de Compartilhamentos Samba com Python

Este projeto automatiza o backup de compartilhamentos de rede SMB/CIFS utilizando Python e snapshots incrementais com rsync.

O script monta automaticamente os compartilhamentos Samba, executa backups incrementais e mantém um histórico de snapshots utilizando hardlinks para otimizar o uso de espaço em disco.

## Funcionalidades

- Montagem automática de compartilhamentos SMB
- Backups incrementais utilizando rsync
- Snapshots eficientes utilizando hardlinks
- Registro de logs das operações de backup
- Compatível com ambientes Linux

## Requisitos

Sistema Linux com os seguintes pacotes instalados:

- Python 3
- rsync
- cifs-utils

Instalação das dependências:

```bash
sudo apt install rsync cifs-utils
```

## Automação e Agendamento

Este script pode ser agendado para executar automaticamente em dias e horários específicos de acordo com a necessidade do ambiente.

Em sistemas Linux, isso pode ser feito utilizando o **cron**, permitindo a execução periódica do backup sem intervenção manual.

Exemplo de agendamento semanal:

0 2 * * 0 python3 /caminho/do/script/backup_samba.py

Nesse exemplo, o backup será executado todo **domingo às 02:00 da manhã**.

Outros exemplos de agendamento:

Executar todos os dias às 01:00:

0 1 * * * python3 /caminho/do/script/backup_samba.py

Executar toda segunda-feira às 03:00:

0 3 * * 1 python3 /caminho/do/script/backup_samba.py


