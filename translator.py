import requests
import json
from typing import Optional

class Translator:
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text: str, target_lang: str = 'pt') -> Optional[str]:
        """
        Traduz texto usando a API do Google Translate
        """
        try:
            params = {
                'client': 'gtx',
                'sl': 'auto',
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # A resposta é uma estrutura JSON complexa
            data = response.json()
            
            # Extrair o texto traduzido
            if data and len(data) > 0:
                translated_parts = []
                for item in data[0]:
                    if item[0]:
                        translated_parts.append(item[0])
                return ''.join(translated_parts)
            
            return text
            
        except Exception as e:
            print(f"Erro na tradução: {e}")
            return text
