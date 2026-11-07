const form = document.getElementById("form");
const campoUrl = document.getElementById("url");
const campoRede = document.getElementById("rede");
const botao = document.getElementById("botao");
const mensagem = document.getElementById("mensagem");
const resultado = document.getElementById("resultado");
const nivel = document.getElementById("nivel");
const pontuacao = document.getElementById("pontuacao");
const urlAnalisada = document.getElementById("url-analisada");
const sinais = document.getElementById("sinais");
const historico = document.getElementById("historico");
const anel = document.getElementById("anel");

const CLASSE_NIVEL = { baixo: "baixo", "médio": "medio", alto: "alto" };

function criar(tag, texto, classe) {
  const elemento = document.createElement(tag);
  elemento.textContent = texto;
  if (classe) elemento.className = classe;
  return elemento;
}

async function analisar(url, consultarRede) {
  const resposta = await fetch("/analisar/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, consultar_rede: consultarRede }),
  });

  if (!resposta.ok) {
    const erro = await resposta.json().catch(() => ({}));
    const texto = typeof erro.detail === "string"
      ? erro.detail
      : "Não foi possível analisar essa URL.";
    throw new Error(texto);
  }
  return resposta.json();
}

function mostrarResultado(r) {
  const classe = CLASSE_NIVEL[r.nivel] || "";

  resultado.hidden = false;
  nivel.textContent = r.nivel.toUpperCase();
  nivel.className = "badge " + classe;
  pontuacao.textContent = r.pontuacao;
  anel.className = "anel " + classe;
  anel.style.setProperty("--pct", r.pontuacao);
  urlAnalisada.textContent = r.url;

  sinais.replaceChildren();
  if (r.sinais.length === 0) {
    sinais.appendChild(criar("li", "Nenhum sinal de risco encontrado."));
    return;
  }
  for (const s of r.sinais) {
    const item = document.createElement("li");
    item.appendChild(criar("span", s.descricao));
    item.appendChild(criar("span", "+" + s.pontos, "pontos"));
    sinais.appendChild(item);
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

carregarHistorico();