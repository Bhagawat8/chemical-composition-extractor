"""
GPU availability checker for DeepSeek-OCR compatibility
"""
import logging

logger = logging.getLogger(__name__)

def check_gpu_available() -> bool:
    """
    Check if CUDA-compatible GPU is available
    
    Returns:
        True if GPU with CUDA is available, False otherwise
    """
    try:
        import torch
        available = torch.cuda.is_available()
        
        if available:
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
            logger.info(f"GPU detected: {gpu_name} with {gpu_memory:.2f} GB memory")
            
            if gpu_memory < 8:
                logger.warning(f"GPU memory ({gpu_memory:.2f} GB) is below recommended 12 GB for DeepSeek-OCR")
                return False
            
            return True
        else:
            logger.info("No CUDA-compatible GPU detected. Using CPU mode.")
            return False
            
    except ImportError:
        logger.warning("PyTorch not installed. GPU check skipped. Using CPU mode.")
        return False
    except Exception as e:
        logger.error(f"Error checking GPU availability: {e}")
        return False

def get_gpu_info() -> dict:
    """
    Get detailed GPU information
    
    Returns:
        Dictionary with GPU details or empty dict if not available
    """
    try:
        import torch
        if not torch.cuda.is_available():
            return {}
        
        return {
            'name': torch.cuda.get_device_name(0),
            'memory_total_gb': torch.cuda.get_device_properties(0).total_memory / (1024**3),
            'memory_allocated_gb': torch.cuda.memory_allocated(0) / (1024**3),
            'cuda_version': torch.version.cuda,
            'device_count': torch.cuda.device_count()
        }
    except:
        return {}
