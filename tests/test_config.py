"""
test_config.py - Pruebas unitarias para el módulo de configuración
"""

import pytest
import sys
from pathlib import Path
from src.config import Config


class TestConfig:
    """Suite de pruebas para la clase Config."""
    
    def test_config_api_url_default(self):
        """Verifica que API_URL tenga un valor por defecto."""
        assert Config.API_URL is not None
        assert isinstance(Config.API_URL, str)
    
    def test_config_max_routes_is_integer(self):
        """Verifica que MAX_ROUTES sea un entero."""
        assert isinstance(Config.MAX_ROUTES, int)
        assert Config.MAX_ROUTES > 0
    
    def test_config_refresh_interval_is_float(self):
        """Verifica que REFRESH_INTERVAL sea un float."""
        assert isinstance(Config.REFRESH_INTERVAL, float)
        assert Config.REFRESH_INTERVAL > 0
    
    def test_config_enable_browser_is_boolean(self):
        """Verifica que ENABLE_BROWSER sea un booleano."""
        assert isinstance(Config.ENABLE_BROWSER, bool)
    
    def test_config_server_port_is_integer(self):
        """Verifica que SERVER_PORT sea un entero válido."""
        assert isinstance(Config.SERVER_PORT, int)
        assert 0 < Config.SERVER_PORT < 65536
    
    def test_firefox_path_exists_or_default(self):
        """Verifica que FIREFOX_PATH sea válido o tenga un valor por defecto."""
        assert isinstance(Config.FIREFOX_PATH, str)
        assert len(Config.FIREFOX_PATH) > 0
    
    def test_config_to_dict(self):
        """Verifica que to_dict() retorne un diccionario válido."""
        config_dict = Config.to_dict()
        assert isinstance(config_dict, dict)
        assert "API_URL" in config_dict
        assert "MAX_ROUTES" in config_dict
        assert "SERVER_PORT" in config_dict
