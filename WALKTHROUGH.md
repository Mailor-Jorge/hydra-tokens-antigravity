# 🐍 HYDRA TOKENS ANTIGRAVITY — Walkthrough Completo

> Guia passo a passo: da primeira instalação até o uso avançado de todos os 9 heads.

---

## Índice

1. [O que é o HYDRA?](#1-o-que-é-o-hydra)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Instalação](#3-instalação)
4. [Verificação pós-instalação](#4-verificação-pós-instalação)
5. [Primeiro uso: Comandos básicos](#5-primeiro-uso-comandos-básicos)
6. [Heads detalhados: Como cada um funciona](#6-heads-detalhados)
7. [Ciclos automáticos](#7-ciclos-automáticos)
8. [Comandos rápidos (Quick Reference)](#8-comandos-rápidos)
9. [Cenários práticos](#9-cenários-práticos)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. O que é o HYDRA?

HYDRA TOKENS ANTIGRAVITY é um framework modular que **reduz o consumo de tokens** ao usar agentes de IA no Google Antigravity IDE. Funciona como uma hidra de 9 cabeças — cada "head" ataca um tipo diferente de desperdício de tokens:

```
╔═══════════════════════════════════════════════════════════════╗
║                    HYDRA — 9 HEADS                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🧠 Skills (on-demand, ativados por trigger)                  ║
║  ├── HEAD-1: hydra           → Orquestrador principal         ║
║  ├── HEAD-2: hydra_mcp       → Seletor inteligente de MCP     ║
║  ├── HEAD-3: hydra_compress  → Compressor de contexto         ║
║  └── HEAD-4: hydra_audit     → Auditor de custo de tokens     ║
║                                                               ║
║  📜 Rules (sempre ativas, 0 ação necessária)                  ║
║  ├── HEAD-5: OUTPUT_FORMAT   → Formato compacto de saída      ║
║  ├── HEAD-6: CONTEXT_GUARD   → Proteção contra bloat          ║
║  └── HEAD-7: NO_REPEAT       → Anti-repetição                 ║
║                                                               ║
║  🔧 MCP Server (6 ferramentas locais)                         ║
║  └── HEAD-8: hydra-tools-mcp → filter, estimate, snippet...   ║
║                                                               ║
║  🤖 Agent Template (opcional)                                 ║
║  └── HEAD-9: hydra_agent     → System prompt minimalista      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Impacto total:** Redução de 40% a 90% no consumo de tokens, dependendo do tipo de tarefa.

---

## 2. Pré-requisitos

| Requisito | Verificação |
|-----------|-------------|
| Google Antigravity IDE | Instalado e funcionando |
| Git | `git --version` retorna versão |
| Node.js (para MCP) | `node --version` retorna ≥ 18.x |
| npm (para MCP) | `npm --version` retorna ≥ 9.x |
| PowerShell | Terminal padrão do Windows |

---

## 3. Instalação

### Passo 1 — Clonar o repositório

```powershell
git clone https://github.com/Mailor-Jorge/hydra-tokens-antigravity.git
cd hydra-tokens-antigravity
```

### Passo 2 — Instalar automaticamente

```powershell
.\install.ps1
```

O script faz tudo:
- ✅ Copia as 4 skills para `~\.gemini\config\skills\`
- ✅ Adiciona as regras HEAD-5,6,7 ao `AGENTS.md`
- ✅ Configura o MCP server

### Passo 3 — Instalar o MCP Server (opcional mas recomendado)

O MCP Server roda **localmente na sua máquina** e processa dados antes de enviar ao modelo. Configuração no arquivo `settings.json` do Antigravity:

```json
{
  "mcpServers": {
    "hydra-tools-mcp": {
      "command": "npx",
      "args": ["-y", "@mailoko/hydra-tools-mcp@latest"]
    }
  }
}
```

> **Alternativa local (sem npm):** Se preferir rodar diretamente o Python:
> ```json
> {
>   "mcpServers": {
>     "hydra-tools-mcp": {
>       "command": "python",
>       "args": ["C:\\Users\\SeuUsuario\\.gemini\\config\\hydra_mcp_server.py"]
>     }
>   }
> }
> ```

### Passo 4 — Reiniciar o Antigravity IDE

Feche e reabra o IDE. **Isso é obrigatório** para que as skills sejam detectadas.

---

## 4. Verificação pós-instalação

Após reiniciar, vá em **Settings → Customizations**. Você deve ver:

```
Skills (4):
  ✅ hydra
  ✅ hydra_mcp
  ✅ hydra_compress
  ✅ hydra_audit

Rules (1 arquivo, 3 heads):
  ✅ AGENTS.md → HEAD-5, HEAD-6, HEAD-7

Budget estimado: ~4-6% do total
```

**Teste rápido:** No chat, digite:

```
hydra audit
```

Se aparecer um relatório com tabela de custos → **instalação concluída com sucesso!** ✅

---

## 5. Primeiro uso: Comandos básicos

### 5.1 — `hydra audit` (verificar saúde do sistema)

```
Você digita: hydra audit

HYDRA retorna:
╔══════════════════════════════════════════════════╗
║         HYDRA TOKEN AUDIT REPORT                 ║
╠══════════════════════════════════════════════════╣
║ RULES LOADED (always-on)                         ║
║   AGENTS.md (HEAD-5,6,7)          ~380 tokens    ║
║ SKILLS ACTIVE (on-demand)                        ║
║   hydra_audit (this session)      ~350 tokens    ║
║ MCP SERVERS                                      ║
║   hydra-tools-mcp (6 tools)      ~200 tokens     ║
║ EFFICIENCY SCORE: 85/100                         ║
╚══════════════════════════════════════════════════╝
```

### 5.2 — `hydra compress` (limpar histórico longo)

Após muitas interações, o contexto da conversa fica grande. O compress cria um **digest semântico** que resume tudo em ~1.5k tokens:

```
Você digita: hydra compress

HYDRA retorna:
[HYDRA HEAD-3] Compression complete.
  Before : ~8,200 tokens
  After  : ~1,400 tokens
  Saved  : ~6,800 tokens (83%)
```

### 5.3 — `hydra limit 200` (controlar tamanho da resposta)

```
Você digita: hydra limit 200

A próxima resposta terá no máximo ~200 tokens.
Para desativar: hydra limit off
```

### 5.4 — `hydra snapshot` (ver arquivos pesados)

```
Você digita: hydra snapshot C:\MeuProjeto

HYDRA retorna:
[HYDRA CONTEXT SNAPSHOT] C:\MeuProjeto
  Total files: 45 | Total est. tokens: ~12,340
  ────────────────────────────────────────
  [HEAVY] main.py                    8.2 KB  ~2,050 tok
  [HEAVY] database.py               6.1 KB  ~1,525 tok
  [OK   ] config.json               1.2 KB  ~300 tok
  [OK   ] utils.py                  0.8 KB  ~200 tok
```

---

## 6. Heads detalhados

### HEAD-1: `hydra` (Orquestrador)

**Tipo:** Skill (trigger manual)
**Triggers:** `hydra`, `/hydra`, `modo hydra`

Faz um scan completo do sistema e recomenda quais heads ativar para a sessão atual. É o ponto de entrada principal.

---

### HEAD-2: `hydra_mcp` (Seletor Inteligente de MCP)

**Tipo:** Skill (trigger manual)
**Triggers:** `hydra mcp`, `qual mcp usar`, `selecionar mcp`

Analisa a tarefa atual e recomenda **quais MCP servers carregar** — porque cada MCP server carregado consome tokens de input com suas definições de ferramentas.

**Exemplo prático:**
```
Você: hydra mcp Vou editar arquivos Papyrus do Skyrim

HYDRA: Para esta tarefa, recomendo carregar apenas:
  ✅ hydra-tools-mcp (snippet + filter_log)
  ❌ Não precisa de: browser, database, search
  Economia: ~2,400 tokens de input
```

---

### HEAD-3: `hydra_compress` (Compressor de Contexto)

**Tipo:** Skill (trigger manual + automático a cada 10 turns)
**Triggers:** `hydra compress`, `compactar contexto`

Cria um **checkpoint semântico** que substitui o histórico bruto da conversa por um resumo estruturado. Informações preservadas:
- Decisões tomadas
- Caminhos de arquivo importantes
- Estado atual do projeto
- Próximos passos pendentes

---

### HEAD-4: `hydra_audit` (Auditor de Tokens)

**Tipo:** Skill (trigger manual)
**Triggers:** `hydra audit`, `quanto custa`, `token report`

Gera um relatório detalhado de **tudo que está consumindo tokens** na sessão atual: rules, skills, MCPs, histórico, arquivos carregados.

---

### HEAD-5: `HYDRA_OUTPUT_FORMAT` (Formato de Saída)

**Tipo:** Rule (sempre ativa)
**Arquivo:** `AGENTS.md`

Força a IA a seguir estas regras de output:
- ❌ Sem saudações ou despedidas
- ❌ Sem recapitulações no final
- ✅ Usar bullet points, tabelas, code blocks
- ✅ Diff-only mode: nunca re-exibir arquivo inteiro ao editar
- ✅ Calibrar tamanho: resposta simples = curta, complexa = lista

---

### HEAD-6: `HYDRA_CONTEXT_GUARD` (Guarda de Contexto)

**Tipo:** Rule (sempre ativa)
**Arquivo:** `AGENTS.md`

Protege contra acúmulo de contexto com ciclos automáticos:

| Ciclo | Evento |
|-------|--------|
| A cada 10 turns | Auto-compress do histórico |
| A cada 15 turns | Context snapshot (scan de arquivos) |
| A cada 20 turns | Pergunta sobre `hydra_clean_scratch` |
| Ao ler arquivo | Sugere `hydra_snippet` antes |
| Ao repetir tópico | Checa `hydra_cache` primeiro |

---

### HEAD-7: `HYDRA_NO_REPEAT` (Anti-Repetição)

**Tipo:** Rule (sempre ativa)
**Arquivo:** `AGENTS.md`

Impede que a IA desperdice tokens com:
- ❌ "Você me pediu para..." (restating)
- ❌ Re-explicar passos já concluídos
- ❌ Confirmações repetidas
- ❌ Tool calls duplicados

---

### HEAD-8: `hydra-tools-mcp` (6 Ferramentas Locais)

**Tipo:** MCP Server (Python, roda localmente)
**NPM:** `@mailoko/hydra-tools-mcp@1.1.0`

| Ferramenta | Economia | Modo |
|------------|----------|------|
| `hydra_filter_log` | -99.8% em logs | Perguntar ao usuário |
| `hydra_token_estimate` | Previne bloat | Perguntar ao usuário |
| `hydra_clean_scratch` | Limpa workspace | Automático a cada 20 turns |
| `hydra_snippet` | -90% em leitura de arquivo | Automático (snippet-first) |
| `hydra_cache` | -100% em repetições | Automático (checa antes de gerar) |
| `hydra_context_snapshot` | Identifica arquivos pesados | Automático a cada 15 turns |

---

### HEAD-9: `hydra_agent` (Template de Agente)

**Tipo:** Template (opcional)
**Uso:** Para criar subagentes com system prompt minimalista, otimizado para baixo consumo de tokens.

---

## 7. Ciclos automáticos

O HYDRA roda ações automaticamente conforme a conversa progride:

```
Turn 1-9:    Nenhuma ação automática (conversa curta)
Turn 10:     [AUTO] hydra_compress → resume o histórico
Turn 15:     [AUTO] hydra_context_snapshot → identifica arquivos pesados
Turn 20:     [AUTO] Pergunta: "Deseja executar hydra_clean_scratch?"
             [AUTO] hydra_compress (2ª compressão)
Turn 30:     [AUTO] hydra_compress (3ª) + context_snapshot (2ª)
Turn 40:     [AUTO] hydra_compress (4ª) + pergunta clean_scratch (2ª)
```

**Em qualquer momento:**
- Ao abrir arquivo grande → Pergunta: "Usar `hydra_snippet`?"
- Ao detectar tópico repetido → Checa `hydra_cache` silenciosamente
- Ao editar arquivo → Mostra apenas o diff (nunca re-exibe o arquivo inteiro)

---

## 8. Comandos rápidos

### Skills (digitar no chat)

| Comando | O que faz |
|---------|-----------|
| `hydra` | Ativa o orquestrador, scan completo |
| `hydra audit` | Relatório de custo de tokens |
| `hydra compress` | Comprime o contexto da conversa |
| `hydra mcp [tarefa]` | Recomenda MCPs para a tarefa |
| `hydra limit N` | Limita output a ~N tokens |
| `hydra limit off` | Remove limite de output |
| `hydra diff on/off` | Liga/desliga modo diff-only |

### Ferramentas MCP (linguagem natural ou tool call)

| Comando | O que faz |
|---------|-----------|
| `hydra snippet [arquivo] [função]` | Extrai só uma função do arquivo |
| `hydra cache list` | Lista respostas cacheadas |
| `hydra cache save [chave]` | Salva resposta no cache |
| `hydra cache get [chave]` | Recupera resposta do cache |
| `hydra snapshot [diretório]` | Escaneia diretório por token cost |

---

## 9. Cenários práticos

### Cenário 1: Desenvolvendo um mod para Skyrim

```
Você: "Preciso editar a função OnPageReset no arquivo MyMod.psc"

HYDRA (automático): "Deseja que eu extraia apenas a função OnPageReset
  via hydra_snippet em vez de carregar o arquivo inteiro (~2.000 tokens)?"

Você: "Sim"

HYDRA executa: hydra_snippet("MyMod.psc", "OnPageReset")
→ Retorna apenas 30 linhas (~120 tokens) em vez de 500 linhas (~2.000 tokens)
→ Economia: 1.880 tokens (94%)
```

### Cenário 2: Analisando um log de erro grande

```
Você: "Analise o arquivo PapyrusCompiler.log para erros"

HYDRA (automático): "Detectei o arquivo PapyrusCompiler.log.
  Deseja usar hydra_filter_log para extrair apenas as linhas de erro
  (economizando ~99% de tokens)?"

Você: "Sim"

HYDRA executa: hydra_filter_log("PapyrusCompiler.log")
→ Log original: 50.000 linhas (~200.000 tokens)
→ Retornado: 12 linhas de erro (~48 tokens)
→ Economia: 199.952 tokens (99.97%)
```

### Cenário 3: Pergunta repetida sobre compilação

```
[Sessão 1]
Você: "Como compilar scripts Papyrus?"
HYDRA: [gera resposta de 500 tokens]
HYDRA: "Deseja salvar esta resposta no cache para reutilização futura?"
Você: "Sim"
→ hydra_cache(save, "compilar papyrus", resposta)

[Sessão 2]
Você: "Como compilo Papyrus mesmo?"
HYDRA: [checa cache silenciosamente]
HYDRA: "Encontrei uma resposta cacheada para este tópico (salva em 21/07).
  Deseja usar o cache (0 tokens de geração) ou uma resposta nova?"
Você: "Use o cache"
→ Economia: 500 tokens de geração (100%)
```

### Cenário 4: Conversa ficando longa (turn 10)

```
[Turn 10 — automático]
HYDRA: [HYDRA] Auto-compress T10
  Before: ~8,200 tokens
  After:  ~1,400 tokens
  Saved:  6,800 tokens (83%)

  Checkpoint salvo. Decisões anteriores preservadas.
  Continuando com contexto limpo.
```

---

## 10. Troubleshooting

| Problema | Solução |
|----------|---------|
| Skills não aparecem após instalar | Reinicie o Antigravity IDE |
| `hydra audit` não funciona | Verifique se a skill `hydra_audit` aparece em Customizations |
| MCP tools não disponíveis | Verifique se `hydra-tools-mcp` está configurado em settings.json |
| `hydra_snippet` não encontra a função | Use o nome exato da função (case-sensitive) |
| `hydra_cache` não salva | Verifique permissões em `~\.gemini\antigravity\` |
| Budget acima de 6% | Execute `hydra audit` para identificar o que está consumindo |
| Compress não ativa em T10 | O ciclo depende do contexto; funciona quando há histórico suficiente |
| Regras HEAD-5,6,7 não aplicam | Verifique se `AGENTS.md` foi salvo corretamente em `~\.gemini\config\` |

---

<div align="center">

**HYDRA TOKENS ANTIGRAVITY v1.1.0** — *Every token saved is a battle won.*

Made with 🐍 by [@Mailor-Jorge](https://github.com/Mailor-Jorge)

</div>
