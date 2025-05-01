import streamlit as st

# App title
st.title(" Market basket Analysis!")

# User input
name = st.text_input("Enter your name:")
fav_item = st.text_input("What's your favorite item?")

# Display output when inputs are provided
if name and fav_item:
    st.success(f"Hello, {name}! 🤝")
    st.info(f"You searched for: {fav_item}")

# Optional extras
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")