import psutil
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_memory_stats() -> Dict[str, Any]:
    """Get current memory usage stats for this process and system."""
    process = psutil.Process(os.getpid())
    
    # Memory info
    mem_info = process.memory_info()
    memory_percent = process.memory_percent()
    
    # System memory
    sys_mem = psutil.virtual_memory()
    
    return {
        "process_rss_mb": mem_info.rss / 1024 / 1024,  # Resident Set Size
        "process_vms_mb": mem_info.vms / 1024 / 1024,  # Virtual Memory Size
        "process_percent": memory_percent,
        "system_available_mb": sys_mem.available / 1024 / 1024,
        "system_percent": sys_mem.percent
    }

def log_memory_checkpoint(label: str):
    """Log memory stats at a checkpoint."""
    stats = get_memory_stats()
    logger.info(
        f"[MEMORY] {label} | "
        f"Process: {stats['process_rss_mb']:.1f}MB | "
        f"Available: {stats['system_available_mb']:.1f}MB | "
        f"System: {stats['system_percent']}%"
    )
