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
