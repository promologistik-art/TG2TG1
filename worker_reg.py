"""Регистрация клона и привязок пользователей через общие файлы в /app/shared"""
import json
import os
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

WORKERS_FILE = os.path.join(Config.DATA_DIR, "workers.json")
BINDINGS_FILE = os.path.join(Config.DATA_DIR, "bindings.json")


def register_self():
    """Записывает этого клона в общий реестр workers.json"""
    workers = {}
    
    if os.path.exists(WORKERS_FILE):
        try:
            with open(WORKERS_FILE, "r") as f:
                workers = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read workers.json: {e}")
            workers = {}
    
    worker_key = f"{Config.BOT_TYPE}_{Config.CLONE_ID}"
    
    workers[worker_key] = {
        "bot_type": Config.BOT_TYPE,
        "clone_id": Config.CLONE_ID,
        "bot_username": Config.BOT_USERNAME,
        "db_path": Config.DB_PATH,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    try:
        with open(WORKERS_FILE, "w") as f:
            json.dump(workers, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Registered in workers.json: {worker_key}")
    except Exception as e:
        logger.error(f"Failed to write workers.json: {e}")


def save_user_binding(head_user_id: int, worker_user_id: int):
    """Сохраняет привязку: пользователь KontentFabrik → пользователь в клоне"""
    bindings = {}
    
    if os.path.exists(BINDINGS_FILE):
        try:
            with open(BINDINGS_FILE, "r") as f:
                bindings = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read bindings.json: {e}")
            bindings = {}
    
    bindings[str(head_user_id)] = {
        "head_user_id": head_user_id,
        "worker_user_id": worker_user_id,
        "bot_type": Config.BOT_TYPE,
        "clone_id": Config.CLONE_ID,
        "db_path": Config.DB_PATH,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    try:
        with open(BINDINGS_FILE, "w") as f:
            json.dump(bindings, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Binding saved: head={head_user_id} → clone {Config.CLONE_ID}")
    except Exception as e:
        logger.error(f"Failed to write bindings.json: {e}")