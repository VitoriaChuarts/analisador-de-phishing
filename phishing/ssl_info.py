import socket
import ssl
from phishing.validar_rede import validar_url


from phishing.validar_rede import validar_url


def verificar_certificado(host: str, porta: int = 443, timeout: float = 5) -> str:
    try:
        validar_url(host)
    except ValueError:
        return "indisponivel"

    contexto = ssl.create_default_context()
    
def seguir_redirecionamentos(url: str, timeout: float = 5) -> list:
    caminho = [url]
    atual = url

    for _ in range(MAX_SALTOS):
        try:
            validar_url(atual)
        except ValueError:
            break

        try:
            resposta = requests.get(
                atual, allow_redirects=False, timeout=timeout, stream=True
            )
        except requests.RequestException:
            break

       
    contexto = ssl.create_default_context()
    try:
        with socket.create_connection((host, porta), timeout=timeout) as conexao:
            with contexto.wrap_socket(conexao, server_hostname=host):
                return "valido"
    except ssl.SSLCertVerificationError:
        return "invalido"
    except (OSError, ssl.SSLError):
        return "indisponivel"


def sinal_certificado(status: str):
    if status == "invalido":
        return ("Certificado SSL inválido (vencido, autoassinado ou de outro site)", 25)
    return None