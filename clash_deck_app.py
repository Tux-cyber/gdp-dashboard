import streamlit as st
import pandas as pd
import random
from pathlib import Path

@st.cache_data(ttl=24*60*60)
def load_card_data():
    """Load Clash Royale card data. The data file can be updated over time."""
    data_file = Path(__file__).parent / 'data' / 'clash_cards.csv'
    return pd.read_csv(data_file)

SYNERGY_PAIRS = {
    ('Hog Rider', 'Fireball'): 1.0,
    ('Balloon', 'Freeze'): 1.0,
    ('Golem', 'Baby Dragon'): 1.0,
    ('Royal Giant', 'Lightning'): 1.0,
    ('Miner', 'Poison'): 1.0,
    ('X-Bow', 'Tesla'): 1.0,
    ('Rocket', 'X-Bow'): 1.0,
    ('P.E.K.K.A', 'Bandit'): 1.0,
    ('Mortar', 'Log'): 1.0,
}

def score_deck(deck_df: pd.DataFrame) -> float:
    """Simple scoring for a deck."""
    elixir_mean = deck_df['elixir'].mean()
    score = -abs(elixir_mean - 3.5)
    cards = set(deck_df['card'])
    for pair, val in SYNERGY_PAIRS.items():
        if set(pair).issubset(cards):
            score += val
    return score

def generate_deck(cards_df: pd.DataFrame):
    best_score = -999
    best_deck = None
    for _ in range(200):
        building = cards_df[cards_df['type'] == 'building'].sample(1)
        spell = cards_df[cards_df['type'] == 'spell'].sample(1)
        remaining = cards_df[~cards_df['card'].isin(pd.concat([building, spell])['card'])].sample(6)
        deck = pd.concat([building, spell, remaining])
        deck_score = score_deck(deck)
        if deck_score > best_score:
            best_score = deck_score
            best_deck = deck
    return best_deck.reset_index(drop=True), best_score

def main():
    st.set_page_config(page_title='Clash Royale Deck Generator', page_icon='\u2694')
    st.title('Clash Royale Deck Generator')
    st.write('Este gerador usa uma IA simples para sugerir decks balanceados. O conjunto de cartas pode ser atualizado a qualquer momento para refletir as mudan\u00e7as do jogo.')
    cards_df = load_card_data()
    if st.button('Gerar novo deck'):
        deck, score = generate_deck(cards_df)
    else:
        deck, score = generate_deck(cards_df)
    avg_elixir = deck['elixir'].mean()
    st.subheader(f'Custo m\u00e9dio de elixir: {avg_elixir:.2f}')
    st.subheader(f'Pontua\u00e7\u00e3o do deck: {score:.2f}')
    for idx, row in deck.iterrows():
        st.write(f"{row['card']} ({row['elixir']} elixir)")

if __name__ == '__main__':
    main()
