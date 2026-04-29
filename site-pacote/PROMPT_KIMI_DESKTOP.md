# Prompt para Criação do Site — Kimi Desktop

> Use este prompt no Kimi Desktop para gerar um site estático completo a partir deste pacote de dados.

---

## 🎯 INSTRUÇÃO PRINCIPAL

Crie um **site estático moderno e responsivo** (HTML/CSS/JS puro ou framework leve como Astro/VitePress) para divulgar os resultados do projeto de pesquisa:

> **"Crise, migração e trabalho: trajetórias migrantes de venezuelanos no Oeste de Santa Catarina"**
>
> Coordenação: Prof. Dr. Vicente Neves da Silva Ribeiro (UFFS) e Prof. Dr. Leonardo Rafael Santos Leitão (UFFS)

O site deve ter **aparência acadêmica mas acessível**, com visualização de dados interativa quando possível, e deve ser totalmente em **português brasileiro**.

---

## 📑 ESTRUTURA DE PÁGINAS SUGERIDA

### 1. Página Inicial (`index.html`)
- **Hero section** com título do projeto, subtítulo explicativo e foto/ilustração representativa
- Destaque para os **3 números principais** em cards grandes:
  - **226.945** vínculos de emprego (RAIS 2018–2024)
  - **14.661** internações hospitalares (SIH/SUS 2018–2025)
  - **109** municípios da Região Intermediária de Chapecó
- Breve apresentação dos coordenadores com afiliação UFFS
- Botão "Explore os Dados" levando ao dashboard

### 2. Página "Sobre o Projeto" (`sobre.html`)
- Contexto da crise venezuelana e migração para o Brasil
- Por que o Oeste de SC? (agronegócio, frigoríficos, demanda laboral)
- Descrição dos objetivos de pesquisa
- Metodologia resumida (fontes: RAIS, SIH/SUS, IBGE)
- **Limitações importantes**: SIM/SINASC sem nacionalidade; CAGED sem filtro de nacionalidade
- Ficha técnica com coordenadores, instituição (UFFS), período de análise

### 3. Dashboard Interativo (`dashboard.html`)
Esta é a página principal de dados. Organize em seções:

#### Seção A: Emprego e Vínculos (RAIS)
- Figura 01: Evolução regional de vínculos 2018–2024
- Figura 03: Top 15 municípios por volume (2024)
- Figura 04: Dispersão população vs vínculos (R²=0,912)
- Figuras 08 e 09: Mapas coropléticos (taxa per capita e volume absoluto)
- GIF 10: Animação da evolução espacial 2018–2024
- GIF 11: Bar chart race dos top 15 municípios
- **Tabela interativa** com os dados do painel CSV (os 109 municípios, ordenável)

#### Seção B: Perfil Demográfico
- Figura 12: Pirâmide etária comparativa (venezuelanos vs população total)
- Figura 13: Distribuição percentual por faixa etária
- Figura 17: Índice de concentração etária (super-representação)
- Destaque em texto: 70% dos venezuelanos têm 25–49 anos (perfil laboral)

#### Seção C: Saúde e Morbidade (SIH/SUS)
- Figura 05: Evolução das internações hospitalares
- Figura 06: Comparativo RAIS vs SIH (2024)
- Figura 07: Correlação taxa de internações vs vínculos (R²=0,329)
- Figura 14: Heatmap CIDs × municípios
- Figura 15: Composição da morbidade por capítulo CID
- Figura 16: Evolução temporal dos 5 principais CIDs
- **Destaque**: 40% das internações são gravidez/parto; O800 (parto espontâneo) é o principal CID

### 4. Página "Municípios em Destaque" (`municipios.html`)
- Cards individuais para os 10 municípios com mais vínculos
- Cada card com: nome, população, vínculos RAIS, taxa per mil, internações SIH, principal CID
- Destaque especial para **Chapecó** (16.177 vínculos, polo regional)
- Destaque para **Guatambú** (maior taxa: 278,7 per mil — pequeno município, alta concentração)
- Mapa interativo simples (embed do coroplético como imagem clicável)

### 5. Página "Dados e Download" (`dados.html`)
- Tabela com metadados das bases utilizadas
- Links para download dos arquivos CSV e imagens
- Descrição de cada variável do painel longitudinal
- Nota sobre reprodutibilidade e pipeline de dados

---

## 🎨 DIRETRIZES DE DESIGN

### Paleta de Cores (sugestão)
- **Primária:** `#1a5276` (azul acadêmico profundo)
- **Secundária:** `#e67e22` (laranja/laranja-queimado — representa energia/migração)
- **Destaque:** `#c0392b` (vermelho — alertas, dados críticos)
- **Neutros:** `#f8f9fa` (fundo), `#2c3e50` (texto)
- **Mapas:** Use `YlOrRd` para coropléticos (mesma escala do projeto: 0–280)

### Tipografia
- Títulos: Inter ou Montserrat (sans-serif moderna)
- Corpo: Merriweather ou Georgia (serif para leitura longa)
- Dados/destaques: JetBrains Mono (monospace para números)

### Componentes
- Cards com sombra sutil e bordas arredondadas (`border-radius: 8px`)
- Gráficos em containers com título e legenda descritiva
- Tooltips nos números principais explicando o que significam
- Layout responsivo (mobile-first)
- Navbar fixa no topo com links suaves

### Estilo Visual
- Clean, acadêmico, mas não austero
- Use as próprias figuras do pacote (são de alta resolução, 2000–4000px)
- GIFs animados devem ser exibidos como elementos centrais
- Tabelas devem ter zebra-striping e ser ordenáveis (use DataTables.js ou similar)

---

## 🔧 FUNCIONALIDADES TÉCNICAS

1. **Menu de navegação fixo** com âncoras suaves
2. **Botão "Voltar ao topo"** após scroll
3. **Lazy loading** nas imagens (são grandes)
4. **Lightbox** para ampliar figuras ao clicar
5. **Tabela ordenável** para os dados do painel CSV
6. **SEO básico**: meta tags, Open Graph, descrição
7. **Footer** com:
   - Logo/nome da UFFS
   - Nomes dos coordenadores com links para Lattes (se disponível)
   - Ano de atualização (2026)
   - Licença CC-BY-SA 4.0 (sugestão)

---

## 📝 CONTEÚDO TEXTO-CHAVE PARA INCORPORAR

### Introdução
> A crise humanitária, política e econômica na Venezuela a partir de 2015 desencadeou o maior êxodo da história recente da América Latina. Com mais de 7 milhões de venezuelanos em situação de deslocamento forçado, o Brasil tornou-se um dos principais países de destino. No interior do país, a Região Intermediária de Chapecó, no Oeste de Santa Catarina, emergiu como um dos polos mais dinâmicos de absorção dessa migração, impulsionada pela expansão do agronegócio e da agroindústria.

### Destaque — Crescimento Exponencial
> Entre 2018 e 2024, o número de vínculos de emprego de venezuelanos na RAIS cresceu de 1.069 para mais de 74 mil em todo SC. No Oeste, a concentração é ainda mais acentuada: Chapecó sozinha concentra 16.177 vínculos em 2024, enquanto municípios como Guatambú, Itapiranga e Seara apresentam taxas de vínculos per capita superiores a 100 por mil habitantes — indicando uma presença proporcionalmente massiva da população venezuelana.

### Destaque — Perfil de Saúde
> A análise de 14.661 internações hospitalares de venezuelanos em SC revela um perfil de morbidade dominado por **gravidez e parto (40% do total)**. O CID O800 (parto único espontâneo) lidera com 931 registros, seguido por O809 (parto por cesariana) com 389. Esse padrão reflete a presença massiva de mulheres venezuelanas em idade fértil na região, muitas delas em trabalhos informais ou sem acesso pleno ao pré-natal.

### Destaque — Perfil Etário
> A pirâmide etária dos venezuelanos no Oeste SC é radicalmente diferente da população local: **70% dos vínculos estão na faixa de 25 a 49 anos**, praticamente zero adolescentes (14–17 anos) e idosos (65+). Isso confirma o caráter essencialmente laboral da migração — são adultos jovens que migram para trabalhar.

---

## 📤 OUTPUT ESPERADO

Ao final, o Kimi Desktop deve produzir:

1. Um diretório `site/` com todos os arquivos HTML, CSS, JS
2. Imagens da pasta `figuras/` copiadas para `site/assets/figuras/`
3. Dados CSV em `site/assets/dados/`
4. Um arquivo `README.md` no site com instruções de deploy (GitHub Pages, Netlify, etc.)
5. O site deve ser **estático** (não requer backend) e **pronto para deploy**

---

## ⚠️ RESTRIÇÕES

- NÃO invente dados que não estejam no pacote
- NÃO crie gráficos que não correspondam às figuras fornecidas
- Use os valores exatos das tabelas e figuras
- Mantenha a atribuição correta aos coordenadores e à UFFS
- O site deve ser em português do Brasil
