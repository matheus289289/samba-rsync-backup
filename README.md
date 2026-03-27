# 🔄 Automação de Backup de Compartilhamentos Samba com Python

Este projeto automatiza o backup de compartilhamentos de rede SMB/CIFS utilizando Python, com suporte a:

* 📦 Backup completo (semanal)
* ⚡ Backup incremental (diário)
* 🗂️ Snapshots eficientes com hardlinks (rsync)

---

## 📌 Visão Geral

O sistema realiza:

1. Montagem automática de compartilhamentos Samba (SMB/CIFS)
2. Execução de backups utilizando `rsync`
3. Organização em snapshots por data
4. Otimização de espaço com hardlinks (`--link-dest`)
5. Registro detalhado de logs

---

## 🚀 Funcionalidades

### 🔹 Backup Completo (Full)

* Executado semanalmente
* Cópia integral dos dados
* Base para os incrementais

### 🔹 Backup Incremental

* Executado diariamente
* Copia apenas arquivos modificados no dia
* Utiliza `--files-from` + `--link-dest`
* Mantém histórico de versões por data

### 🔹 Outras Features

* Montagem automática de compartilhamentos SMB
* Logs persistentes das execuções
* Estrutura otimizada para recuperação de dados
* Compatível com ambientes Linux

---

## 🧰 Tecnologias Utilizadas

* Python 3
* rsync
* CIFS/SMB (cifs-utils)
* Linux (cron para automação)

---

## 📂 Estrutura do Projeto

```bash
backup/
├── backup_semanal.py        # Script de backup completo
├── backup_incremental.py    # Script de backup incremental
├── logs/
└── snapshots/
    ├── publico/
    └── departamentos/
```

---

## ⚙️ Requisitos

Sistema Linux com os seguintes pacotes instalados:

* Python 3
* rsync
* cifs-utils

### Instalação:

```bash
sudo apt update
sudo apt install rsync cifs-utils
```

---

## 🔄 Funcionamento do Backup Incremental

O script incremental executa o seguinte fluxo:

1. Monta os compartilhamentos SMB automaticamente
2. Identifica arquivos modificados no dia atual
3. Gera uma lista de arquivos modificados
4. Executa o `rsync` com:

   * `--files-from`
   * `--link-dest` (referência ao último backup)
5. Cria snapshot com data (YYYY-MM-DD)
6. Atualiza o symlink `latest`

---

## ⏱️ Automação e Agendamento

O projeto pode ser automatizado via `cron`.

### 📅 Backup Incremental Diário (recomendado)

```bash
0 1 * * * python3 /caminho/do/script/backup_incremental.py
```

Executa todos os dias às 01:00.

---

### 📦 Backup Completo Semanal

```bash
0 2 * * 0 python3 /caminho/do/script/backup_semanal.py
```

Executa todo domingo às 02:00.

---

### 🧠 Estratégia Recomendada

* Incremental diário → reduz perda de dados
* Full semanal → garante consistência completa

---

## 📈 Vantagens

* Redução de uso de armazenamento
* Backups mais frequentes
* Recuperação granular por data
* Baixo impacto na rede
* Estrutura escalável

---

## 🔮 Melhorias Futuras

* Integração com monitoramento (Zabbix)
* Alertas via Telegram
* Dashboard web de backups
* Política de retenção automática (limpeza de snapshots antigos)

---

## 🤝 Contribuição

Sugestões, melhorias e novas features são bem-vindas.

---

## 📌 Observação

Este projeto foi desenvolvido com foco em ambientes corporativos que utilizam compartilhamentos SMB, visando automação, confiabilidade e eficiência no processo de backup.
