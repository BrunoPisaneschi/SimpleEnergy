*** Settings ***
Library     Collections
Library     RequestsLibrary

*** Variables ***
${BASE_URL}             http://localhost:8000
${CODIGO}               98465

*** Keywords ***
Consultar Processo
    [Arguments]    ${codigo}
    ${payload}=    Create Dictionary    codigo=${codigo}
    Create Session    minha_sessao    ${BASE_URL}
    ${response}=    POST On Session    minha_sessao    /consultar-codigo    json=${payload}
    ${json_response}=    Set Variable    ${response.json()}
    ${status_code}=    Set Variable    ${response.status_code}
    Set Suite Variable    ${json_response}
    Set Suite Variable    ${status_code}

*** Test Cases ***
Teste Consulta Código Existente
    Consultar Processo    ${CODIGO}
    Dictionary Should Contain Key    ${json_response}    ${CODIGO}
    ${data}=    Get From Dictionary    ${json_response}    ${CODIGO}
    Should Be Equal As Strings    ${status_code}    200
    Should Be True    ${data} != None

