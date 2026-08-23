# Stock Spread Analyzer

Aplicação experimental para análise de pares de ações e oportunidades de spread.

## Aplicações

O projeto contém duas interfaces:

- Streamlit: `src/app.py`
- React/Vite: interface web em `src/main.tsx`

A interface React depende de uma API externa compatível com `GET /analyze-pair`. Configure o endereço com `VITE_API_URL`; o padrão é `/api`.

## Desenvolvimento

```bash
npm ci --legacy-peer-deps
npm run dev
```

## Validação frontend

```bash
npm run lint
npm run build
npm audit
```

## Streamlit

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
streamlit run src/app.py
```

No Windows, use `.venv\\Scripts\\python.exe` e `.venv\\Scripts\\streamlit.exe`.

## Dados de mercado

A função de aquisição em `src/utils/stock_data.py` deve ser conectada a uma fonte de mercado autorizada antes de uso operacional. Resultados de spread são pesquisa e não constituem recomendação de investimento.
