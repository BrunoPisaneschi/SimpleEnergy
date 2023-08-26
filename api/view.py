from logging import basicConfig, getLogger, INFO

from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

from api.schemas.input import ConsultaCodigoInput
from api.schemas.output import ConsultaCodigoOutput, DefaultResponses
from crawler.capturar_dados import CapturarDados
from exemplo import execucao_modelo

# Configuração de log
basicConfig(filename='log.txt',
            level=INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)

api_router = APIRouter(
    tags=['codigo']
)


@api_router.get("/", include_in_schema=False)
def read_root():
    """
    Redireciona a raiz para a página de documentação.
    """
    return RedirectResponse(url="/docs")


@api_router.post("/consultar-codigo", response_model=ConsultaCodigoOutput, responses=DefaultResponses.responses())
async def consulta_codigo(payload: ConsultaCodigoInput):
    """
    Recebe um código para ser buscado no site teste.
    Caso não encontre, retorna status 404.
    :param payload: Código para ser buscado
    :return:
    """
    capturar_dados = CapturarDados()

    response = capturar_dados.capturar_dados_existentes(payload.codigo)

    if not response:
        return JSONResponse(status_code=404, content={"error": "Código não encontrado"})

    return JSONResponse(
        content=ConsultaCodigoOutput.model_validate({payload.codigo: response}).model_dump(),
        status_code=200
    )


@api_router.get("/executar-modelo",
                response_model=ConsultaCodigoOutput,
                responses=DefaultResponses.responses())
async def executar_modelo():
    response = execucao_modelo()

    return JSONResponse(
        content=ConsultaCodigoOutput.model_validate(response).model_dump(exclude_none=True),
        status_code=200
    )
