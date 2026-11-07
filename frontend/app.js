const form = document.getElementById("form");
const campoUrl = document.getElementById("url");
const campoRede = document.getElementById("rede");
const botao = document.getElementById("botao");

const formEmail = document.getElementById("form-email");
const campoArquivo = document.getElementById("arquivo");
const campoRedeEmail = document.getElementById("rede-email");
const botaoEmail = document.getElementById("botao-email");

const abaUrl = document.getElementById("aba-url");
const abaEmail = document.getElementById("aba-email");
const abas = document.querySelectorAll("[data-aba]");

const mensagem = document.getElementById("mensagem");
const resultado = document.getElementById("resultado");
const anel = document.getElementById("anel");
const nivel = document.getElementById("nivel");
const pontuacao = document.getElementById("pontuacao");
const urlAnalisada = document.getElementById("url-analisada");
const tituloSinais = document.getElementById("titulo-sinais");
const sinais = document.getElementById("sinais");
const tituloLinks = document.getElementById("titulo-links");
const links = document.getElementById("links");
const historico = document.getElementById("historico");

const CLASSE_NIVEL = { baixo: "baixo", "médio": "medio", alto: "alto" };
const LIMITE_EML = 2 * 1024 * 1024;

function criar(tag, texto, classe) {
  const elemento = document.createElement(tag);
  elemento.textContent = texto;
  if (classe) elemento.className = classe;
  return elemento;
}

// Mostra o link "desarmado" (hxxp, [.]) para ninguém clicar sem querer.
function neutralizar(url) {
  return url.replace(/^http/i, "hxxp").replace(/\./g, "[.]");
}

async function mensagemDeErro(resposta, padrao) {
  const erro = await resposta.json().catch(() => ({}));
  return typeof erro.detail === "string" ? erro.detail : padrao;
}

async function analisar(url, consultarRede) {
  const resposta = await fetch("/analisar/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, consultar_rede: consultarRede }),
  });

  if (!resposta.ok) {
    throw new Error(
      await mensagemDeErro(resposta, "Não foi possível analisar essa URL.")
    );
  }
  return resposta.json();
}

async function analisarEmail(arquivo, consultarRede) {
  const dados = new FormData();
  dados.append("arquivo", arquivo);
  dados.append("consultar_rede", consultarRede ? "true" : "false");

  // Sem Content-Type: o navegador monta o formato multipart sozinho.
  const resposta = await fetch("/analisar/email", {
    method: "POST",
    body: dados,
  });

  if (!resposta.ok) {
    throw new Error(
      await mensagemDeErro(resposta, "Não foi possível analisar esse e-mail.")
    );
  }
  return resposta.json();
}

function preencherTopo(nivelTexto, pontos, linha) {
  const classe = CLASSE_NIVEL[nivelTexto] || "";

  resultado.hidden = false;
  nivel.textContent = nivelTexto.toUpperCase();
  nivel.className = "badge " + classe;
  pontuacao.textContent = pontos;
  anel.className = "anel " + classe;
  anel.style.setProperty("--pct", pontos);
  urlAnalisada.textContent = linha;
}

function listarSinais(lista, itens, textoVazio) {
  lista.replaceChildren();
  if (itens.length === 0) {
    lista.appendChild(criar("li", textoVazio));
    return;
  }
  for (const s of itens) {
    const item = document.createElement("li");
    item.appendChild(criar("span", s.descricao));
    item.appendChild(criar("span", "+" + s.pontos, "pontos"));
    lista.appendChild(item);
  }
}

function mostrarResultado(r) {
  preencherTopo(r.nivel, r.pontuacao, r.url);
  tituloSinais.hidden = true;
  tituloLinks.hidden = true;
  links.hidden = true;
  listarSinais(sinais, r.sinais, "Nenhum sinal de risco encontrado.");
}

function mostrarResultadoEmail(r) {
  preencherTopo(r.nivel, r.pontuacao, "Assunto: " + r.assunto);
  tituloSinais.hidden = false;
  tituloLinks.hidden = false;
  links.hidden = false;
  listarSinais(sinais, r.sinais, "Nenhum sinal de risco no cabeçalho.");

  links.replaceChildren();
  if (r.links.length === 0) {
    links.appendChild(criar("li", "Nenhum link encontrado no e-mail."));
  }
  for (const l of r.links) {
    const item = document.createElement("li");
    item.appendChild(criar("span", neutralizar(l.url), "link-url"));
    item.appendChild(
      criar(
        "span",
        l.nivel + " · " + l.pontuacao,
        "badge " + (CLASSE_NIVEL[l.nivel] || "")
      )
    );
    links.appendChild(item);
  }
  if (r.links_ignorados > 0) {
    links.appendChild(
      criar("li", `+ ${r.links_ignorados} link(s) não analisado(s) (limite de 20).`)
    );
  }
}

async function carregarHistorico() {
  const resposta = await fetch("/historico?limite=10");
  if (!resposta.ok) return;
  const itens = await resposta.json();

  historico.replaceChildren();
  for (const item of itens) {
    const linha = document.createElement("tr");
    linha.appendChild(criar("td", new Date(item.criado_em + "Z").toLocaleString("pt-BR")));
    linha.appendChild(criar("td", item.url, "url"));
    linha.appendChild(criar("td", String(item.pontuacao)));

    const celulaNivel = document.createElement("td");
    celulaNivel.appendChild(
      criar("span", item.nivel, "badge " + (CLASSE_NIVEL[item.nivel] || ""))
    );
    linha.appendChild(celulaNivel);

    historico.appendChild(linha);
  }
}

function mostrarAba(nome) {
  abaUrl.hidden = nome !== "url";
  abaEmail.hidden = nome !== "email";
  for (const link of abas) {
    link.classList.toggle("ativo", link.dataset.aba === nome);
  }
  resultado.hidden = true;
  mensagem.textContent = "";
}

for (const link of abas) {
  link.addEventListener("click", (evento) => {
    evento.preventDefault();
    mostrarAba(link.dataset.aba);
  });
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mensagem.textContent = "Analisando… pode levar alguns segundos.";
  botao.disabled = true;

  try {
    const r = await analisar(campoUrl.value.trim(), campoRede.checked);
    mostrarResultado(r);
    mensagem.textContent = "";
    await carregarHistorico();
  } catch (erro) {
    resultado.hidden = true;
    mensagem.textContent = erro.message;
  } finally {
    botao.disabled = false;
  }
});

formEmail.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const arquivo = campoArquivo.files[0];
  if (!arquivo) {
    mensagem.textContent = "Escolha um arquivo .eml.";
    return;
  }
  if (!arquivo.name.toLowerCase().endsWith(".eml")) {
    mensagem.textContent = "O arquivo precisa ser um .eml.";
    return;
  }
  if (arquivo.size > LIMITE_EML) {
    mensagem.textContent = "O arquivo é maior que 2 MB.";
    return;
  }

  mensagem.textContent = "Analisando o e-mail… pode levar alguns segundos.";
  botaoEmail.disabled = true;

  try {
    const r = await analisarEmail(arquivo, campoRedeEmail.checked);
    mostrarResultadoEmail(r);
    mensagem.textContent = "";
    await carregarHistorico();
  } catch (erro) {
    resultado.hidden = true;
    mensagem.textContent = erro.message;
  } finally {
    botaoEmail.disabled = false;
  }
});

carregarHistorico();