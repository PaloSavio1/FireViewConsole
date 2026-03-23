"""
fireview_console.py - Modulo de visualizacion de API
Permite visualizar datos de APIs locales en consola y navegador.
"""
import asyncio
from aiohttp import web
import aiohttp
import webbrowser
import json
import logging
from typing import List, Dict, Any

# Importar configuraciones desde config.py
try:
    from config import API_URL, MAX_ROUTES, REFRESH_INTERVAL, TIMEOUT, MAX_DEPTH, ENABLE_BROWSER
except ImportError:
    # Valores predeterminados si config.py no está presente
    API_URL = "http://localhost:8000"
    MAX_ROUTES = 5
    REFRESH_INTERVAL = 5.0
    TIMEOUT = 5.0
    MAX_DEPTH = 5
    ENABLE_BROWSER = True

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FireViewConsole")

# Configuración de Firefox
FIREFOX_PATH = "/usr/bin/firefox"  # Cambia esto según tu sistema operativo

# Clase principal de visualización de API
class FireviewConsole:
    """
    Clase principal que gestiona la visualizacion de API.
    """
    def __init__(self, api_url: str = "http://localhost:8000", max_routes: int = 5,refresh_interval: float = 5.0,timeout: float = 5.0,max_depth: int = 5,enable_browser: bool = True):
        """Inicializa la clase con configuraciones predeterminadas."""
        self.api_url = api_url
        self.max_routes = max_routes
        self.refresh_interval = refresh_interval
        self.timeout = timeout
        self.max_depth = max_depth
        self.enable_browser = enable_browser
        self.routes_data: List[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.handle_root)])
        self.runner = web.AppRunner(self.app)
        self.site = None
        self.logger = logging.getLogger("FireViewConsole")
        logging.basicConfig(level=logging.INFO)
        
    async def fetch_routes(self) -> List[Dict[str, Any]]:
        """Obtiene las rutas de la API desde el endpoint /routes."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(f"{self.api_url}/routes") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.logger.info(f"Rutas obtenidas: {len(data)}")
                        return data[:self.max_routes]
                    else:
                        self.logger.error(f"Error al obtener rutas: {response.status}")
                        return []
        except Exception as e:
            self.logger.error(f"Excepción al obtener rutas: {e}")
            return []
        
    async def handle_root(self, request: web.Request) -> web.Response:
        """Maneja la ruta raíz y muestra las rutas obtenidas."""
        self.routes_data = await self.fetch_routes()
        html_content = self.generate_html(self.routes_data)
        return web.Response(text=html_content, content_type='text/html')
    
    def generate_html(self, routes: List[Dict[str, Any]]) -> str:
        """Genera el contenido HTML para mostrar las rutas."""
        html = "<html><head><title>FireView Console</title></head><body>"
        html += "<h1>Rutas de la API</h1><ul>"
        for route in routes:
            html += f"<li>{route.get('method', 'N/A')} {route.get('path', 'N/A')}</li>"
        html += "</ul></body></html>"
        return html
    
    async def start_server(self):
        """Inicia el servidor web para mostrar las rutas."""
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, 'localhost', 8080)
        await self.site.start()
        self.logger.info("Servidor iniciado en http://localhost:8080")
        if self.enable_browser:
            webbrowser.open("http://localhost:8080")

    async def refresh_routes(self):
        """Refresca las rutas periódicamente."""
        while True:
            self.routes_data = await self.fetch_routes()
            await asyncio.sleep(self.refresh_interval)

    async def run(self):
        """Ejecuta el servidor y el refresco de rutas."""
        await self.start_server()
        await self.refresh_routes()

    async def start(self):
        """Inicia la aplicación."""
        await self.run()