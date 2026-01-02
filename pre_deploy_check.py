import os
import sys
import py_compile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PreDeployCheck")

def check_syntax():
    """Check syntax of all python files."""
    try:
        files = [f for f in os.listdir('.') if f.endswith('.py')]
        for f in files:
            logger.info(f"Checking syntax: {f}")
            py_compile.compile(f, doraise=True)
        return True
    except Exception as e:
        logger.error(f"Syntax error found: {e}")
        return False

def check_env_vars():
    """Check if critical environment variables are defined."""
    critical_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY']
    missing = [v for v in critical_vars if not os.getenv(v)]
    
    if missing:
        logger.warning(f"Missing environment variables: {', '.join(missing)}")
        # We don't necessarily exit 1 here in case they are set in Render dashboard but not build env
        # However, for a strict check, we could.
    return True

def main():
    logger.info("Starting pre-deployment checks...")
    
    if not check_syntax():
        logger.error("Pre-deployment check FAILED: Syntax errors detected.")
        sys.exit(1)
        
    check_env_vars()
    
    logger.info("Pre-deployment checks PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
