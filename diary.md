### 2026-10-12 – 2026-10-18

**2026-10-12**

Finalização dos slides da 1.ª sprint: próximos passos, desafios e estado da revisão de literatura sobre zero trust
Ferramenta renomeada para stackform (distribuição e comando), licença MIT, CI de testes unitários consolidada (Python 3.11/3.13), exemplo de controlo de acesso com roles e rota de login por password no servidor de desenvolvimento
Artigo da ferramenta: posicionamento face a geradores industriais e esquema OpenAPI, licença registada e nova ronda de revisão pelo orientador

### 2026-10-05 – 2026-10-11

**2026-10-11**

Preparação da apresentação da 1.ª sprint (motivação: IA, solução proposta, zero trust)
Revisão do artigo da ferramenta com base nos comentários; escolha da licença MIT após análise das licenças comuns na SoftwareX
Isolamento das credenciais do registry por deployment na ferramenta

**2026-10-08**

Desenvolvimento da plataforma X com base na ferramenta de geração de código

**2026-10-07**

Especificação de deploy v0.3 da ferramenta: runtime Docker, deploy por ambiente com Ansible, unidades systemd e pipeline de CI/CD reutilizável
Desenvolvimento da plataforma X com base na ferramenta de geração de código

**2026-10-06**

Correções no código gerado pela ferramenta: cursores assíncronos do pymongo, quebras de linha em ficheiros FastAPI (PR #120), geração de requirements/imports e validação dos contextos de build de deploy
Desenvolvimento da plataforma X com base na ferramenta de geração de código

### 2026-09-28 – 2026-10-04

**2026-10-01**

Datastores de ficheiros e tipo de campo `file` na ferramenta geradora de APIs (PR #118)

**2026-09-29**

Desenvolvimento da plataforma X com base na ferramenta de geração de código

### 2026-09-21 – 2026-09-27

**2026-09-27**

Download de template de tese da Universidade de Aveiro
Pipeline de compilação latex com github actions
Reestruturação do manuscrito como proposta de dissertação; criação de roadmap e diário

**2026-09-26**

Inicialização de repositório

**2026-09-25**

PR na ferramenta para permitir declaração de templates yaml globais - deixa de ser necessário duplicar conteúdo reutilizável em cada ficheiro onde o template é utilizado
Correção do build do site de documentação (404) e página de entrada da v0.3

**2026-09-24**

Desenvolvimento da plataforma X (pseudónimo) com base na ferramenta de geração de código

**2026-09-23**

Reunião com orientador:
- Preparar secções da análise do estado da arte
	- Arquiteturas de software
	- zero-trust
	- Ferramentas de auxílio de criação de software
	- Revisão da literatura

Presença no seminário: When Data Meets the Real World: AI, Digital Twins and Data Science for a Sustainable Future, by Professor Estanislau Lima
Verificação prévia da disponibilidade do MongoDB no comando `yaml-api run`

### 2026-09-14 – 2026-09-20

**2026-09-15**

Correção de erros na ferramenta geradora de APIs: suporte a roles nas regras de acesso v0.3 (PR #115), autorização com ligação `where` e lookup de autenticação
Finalização do primeiro rascunho do paper da ferramenta: reescrita da prosa, revisão das palavras-chave e do resumo
Presença no seminário no IEETA _A Lasting Footprint- When Viruses Stick Around. Decoding the Persistent Human Virome in Health and Disease_ por Maria Perdomo

**2026-09-14**

Artigo da ferramenta: corpo reduzido a 3881 palavras, reorganização das figuras, checklist de submissão e passagem a revisão interna

### 2026-09-07 – 2026-09-13

**2026-09-13**

Artigo da ferramenta: nome final Stackform, requisitos da SoftwareX (Guide for Authors, template v6, APC) e ajuste ao limite de palavras
Correção das referências e dos trabalhos relacionados (EMF-REST, BESSER); nova ronda de revisão adversarial

**2026-09-12**

Integração de PRs de autenticação na ferramenta: PKCE, DPoP, rotação de refresh tokens, assinatura RS256 com JWKS e cookie BFF
Paginação offset/keyset, migrações MongoDB, geração standalone de frontend e exemplos v0.3 verificados
Artigo atualizado segundo o código mais recente; revisão adversarial do manuscrito

**2026-09-11**

Integração de PRs na ferramenta: encaminhamento de inputs de serviço, conflitos únicos (409), negações de acesso explicáveis, referência da gramática de acesso e verificação de IdP
Artigo: renomeação da ferramenta para PROSE e redesenho do diagrama de arquitetura

**2026-09-10**

Reforço do parsing de bindings `where`/`given` e da autorização na v0.3 da ferramenta (PRs #75, #100, #101, #103); reposição da baseline de testes

### 2026-08-31 – 2026-09-06

**2026-09-06**

Revisão sistemática: nova pesquisa com a vertente zero-trust da RQ1 e corpus fixado em 893 registos
Triagem do corpus em dois fluxos, com calibração e adjudicação; recolha dos textos integrais de 387 relatórios
Esqueleto do artigo da revisão e figura do fluxo PRISMA

**2026-09-04**

Integração das políticas de acesso na ferramenta geradora de APIs (PR #79)
Revisão do artigo da ferramenta: figuras sobrepostas e redesenho do diagrama de componentes da arquitetura
Registo de candidatos a nome da ferramenta

**2026-09-01**

Discussão de nomes alternativos para a ferramenta geradora de APIs (renomeação provisória para "Yapify")
