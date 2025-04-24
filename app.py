import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# 🧠 Load Model & Product Metadata
# -----------------------------

# Load hybrid similarity matrix
with open("metadata/hybrid_similarity.pkl", "rb") as file:
    hybrid_sim = pickle.load(file)

# Load product details
products_df = pd.read_csv("metadata/products.csv")

# -----------------------------
# 🔍 Recommendation Logic
# -----------------------------
def recommend_products(product_id, num_recommendations=5):
    product_id = str(product_id)

    if product_id not in hybrid_sim.index:
        return []

    scores = hybrid_sim.loc[product_id].sort_values(ascending=False)
    recommended_products = scores.iloc[1:num_recommendations+1].index.astype(str)

    return products_df[products_df["product_id"].isin(recommended_products)][
        ["product_name", "brand_name", "price_usd"]
    ].to_dict(orient="records")

# -----------------------------
# 🎨 Streamlit App UI
# -----------------------------
st.set_page_config(page_title="Skincare Recommender", page_icon="🧴")

st.title("🧴 Sephora Skincare Recommender")
st.write("Select a skincare category and get personalized product recommendations!")

# Dropdown: Select category
categories = products_df["primary_category"].dropna().unique()
selected_category = st.selectbox("Select a category:", sorted(categories))

# Dropdown: Select product within category
filtered_products = products_df[products_df["primary_category"] == selected_category]
product_name = st.selectbox("Choose a product:", filtered_products["product_name"].unique())

# Get product ID from selected name
product_id = filtered_products.loc[
    filtered_products["product_name"] == product_name, "product_id"
].values[0]

# Slider: Number of recommendations
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=10, value=5)

# Button: Trigger recommendation
if st.button("Get Recommendations"):
    recommendations = recommend_products(product_id, num_recommendations)
    
    if recommendations:
        st.write("### Recommended Products")
        st.table(pd.DataFrame(recommendations))
    else:
        st.warning("No recommendations found for the selected product.")
