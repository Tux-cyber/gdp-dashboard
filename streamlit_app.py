import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(
    page_title='VivaFit - Dieta Saudável Premium',
    page_icon=':green_apple:',
    layout='wide'
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f1fff1 0%, #fdfdfd 40%, #f6fff6 100%);
        color: #1b4332;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3, h4 {
        font-weight: 700 !important;
        color: #1b4332 !important;
    }
    .hero {
        background: radial-gradient(circle at top left, #95d5b2, #52b788);
        color: white;
        padding: 3.5rem;
        border-radius: 28px;
        margin-bottom: 2rem;
        box-shadow: 0 30px 60px rgba(82, 183, 136, 0.25);
    }
    .hero h1 { font-size: 3rem; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.2rem; margin-bottom: 1.5rem; }
    .cta-button {
        display: inline-block;
        background: #2d6a4f;
        color: white;
        padding: 0.9rem 2.8rem;
        border-radius: 999px;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 18px 35px rgba(45, 106, 79, 0.35);
    }
    .cta-button:hover {
        background: #1b4332;
        transform: translateY(-2px);
        box-shadow: 0 25px 45px rgba(45, 106, 79, 0.4);
    }
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 20px 35px rgba(0,0,0,0.07);
        height: 100%;
    }
    .pricing-card {
        border: 2px solid #74c69d;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .pricing-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 28px 45px rgba(116,198,157,0.35);
    }
    .badge {
        display: inline-block;
        background: #2d6a4f;
        color: white;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .metric-label { color: #2d6a4f; font-weight: 600; }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #2d6a4f;
        font-size: 0.9rem;
    }
    .section-title {
        font-size: 1.9rem;
        margin-bottom: 1.2rem;
        position: relative;
        padding-bottom: 0.5rem;
    }
    .section-title:after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 60px;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #52b788, #1b4332);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='hero'>
        <div class='badge'>Experiência premium</div>
        <h1>VivaFit: a jornada completa para uma vida saudável</h1>
        <p>Planos alimentares personalizados, orientação profissional e uma comunidade inspiradora. Tudo o que você precisa para transformar seu bem-estar em um estilo de vida sustentável.</p>
        <a class='cta-button' href='#assessment'>Começar minha transformação</a>
    </div>
    """,
    unsafe_allow_html=True
)

col_highlights = st.columns(4)
highlights = [
    ("🍽️", "Chef & Nutri", "Receitas gourmet aprovadas por nutricionistas"),
    ("🧬", "Bioindividual", "Planos adaptados ao seu metabolismo"),
    ("📊", "Métricas inteligentes", "Painel completo para acompanhar resultados"),
    ("🤝", "Apoio 360º", "Mentorias, desafios e comunidade exclusiva"),
]

for col, (icon, title, subtitle) in zip(col_highlights, highlights):
    with col:
        st.markdown(
            f"""
            <div class='card'>
                <div style='font-size:2.4rem'>{icon}</div>
                <h3 style='margin-top:0.8rem'>{title}</h3>
                <p style='margin-bottom:0'>{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<a id='assessment'></a>", unsafe_allow_html=True)
st.markdown("## Diagnóstico premium")
st.write("Personalize sua experiência em menos de 60 segundos e receba um direcionamento inicial exclusivo.")

with st.form("assessment_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        goal = st.selectbox(
            "Qual é o seu principal objetivo?",
            [
                "Perder gordura com saúde",
                "Ganho de massa magra",
                "Melhorar disposição e imunidade",
                "Reeducação alimentar equilibrada"
            ]
        )
        meals = st.slider("Quantas refeições completas você deseja por dia?", 3, 6, 4)
        hydration = st.number_input("Litros de água que costuma consumir diariamente", 0.5, 5.0, 1.8, 0.1)
    with col_b:
        preference = st.multiselect(
            "Quais estilos alimentares fazem sentido para você?",
            ["Mediterrânea", "Low carb consciente", "Plant-based flexível", "Sem glúten", "Sem lactose", "Proteínas de alto valor biológico"]
        )
        activity = st.select_slider(
            "Nível atual de atividade física",
            options=["Iniciante", "Intermediário", "Avançado"],
            value="Intermediário"
        )
        restrictions = st.text_input("Alguma restrição ou observação importante?", placeholder="Ex.: alergia a castanhas, rotina de plantão...")

    submitted = st.form_submit_button("Gerar insight personalizado")

if submitted:
    goal_messages = {
        "Perder gordura com saúde": "Foque em um déficit calórico leve com densidade nutricional alta. Vamos sugerir fibras, ômega 3 e proteínas magras para manter saciedade.",
        "Ganho de massa magra": "Aumente a ingestão proteica distribuída ao longo do dia e garanta carboidratos complexos no pré e pós-treino.",
        "Melhorar disposição e imunidade": "Priorize alimentos ricos em micronutrientes, cores vivas no prato e rotinas de sono consistentes.",
        "Reeducação alimentar equilibrada": "Equilíbrio é chave: combinamos técnicas de mindful eating com variações de texturas e sabores."
    }
    hydration_tip = "Ótima hidratação!" if hydration >= 2 else "Podemos trabalhar com estratégias para aumentar sua ingestão de água ao longo do dia."
    st.success(
        f"{goal_messages.get(goal)} {hydration_tip} Nossa equipe premium entrará em contato para montar o plano completo baseado nas suas escolhas."  # noqa: E501
    )
    preference_text = ", ".join(preference) if preference else "Preferências flexíveis"
    st.info(
        f"Seu plano incluirá {meals} refeições completas por dia, com foco em: {preference_text}. Consideraremos seu nível {activity.lower()} de atividade física para ajustar calorias e timing ideal."
    )
    if restrictions:
        st.warning(f"Anotamos sua observação: {restrictions}.")

st.markdown("## Planos alimentares de alta performance")
st.write("Um gostinho do que entregamos semanalmente para os assinantes VivaFit Prime.")

weekly_meal_plan = pd.DataFrame([
    {
        "Dia": "Segunda",
        "Café da manhã": "Panqueca proteica com frutas vermelhas",
        "Almoço": "Salmão grelhado, quinoa de ervas e aspargos",
        "Jantar": "Risoto de couve-flor com camarões",
        "Snacks premium": "Mix de oleaginosas e kombucha",
        "Calorias": 1850,
    },
    {
        "Dia": "Terça",
        "Café da manhã": "Overnight oats com chia e manga",
        "Almoço": "Frango orgânico ao pesto, batata-doce roxa e salada de rúcula",
        "Jantar": "Sopa tailandesa de leite de coco com tofu",
        "Snacks premium": "Hummus com crudités e kefir",
        "Calorias": 1800,
    },
    {
        "Dia": "Quarta",
        "Café da manhã": "Smoothie verde detox com spirulina",
        "Almoço": "Buddha bowl mediterrâneo",
        "Jantar": "Nhoque de mandioquinha ao sugo fresco",
        "Snacks premium": "Iogurte grego com granola artesanal",
        "Calorias": 1780,
    },
    {
        "Dia": "Quinta",
        "Café da manhã": "Tapioca recheada com queijo de castanhas",
        "Almoço": "Filé mignon com purê de couve-flor",
        "Jantar": "Sushi bowl com arroz negro",
        "Snacks premium": "Brownie funcional de cacau 70%",
        "Calorias": 1900,
    },
    {
        "Dia": "Sexta",
        "Café da manhã": "Avocado toast com ovo pochê",
        "Almoço": "Moqueca de peixe leve",
        "Jantar": "Wrap integral de peru com legumes crocantes",
        "Snacks premium": "Chips de grão-de-bico",
        "Calorias": 1820,
    },
    {
        "Dia": "Sábado",
        "Café da manhã": "Crepioca doce com recheio de banana caramelizada",
        "Almoço": "Risoto de cogumelos trufados",
        "Jantar": "Pizza integral de burrata e tomate confit",
        "Snacks premium": "Sorbet de frutas naturais",
        "Calorias": 1950,
    },
    {
        "Dia": "Domingo",
        "Café da manhã": "Waffle proteico com mel de abelha nativa",
        "Almoço": "Feijoada leve com vegetais",
        "Jantar": "Sopa de abóbora com gengibre e leite de coco",
        "Snacks premium": "Golden milk relaxante",
        "Calorias": 1880,
    },
])

st.dataframe(
    weekly_meal_plan,
    use_container_width=True,
    column_config={
        "Calorias": st.column_config.NumberColumn("Calorias (kcal)", format="%d"),
    }
)

st.markdown("## Experiência gourmet + ciência")
st.write("Receitas exclusivas com ingredientes frescos, sazonalidade respeitada e tecnologia para acompanhar a evolução do seu corpo.")

recipes = [
    {
        "title": "Bowl antioxidante com salmão selvagem",
        "details": "29g de proteína | Rico em ômega 3 | Pronto em 15 minutos",
    },
    {
        "title": "Moqueca plant-based de grão-de-bico",
        "details": "Sem glúten e lactose | Temperos brasileiros | Fonte de fibras",
    },
    {
        "title": "Cheesecake raw de frutas amarelas",
        "details": "Sobremesa funcional | Zero açúcar refinado | Probióticos naturais",
    },
]

col_recipe = st.columns(3)
for col, recipe in zip(col_recipe, recipes):
    with col:
        st.markdown(
            f"""
            <div class='card'>
                <span class='badge'>Chef signature</span>
                <h3>{recipe['title']}</h3>
                <p>{recipe['details']}</p>
                <ul>
                    <li>Ficha nutricional completa</li>
                    <li>Videoaulas passo a passo</li>
                    <li>Lista inteligente de compras</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("## Monitoramento e evolução")
st.write("Tecnologia proprietária para garantir que cada marco da sua jornada seja celebrado e ajustado em tempo real.")

progress_df = pd.DataFrame({
    "Semana": list(range(1, 9)),
    "Peso (kg)": [72.0, 71.2, 70.5, 69.7, 69.0, 68.5, 67.9, 67.2],
    "Energia": [55, 62, 68, 72, 78, 82, 87, 90],
})

progress_long = progress_df.melt("Semana", var_name="Indicador", value_name="Valor")
chart = (
    alt.Chart(progress_long)
    .mark_line(point=True)
    .encode(
        x=alt.X('Semana:O', title='Semana do programa'),
        y=alt.Y('Valor:Q', title='Valor monitorado'),
        color=alt.Color('Indicador:N', scale=alt.Scale(range=['#2d6a4f', '#95d5b2'])),
        tooltip=['Indicador', 'Valor', 'Semana']
    )
    .properties(height=360)
)

st.altair_chart(chart, use_container_width=True)

metrics_col = st.columns(3)
metrics = [
    ("Tempo médio para resultados visíveis", "21 dias"),
    ("Índice de satisfação dos membros", "97%"),
    ("Protocolos exclusivos desenvolvidos", "58"),
]

for col, (label, value) in zip(metrics_col, metrics):
    with col:
        st.metric(label=label, value=value)

st.markdown("## Depoimentos reais")
st.write("Histórias de transformação que mostram que saúde e prazer podem caminhar juntos.")

st.markdown(
    """
    > "Em 3 meses eliminei 9 kg sem abrir mão dos encontros sociais. O suporte da equipe VivaFit foi essencial para aprender a equilibrar."  
    > — **Marina Costa, 34 anos**

    > "O plano premium é realmente personalizado. As receitas são deliciosas e o acompanhamento dos coaches me manteve consistente."  
    > — **Felipe Andrade, 41 anos**

    > "Sou vegetariana e nunca encontrei tantas opções criativas. A comunidade me inspira diariamente."  
    > — **Lia Gomes, 29 anos**
    """
)

st.markdown("## Planos de assinatura VivaFit")
st.write("Escolha a combinação perfeita de nutrição, tecnologia e suporte humano.")

planos = [
    {
        "nome": "Essencial", "valor": "R$ 189/mês", "beneficios": [
            "Plano alimentar atualizado mensalmente",
            "Aplicativo com metas diárias",
            "Suporte por chat em horário comercial",
        ]
    },
    {
        "nome": "Prime", "valor": "R$ 289/mês", "beneficios": [
            "Cardápio semanal com receitas gourmet",
            "Consultas quinzenais com nutricionista",
            "Relatórios de bioimpedância e ajustes", "Acesso completo à comunidade",
        ]
    },
    {
        "nome": "Signature", "valor": "R$ 489/mês", "beneficios": [
            "Plano integrado com personal trainer",
            "Suporte 24/7 com coach dedicado",
            "Sessões exclusivas de meditação guiada",
            "Evento trimestral com experiências gastronômicas",
        ]
    },
]

col_planos = st.columns(3)
for col, plano in zip(col_planos, planos):
    with col:
        beneficios_html = "".join([f"<li>{beneficio}</li>" for beneficio in plano["beneficios"]])
        st.markdown(
            f"""
            <div class='card pricing-card'>
                <span class='badge'>{plano['nome']} premium</span>
                <h3 style='font-size:1.8rem'>{plano['valor']}</h3>
                <ul style='padding-left:1.2rem'>{beneficios_html}</ul>
                <a class='cta-button' href='mailto:contato@vivafit.com'>Quero aderir</a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("## Perguntas frequentes")

faq = {
    "Como funciona a personalização do plano?": "Após o diagnóstico inicial, um nutricionista avalia seus dados, hábitos e objetivos. Em até 24h você recebe um plano sob medida, com ajustes semanais conforme feedback e indicadores.",
    "Existe acompanhamento médico?": "Sim. Trabalhamos com uma equipe multidisciplinar. Conforme necessidade, realizamos encaminhamento para médico nutrólogo ou endocrinologista da nossa rede parceira.",
    "Posso pausar a assinatura?": "Você pode pausar por até 60 dias sem perder o acesso às receitas e à comunidade, mantendo o valor promocional vigente.",
    "Vocês atendem restrições alimentares?": "Sim. Adaptamos cardápios para alergias, intolerâncias e escolhas éticas, sempre com curadoria de ingredientes frescos e confiáveis.",
}

for pergunta, resposta in faq.items():
    with st.expander(pergunta):
        st.write(resposta)

st.markdown("## Conteúdos e eventos exclusivos")
st.write("Muito além de um plano alimentar: experiências completas de saúde e lifestyle.")

col_events = st.columns(3)
items = [
    ("Masterclasses mensais", "Aulas com chefs renomados, especialistas em nutrição e bem-estar holístico."),
    ("Retiro VivaFit", "Imersões trimestrais em destinos naturais com programação detox, yoga e trilhas."),
    ("Clube de vinhos naturais", "Harmonizações guiadas para momentos especiais com equilíbrio."),
]

for col, (title, description) in zip(col_events, items):
    with col:
        st.markdown(
            f"""
            <div class='card'>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("## Pronto para viver o seu melhor capítulo?")
st.write("Nossa concierge premium entra em contato em até 2 horas úteis para apresentar a proposta completa.")

with st.form("contact_form"):
    col_left, col_right = st.columns(2)
    with col_left:
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone/WhatsApp")
    with col_right:
        melhor_horario = st.selectbox("Melhor horário para contato", ["Manhã", "Tarde", "Noite"])
        preferencia_contato = st.selectbox("Preferência de contato", ["WhatsApp", "Telefone", "E-mail"])
        data_interesse = st.date_input("Quando deseja iniciar?", value=datetime.today())
    objetivos = st.text_area("Conte-nos brevemente sobre seus objetivos")
    contato_submit = st.form_submit_button("Solicitar proposta personalizada")

if contato_submit:
    st.success("Recebemos seu pedido! Nossa concierge entrará em contato com você em breve.")

st.markdown(
    """
    <div class='footer'>
        VivaFit © {ano} · Saúde em primeiro lugar · contato@vivafit.com · @vivafit.oficial
    </div>
    """.format(ano=datetime.now().year),
    unsafe_allow_html=True
)
