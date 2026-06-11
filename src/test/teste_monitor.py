from src.ingeston.monitor import MRVMonitor
import pytest
import os
CATEGORIAS = [
    "central_de_resultados_release",
    "central_de_resultados_previa",
    "central_de_resultados_itr",
    "central_de_resultados_planilha_interativa",
    "central_de_resultados_transcricao"
]
CATEGORIAS_invalidas= [
    "central_de_resultados_release1",
    "central_de_resultados_previa2",
    "central_de_resultados_itr3",
    "central_de_resultados_planilha_interativa4",
    "central_de_resultados_transcricao5"
]
# Verificando se todos os payloads esta me retornando algo valido , por caterogia, messagem esperada um 200
def test_my_payload1():
    for cat in CATEGORIAS:
        monitor = MRVMonitor(
            ano=2026,
            categoria=cat
        )

        assert monitor.payload["year"] == 2026
        assert monitor.payload["categories"] == [cat]
# Verificando se todos os payloads esta me retornando algo invalido , por caterogia, messagem esperada um Raise ERROR
def test_my_payload2():
    for cat in CATEGORIAS_invalidas:
       with pytest.raises(ValueError): MRVMonitor(
        ano=2026,
        categoria= cat
        )

# Verificando se passar uma data valida
def test_my_payload_year1():
    for ano in range(2019 , 2026):
        monitor= MRVMonitor(
            ano=ano,
            categoria="central_de_resultados_previa"
        )
        assert monitor.ano == ano

# Verificando se passar uma data invalida
def test_my_payload_year2():
     for ano in range(1 , 100):
        with pytest.raises(ValueError):  monitor= MRVMonitor(
            ano=ano,
            categoria="central_de_resultados_previa"
        )

# Verificando se o hash gerado é igual ao SHA-256 esperado
def test_gerar_hash():

    monitor = MRVMonitor()

    hash = monitor.gerar_hash(b"Bom dia tudo bem")

    assert hash is not None
def test_salvar_pdf():

    monitor = MRVMonitor()

    doc = {
        "file_year": 2026,
        "file_quarter": 1
    }

    conteudo = b"pdf fake"

    hash_doc = monitor.gerar_hash(
        conteudo
    )

    caminho = monitor.salvar_pdf(
        doc,
        conteudo,
        hash_doc
    )

    assert os.path.exists(caminho)


# Verificando se o conteúdo retornado pelo download corresponde ao esperado
def test_baixar_documento():

    monitor = MRVMonitor()

    documentos = monitor.buscar_documentos()

    doc = documentos[0]

    conteudo = monitor.baixar_documento(doc)

    assert conteudo is not None
    assert len(conteudo) > 0


# Verificando se o payload é criado corretamente
def test_payload():

    monitor = MRVMonitor(
        ano=2026,
        categoria="central_de_resultados_previa"
    )

    assert monitor.payload["year"] == 2026

    assert monitor.payload["categories"] == [
        "central_de_resultados_previa"
    ]

    assert monitor.payload["language"] == "pt_BR"

    assert monitor.payload["published"] is True


# Verificando se o monitor busca documentos na API
def test_buscar_documentos():

    monitor = MRVMonitor()

    documentos = monitor.buscar_documentos()

    assert isinstance(
        documentos,
        list
    )

    assert len(documentos) > 0


# Verificando se o arquivo de hashes é carregado corretamente
def test_carregar_hashes():

    monitor = MRVMonitor()

    hashes = monitor.carregar_hashes()

    assert isinstance(
        hashes,
        set
    )


# Verificando se o arquivo de hashes é salvo corretamente
def test_salvar_hashes():

    monitor = MRVMonitor()

    hashes = {
        "abc",
        "def"
    }

    monitor.salvar_hashes(
        hashes
    )

    hashes_lidos = (
        monitor.carregar_hashes()
    )

    assert hashes == hashes_lidos


# Verificando se o nome do PDF é gerado corretamente
def test_nome_arquivo_pdf():

    monitor = MRVMonitor()

    doc = {
        "file_year": 2026,
        "file_quarter": 2
    }

    hash_doc = "123456789abcdef"

    caminho = monitor.salvar_pdf(
        doc,
        b"teste",
        hash_doc
    )

    assert (
        "2026_T2_12345678.pdf"
        in caminho
    )


# Verificando se o hash muda quando o conteúdo do PDF muda
def test_hash_diferente_para_conteudo_diferente():

    monitor = MRVMonitor()

    hash1 = monitor.gerar_hash(
        b"arquivo 1"
    )

    hash2 = monitor.gerar_hash(
        b"arquivo 2"
    )

    assert hash1 != hash2


# Verificando se o monitor executa o fluxo completo de processamento
def test_executar():

    monitor = MRVMonitor()

    monitor.executar()

    assert True