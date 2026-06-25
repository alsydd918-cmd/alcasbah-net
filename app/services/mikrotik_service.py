import subprocess
import platform
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MikroTikService:
    """Service for MikroTik monitoring"""
    
    def __init__(self, device):
        self.device = device
    
    def test_connection(self):
        """Test connection to device"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            result = subprocess.run(
                ['ping', param, '1', self.device.ip_address],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.decode()
                if 'time=' in output:
                    ping_str = output.split('time=')[1].split()[0]
                    ping_time = float(ping_str.replace('ms', ''))
                else:
                    ping_time = 0
                
                return {
                    'success': True,
                    'status': 'online',
                    'ping_time': ping_time
                }
            else:
                return {
                    'success': False,
                    'status': 'offline'
                }
        except Exception as e:
            logger.error(f'Ping error: {e}')
            return {
                'success': False,
                'error': str(e)
            }
