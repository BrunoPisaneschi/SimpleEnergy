from pydantic import BaseModel


class ConsultaCodigoInput(BaseModel):
    """Modelo de entrada para consulta de um processo."""

    codigo: int
