from typing import Dict

from pydantic import BaseModel, RootModel


class ConsultaCodigoOutput(RootModel):
    root: dict


class BaseError(BaseModel):
    """Modelo base para representar erros."""
    error: str


class DefaultResponses:
    """Classe base para respostas HTTP padrão."""

    # Exemplo de processo para resposta
    processo_exemplo = [
        {
            "nome_particao_arquivo": "Arquivo 1",
            "anexos": [
                {
                    "nome_arquivo": "arquivo.txt",
                    "href": "arquivo1-98465.txt",
                    "base64": "MDNiODcwNjAyZGIyMGM5Y2Q1NDk0YTQzOTIzZmI1NzBiNDFkZjZkNDFhOWIxNWQxMTFiNjI1ZjNmYmU3MGM0Ni50eHQ="
                },
                {
                    "nome_arquivo": "arquivo.pdf",
                    "href": "arquivo1-98465.pdf",
                    "base64": "JVBERi0xLjcKCjQgMCBvYmoKKElkZW50aXR5KQplbmRvYmoKNSAwIG9iagooQWRvYmU"
                }
            ],
            "codigo_consultado": 98465
        },
        {
            "nome_particao_arquivo": "Arquivo 2",
            "anexos": [
                {
                    "nome_arquivo": "arquivo2.txt",
                    "href": "arquivo2-98465.txt",
                    "base64": "ZjQxNTczNDFiNzAzZGIwYTc3YzIyYjFjOGVjODcxOWM4ZDg5M2YwODlkMWEwODljYzEwMGZlMzljNDJhYTA5NC50eHQ="
                },
                {
                    "nome_arquivo": "arquivo2.pdf",
                    "href": "arquivo2-98465.pdf",
                    "base64": "JVBERi0xLjcKCjQgMCBvYmoKKElkZW50aXR5KQ"
                }
            ],
            "codigo_consultado": 98465
        }

    ]

    @classmethod
    def _status_200(cls):
        """Resposta para o código de status 200 (OK) para a consulta de status de solicitação."""
        return {
            200: {
                "model": ConsultaCodigoOutput,
                "description": "Código capturado.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example2": {
                                "summary": "Dados capturados",
                                "value": cls.processo_exemplo
                            }
                        }
                    }
                }
            }
        }

    @classmethod
    def _status_404(cls):
        """Resposta para o código de status 404 (Not Found) para a consulta de status de solicitação."""
        return {
            404: {
                "model": BaseError,
                "description": "Código não encontrado",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Código não encontrado"
                        }
                    }
                },
            }
        }

    @classmethod
    def responses(cls):
        """Método que agrega todas as respostas padrão."""
        return {k: v for method in dir(cls) if method.startswith("_status") for k, v in getattr(cls, method)().items()}
