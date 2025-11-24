# 🥗 Vida Leve – App de dieta saudável

Um aplicativo em Streamlit para montar rotinas alimentares personalizadas. Ele calcula suas necessidades calóricas, sugere planos de refeições de acordo com preferências alimentares e gera uma lista de compras condensada, além de checklist de hábitos e metas semanais.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

### Como rodar localmente

1. Instale as dependências

   ```bash
   pip install -r requirements.txt
   ```

2. Execute o aplicativo

   ```bash
   streamlit run streamlit_app.py
   ```

### O que você encontra
- Calculadora de BMR, manutenção e calorias-alvo baseada na fórmula de Mifflin-St Jeor.
- Distribuição automática de macronutrientes conforme objetivo (perder gordura, manter ou ganhar massa).
- Filtros para estilo alimentar (flexível, vegetariano, vegano, low-carb, rico em proteína) e alergias comuns.
- Plano diário com sugestões de café da manhã, almoço, lanche e jantar, com ingredientes e macros por refeição.
- Lista de compras consolidada a partir do plano escolhido.
- Checklist de hábitos saudáveis e painel rápido de metas semanais.
