from datetime import datetime
from pathlib import Path
import subprocess
import os

# --- Configurações ---
BASE_BACKUP = Path("/caminho-do-backup") #-- caminho onde será salvo o seu backup --*
LOG = BASE_BACKUP / "backup.log"

PONTOS_DE_MONTAGEM = {
    "/mnt/share_public": "//fileserver.local/public",  #--montar as pastas para copiar
    "/mnt/share_departments": "//fileserver.local/departments" 
}

CREDENTIALS = "/root/.smbcredentials"

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

# --- Função rsync snapshot ---
def rsync_snapshot(origem, destino_base):
    destino_base.mkdir(parents=True, exist_ok=True)

    destino = destino_base / DATA
    latest = destino_base / "latest"

    destino.mkdir(parents=True, exist_ok=True)

    cmd = [
        "rsync",
        "-a",
        "--delete",
        "--numeric-ids",
        "--human-readable",
        "--stats",
        "--ignore-errors",
        "--partial",
        f"--log-file={LOG}",
    ]

    if latest.exists():
        cmd.append(f"--link-dest={latest.resolve()}")

    cmd.extend([
        origem.rstrip("/") + "/",
        str(destino)
    ])

    log(f"Iniciando rsync snapshot de {origem}")
    subprocess.run(cmd, check=False)
    log(f"Snapshot concluído: {destino}")

    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(destino)

# --- Script principal ---
print("Backups em andamento..⏳")
log("Backup iniciado")

# Montagem dos compartilhamentos
for local, remoto in PONTOS_DE_MONTAGEM.items():
    montar_smb(local, remoto)

# --- Backups ---
rsync_snapshot("/mnt/share_public", BASE_BACKUP / "public")
rsync_snapshot("/mnt/share_departments", BASE_BACKUP / "departments")

log("Backup finalizado")
print("Backup concluído com snapshots. ✅")
