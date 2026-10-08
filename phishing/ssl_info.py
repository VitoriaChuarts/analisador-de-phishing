import socket
import ssl


def verificar_certificado(host: str, porta: int = 443, timeout: float = 5) -> str:
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