import math
from dataclasses import dataclass
from datetime import date
from typing import List

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Vida Leve – Guia de Dieta Saudável",
    page_icon="🥗",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Data models

@dataclass
class Meal:
    meal: str
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int
    tags: List[str]
    ingredients: List[str]


MEALS: List[Meal] = [
    Meal("Café da manhã", "Overnight oats com frutas vermelhas", 380, 18, 52, 12,
         ["vegetariano", "balanceado"],
         ["Aveia", "Iogurte grego", "Frutas vermelhas", "Chia", "Mel"]),
    Meal("Café da manhã", "Omelete de espinafre e cogumelos", 320, 26, 12, 18,
         ["low-carb", "rico em proteína"],
         ["Ovos", "Espinafre", "Cogumelos", "Cebola roxa", "Azeite"]),
    Meal("Café da manhã", "Smoothie tropical verde", 280, 14, 45, 6,
         ["vegano", "sem lactose"],
         ["Abacaxi", "Manga", "Espinafre", "Proteína vegetal", "Água de coco"]),
    Meal("Almoço", "Bowl de quinoa com grão-de-bico assado", 520, 24, 68, 16,
         ["vegano", "rico em fibra"],
         ["Quinoa", "Grão-de-bico", "Pimentão", "Abobrinha", "Tahine"]),
    Meal("Almoço", "Frango grelhado com purê de batata-doce", 560, 46, 48, 18,
         ["rico em proteína", "sem lactose"],
         ["Peito de frango", "Batata-doce", "Brócolis", "Azeite", "Ervas"]),
    Meal("Almoço", "Salmão ao forno com legumes", 610, 42, 36, 30,
         ["rico em ômega-3", "sem lactose"],
         ["Salmão", "Abobrinha", "Tomate-cereja", "Azeite", "Limão"]),
    Meal("Lanche", "Iogurte grego com castanhas e mel", 240, 16, 22, 10,
         ["balanceado", "sem glúten"],
         ["Iogurte grego", "Castanha-de-caju", "Mel", "Semente de abóbora"]),
    Meal("Lanche", "Pão sírio com homus e cenoura", 260, 10, 32, 10,
         ["vegano", "rico em fibra"],
         ["Pão sírio integral", "Homus", "Cenoura", "Azeite", "Páprica"]),
    Meal("Lanche", "Maçã com pasta de amendoim", 210, 6, 28, 10,
         ["sem lactose", "natural"],
         ["Maçã", "Pasta de amendoim 100%", "Canela"]),
    Meal("Jantar", "Tofu grelhado com arroz integral e brócolis", 540, 32, 62, 18,
         ["vegano", "rico em proteína"],
         ["Tofu", "Arroz integral", "Brócolis", "Gergelim", "Shoyu light"]),
    Meal("Jantar", "Tilápia com legumes no vapor", 460, 38, 30, 16,
         ["low-carb", "sem lactose"],
         ["Tilápia", "Couve-flor", "Vagem", "Limão", "Azeite"]),
    Meal("Jantar", "Wrap integral de frango e abacate", 510, 34, 48, 20,
         ["balanceado", "prático"],
         ["Tortilha integral", "Frango desfiado", "Abacate", "Alface", "Tomate"]),
]

ACTIVITY_LEVELS = {
    "Sedentário": 1.2,
    "Leve (1-3x/sem)": 1.375,
    "Moderado (3-5x/sem)": 1.55,
    "Ativo (6-7x/sem)": 1.725,
    "Atlético": 1.9,
}

GOAL_ADJUSTMENTS = {
    "Perder gordura": -300,
    "Manter": 0,
    "Ganhar massa": 300,
}

MACRO_SPLITS = {
    "Perder gordura": (0.35, 0.35, 0.30),
    "Manter": (0.30, 0.40, 0.30),
    "Ganhar massa": (0.30, 0.45, 0.25),
}

# -----------------------------------------------------------------------------
# Helpers

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    gender_factor = 5 if gender == "Masculino" else -161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + gender_factor


def calculate_targets(weight, height, age, gender, activity, goal):
    bmr = calculate_bmr(weight, height, age, gender)
    maintenance = bmr * ACTIVITY_LEVELS[activity]
    target_calories = maintenance + GOAL_ADJUSTMENTS[goal]
    protein_pct, carb_pct, fat_pct = MACRO_SPLITS[goal]
    calories_from_protein = target_calories * protein_pct
    calories_from_carbs = target_calories * carb_pct
    calories_from_fat = target_calories * fat_pct
    return {
        "bmr": bmr,
        "maintenance": maintenance,
        "target_calories": target_calories,
        "protein_g": calories_from_protein / 4,
        "carbs_g": calories_from_carbs / 4,
        "fat_g": calories_from_fat / 9,
    }


def filter_meals(style: str, allergies: List[str]):
    style_tag = style.lower()
    allergen_tags = {a.lower() for a in allergies}

    def is_safe(meal: Meal):
        meal_tags = {t.lower() for t in meal.tags}
        has_style = style_tag in meal_tags or style == "Flexível"
        has_allergy = any(allergen in meal_tags or allergen in map(str.lower, meal.ingredients)
                          for allergen in allergen_tags)
        return has_style and not has_allergy

    return [m for m in MEALS if is_safe(m)]


def build_meal_plan(meals: List[Meal]):
    plan = []
    seen = set()
    for option in ("Café da manhã", "Almoço", "Lanche", "Jantar"):
        for meal in meals:
            if meal.meal == option and meal.name not in seen:
                plan.append(meal)
                seen.add(meal.name)
                break
    return plan


@st.cache_data(show_spinner=False)
def grocery_list(plan: List[Meal]):
    items = {}
    for meal in plan:
        for ingredient in meal.ingredients:
            items[ingredient] = items.get(ingredient, 0) + 1
    df = pd.DataFrame(sorted(items.items()), columns=["Ingrediente", "Frequência no plano"])
    return df


# -----------------------------------------------------------------------------
# UI

st.title("🥗 Vida Leve")
st.subheader("Um hub completo para construir uma rotina alimentar saudável e prazerosa.")

with st.expander("Por que usar este app?", expanded=True):
    st.markdown(
        """
        * Calculadora personalizada de calorias e macronutrientes.
        * Planos de refeições com preferências (vegano, vegetariano, low-carb) e alertas de alergia.
        * Lista de compras inteligente e checklist de hábitos saudáveis.
        * Indicadores rápidos para hidratação, passos e sono.
        """
    )

st.divider()

left, right = st.columns([1.2, 1])

with left:
    name = st.text_input("Como quer ser chamado?", "Convidado")
    gender = st.radio("Gênero biológico (para cálculo de BMR)", ["Feminino", "Masculino"], horizontal=True)
    age = st.slider("Idade", 16, 80, 30)
    weight = st.number_input("Peso (kg)", 40.0, 180.0, 72.0, step=0.5)
    height = st.number_input("Altura (cm)", 140.0, 210.0, 172.0, step=0.5)

with right:
    st.markdown("### Objetivos e estilo")
    goal = st.selectbox("Objetivo principal", list(GOAL_ADJUSTMENTS.keys()))
    activity = st.select_slider("Nível de atividade", options=list(ACTIVITY_LEVELS.keys()), value="Moderado (3-5x/sem)")
    diet_style = st.selectbox("Estilo alimentar", ["Flexível", "Vegetariano", "Vegano", "Low-carb", "Rico em proteína"])
    allergies = st.multiselect("Restrições ou alergias", ["Lactose", "Glúten", "Castanhas", "Soja"])

st.divider()

results = calculate_targets(weight, height, age, gender, activity, goal)
macro_df = pd.DataFrame(
    {
        "Macronutriente": ["Proteína", "Carboidratos", "Gorduras"],
        "Gramas": [
            round(results["protein_g"], 1),
            round(results["carbs_g"], 1),
            round(results["fat_g"], 1),
        ],
    }
)

metric_cols = st.columns(4)
metric_cols[0].metric("BMR", f"{results['bmr']:.0f} kcal")
metric_cols[1].metric("Manutenção", f"{results['maintenance']:.0f} kcal")
metric_cols[2].metric("Calorias alvo", f"{results['target_calories']:.0f} kcal", goal)
metric_cols[3].metric("Consistência", "80/100", "Há espaço para evoluir", delta_color="off")

st.caption(f"Cálculo usando a fórmula de Mifflin-St Jeor, atualizado em {date.today():%d/%m/%Y}.")

calorie_chart = macro_df.set_index("Macronutriente")
chart_cols = st.columns([1, 1, 1])
chart_cols[0].bar_chart(calorie_chart)
chart_cols[1].progress(min(1.0, results["target_calories"] / 3500), text="Calorias vs meta semanal")
water_goal = max(2.0, round(weight * 0.035, 1))
chart_cols[2].metric("Meta diária de água", f"{water_goal} L", "Mantenha a garrafa por perto")

st.divider()

st.subheader("Plano de refeições sugerido")
filtered = filter_meals(diet_style, allergies)
plan = build_meal_plan(filtered)

if not plan:
    st.error("Ops! Não temos opções seguras combinando estilo alimentar e restrições. Ajuste os filtros.")
else:
    for meal in plan:
        with st.container(border=True):
            header = st.columns([1, 3])
            header[0].markdown(f"**{meal.meal}**")
            header[1].markdown(f"{meal.name}")
            st.markdown(
                f"Calorias: **{meal.calories} kcal** · Proteína: **{meal.protein} g** · "
                f"Carboidratos: **{meal.carbs} g** · Gorduras: **{meal.fat} g**"
            )
            st.caption("Ingredientes: " + ", ".join(meal.ingredients))

    st.markdown("---")
    groceries = grocery_list(plan)
    st.markdown("### Lista de compras condensada")
    st.dataframe(groceries, use_container_width=True)

st.subheader("Checklist de hábitos")
habit_cols = st.columns(3)
with habit_cols[0]:
    st.checkbox("Beber água a cada 90 minutos", value=True)
    st.checkbox("Planejar refeições da semana")
with habit_cols[1]:
    st.checkbox("Cozinhar com menos sal")
    st.checkbox("Adicionar 2 porções de frutas")
with habit_cols[2]:
    st.checkbox("Dormir 7-8h por noite")
    st.checkbox("Fazer 8-10 mil passos")

st.divider()

st.subheader("Sua semana em 3 metas")
weekly_df = pd.DataFrame(
    {
        "Meta": ["Passos", "Treinos", "Sono"],
        "Progresso": [8000, 3, 7],
        "Objetivo": [10000, 4, 8],
    }
)

st.dataframe(weekly_df, use_container_width=True)

progress_cols = st.columns(3)
progress_cols[0].progress(weekly_df.loc[0, "Progresso"] / weekly_df.loc[0, "Objetivo"], text="Passos")
progress_cols[1].progress(weekly_df.loc[1, "Progresso"] / weekly_df.loc[1, "Objetivo"], text="Treinos")
progress_cols[2].progress(weekly_df.loc[2, "Progresso"] / weekly_df.loc[2, "Objetivo"], text="Sono (7d)")

st.info(
    f"{name}, pequenas melhorias somadas diariamente geram resultados sólidos. "
    "Experimente repetir este plano por 7 dias e reavalie seu peso e energia!"
)
