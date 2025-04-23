from fastapi import APIRouter, Depends
from utils.auth import verify_key
import platform, socket, psutil, time, os
import getpass

router = APIRouter()


@router.get("/", dependencies=[Depends(verify_key)])
def get_system_info():
    try:
        try:
            current_user = getpass.getuser()
        except Exception:
            current_user = os.getenv("USER") or os.getenv(
                "USERNAME") or "unknown"

        try:
            cpu_usage = psutil.cpu_percent(interval=1)
        except Exception:
            cpu_usage = None

        try:
            mem_info = psutil.virtual_memory()
            memory_total = round(mem_info.total / 1e9, 2)
            memory_percent = mem_info.percent
        except Exception:
            memory_total = None
            memory_percent = None

        try:
            disk_percent = psutil.disk_usage("/").percent
        except Exception:
            disk_percent = None

        try:
            uptime = time.time() - psutil.boot_time()
        except Exception:
            uptime = None

        return {
            "os": platform.system(),
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
            "architecture": platform.machine(),
            "cpu": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "cpu_threads": psutil.cpu_count(logical=True),
            "cpu_usage_percent": cpu_usage,
            "memory_total_gb": memory_total,
            "memory_usage_percent": memory_percent,
            "disk_usage_percent": disk_percent,
            "uptime_seconds": uptime,
            "current_user": current_user
        }
    except Exception as e:
        return {"error": str(e)}
