"""
main.py - Orquestador principal de fireview_console
Coordina todo desde el punto de entrada.
"""

import asyncio
import logging
import sys
import os
import webbrowser
import aiohttp
from aiohttp import web
from typing import List, Dict, Any
from fireview_console import FireviewConsole
from config import API_URL, MAX_ROUTES, REFRESH_INTERVAL, TIMEOUT, MAX_DEPTH, ENABLE_BROWSER
from config import FIREFOX_PATH
from pathlib import Path
# Importar configuraciones desde config.py
try:    from config import API_URL, MAX_ROUTES, REFRESH_INTERVAL, TIMEOUT, MAX_DEPTH, ENABLE_BROWSER
except ImportError:    # Valores predeterminados si config.py no está presente
    API_URL = "http://localhost:8000"
    MAX_ROUTES = 5
    REFRESH_INTERVAL = 5.0
    TIMEOUT = 5.0
    MAX_DEPTH = 5
    ENABLE_BROWSER = True

async def main():
    """Función principal que inicia la aplicación."""
    console = FireviewConsole()
    await console.start()

if __name__ == "__main__":    asyncio.run(main())

