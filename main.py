import streamlit as st
import pandas as pd
import ast

# App title
st.title("🛍️ Market Basket Recommendation System")
st.subheader("Get and enjoy  product recommendations based on items frequently bought together")


# User input
name = st.text_input("Enter your name:")
fav_item = st.text_input("What's your favorite item?")

# Load Association Rules CSV

@st.cache_data
def load_rules():
    rules = pd.read_csv("association_rules.csv")
    rules['antecedents'] = rules['antecedents'].apply(ast.literal_eval)
    rules['consequents'] = rules['consequents'].apply(ast.literal_eval)
    return rules

rules = load_rules()

# Display output when inputs are provided
if name and fav_item:
    st.success(f"Hello, {name}! 🤝")
    st.info(f"You searched for: {fav_item}")

# Filter strong rules

rules = rules[rules['confidence'] >= 0.5]

# Get unique item names from antecedents

item_list = sorted({item for items in rules['antecedents'] for item in items})

# User selects an item

fav_item = st.selectbox("Pick an item to see what customers often buy with it:", item_list)

# Recommendation logic

def recommend_items(picked_item, rules_df, top_n=5):
    picked_item = picked_item.lower()
    
    filtered_rules = rules_df[rules_df['antecedents'].apply(
        lambda x: picked_item in [item.lower() for item in x]
    )]

    if filtered_rules.empty:
        return pd.DataFrame([{"Message": f"No strong recommendations found for '{picked_item}'"}])
    
    top_recommendations = (
        filtered_rules
        .sort_values(by=['confidence', 'lift'], ascending=False)
        [['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        .head(top_n)
    )
    
    return top_recommendations

# Display recommendations

if fav_item:
    st.write("### Recommended Items:")
    recommendations = recommend_items(fav_item, rules)
    st.dataframe(recommendations)


# Optional extras
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")