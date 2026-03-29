import requests
from datetime import datetime
from pathlib import Path
import subprocess
import os

TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "SEU_CHAT_ID_AQUI"
inicio_execucao = datetime.now()

# --- Configurações ---
BASE_BACKUP = Path("/caminho/para/backup/BACKUP_SAMBA")
LOG = BASE_BACKUP / "backup.log"

PONTOS_DE_MONTAGEM = {
    "/mnt/publico": "//SERVIDOR_IP/publico",
    "/mnt/departamentos": "//SERVIDOR_IP/departamentos"
}

CREDENTIALS = "/caminho/credenciais/.smbcredentials"

DATA = datetime.now().strftime("%Y-%m-%d")

# --- Função de log ---
def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

# --- Verificação REAL de mount ---
def esta_montado(ponto):
    return subprocess.run(
        ["mountpoint", "-q", ponto]
    ).returncode == 0

# --- Montar SMB ---
def montar_smb(local, remoto):
    Path(local).mkdir(parents=True, exist_ok=True)

    if not esta_montado(local):
        try:
            subprocess.run([
                "sudo", "mount", "-t", "cifs",
                remoto, local,
                "-o",
                f"credentials={CREDENTIALS},vers=3.0,iocharset=utf8,noperm,serverino"
            ], check=True)
            log(f"Ponto {local} montado com sucesso.")
        except subprocess.CalledProcessError as e:
            log(f"ERRO ao montar {local}: {e}")
    else:
        log(f"Ponto {local} já está montado.")

# --- Lista arquivos modificados hoje ---
def arquivos_modificados_hoje(origem):
    hoje = datetime.today().date()
    arquivos = []
    for root, dirs, files in os.walk(origem):
        for file in files:
            caminho = Path(root) / file
            if datetime.fromtimestamp(caminho.stat().st_mtime).date() == hoje:
                arquivos.append(str(caminho.relative_to(origem)))
    return arquivos

# --- Função rsync incremental por data ---
def rsync_incremental(origem, destino_base):
    destino_base.mkdir(parents=True, exist_ok=True)
    destino = destino_base / DATA
    latest = destino_base / "latest"
    destino.mkdir(parents=True, exist_ok=True)

    arquivos = arquivos_modificados_hoje(origem)
    if not arquivos:
        return True

    arquivos_txt = destino_base / "arquivos_hoje.txt"
    with open(arquivos_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(arquivos))

    cmd = [
        "rsync",
        "-a",
        "--numeric-ids",
        "--human-readable",
        "--stats",
        "--ignore-errors",
        "--partial",
        f"--files-from={arquivos_txt}",
        f"--log-file={LOG}",
    ]

    if latest.exists():
        cmd.append(f"--link-dest={latest.resolve()}")

    cmd.extend([origem.rstrip("/") + "/", str(destino)])

    log(f"Iniciando backup incremental de {origem}")
    resultado = subprocess.run(cmd)
    if resultado.returncode != 0:
        log(f"ERRO no rsync em {origem}")
        return False

    log(f"Backup incremental concluído: {destino}")

    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(destino)

    return True

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)
    except Exception as e:
        log(f"Erro ao enviar Telegram: {e}")

# --- Script principal ---
print("Backups incrementais em andamento..⏳")
log("Backup incremental iniciado")
send_message("🚀 Backup incremental iniciado 🚀")

for local, remoto in PONTOS_DE_MONTAGEM.items():
    montar_smb(local, remoto)

ok1 = rsync_incremental("/mnt/publico", BASE_BACKUP / "publico")
ok2 = rsync_incremental("/mnt/departamentos", BASE_BACKUP / "departamentos")
status = "✅ Sucesso!" if ok1 and ok2 else "❌ Falhou!!"

log("Backup incremental finalizado")

fim_execucao = datetime.now()
duracao = fim_execucao - inicio_execucao

send_message(
    "Backup Servidor de Arquivos (SMB):\n\n"
    f"📦 Backup: {status}\n\n"
    f"⏱ Início: {inicio_execucao.strftime('%H:%M:%S')}\n"
    f"⏱ Fim: {fim_execucao.strftime('%H:%M:%S')}\n"
    f"⌛ Duração: {str(duracao).split('.')[0]}"
)

print("Backup incremental concluído. ✅")
