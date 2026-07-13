import streamlit as st

st.set_page_config(page_title="حاسبة الزكاة", layout="wide", page_icon="🕌")

st.title("🕌 حاسبة الزكاة على الأسهم الأمريكية")

# تسجيل دخول بسيط
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("اسم المستخدم")
    if st.button("دخول"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.rerun()
    st.stop()

st.write(f"مرحباً **{st.session_state.username}**")

symbol = st.text_input("رمز الشركة (AAPL, AMD, MSFT, NVDA...)", "AAPL").upper().strip()
shares = st.number_input("عدد الأسهم", min_value=1, value=100)

if st.button("حساب الزكاة", type="primary"):
    if symbol:
        # طريقة بسيطة بدون API خارجي (للاستقرار)
        st.info("**ملاحظة:** في النسخة الحالية نحسب بناءً على سعر افتراضي أو يدوي للاستقرار.")
        
        price = st.number_input("سعر السهم الحالي ($)", value=150.0, step=0.1)
        market_value = shares * price
        zakat = market_value * 0.025
        
        st.success(f"**القيمة السوقية: ${market_value:,.2f}**")
        st.success(f"**الزكاة المستحقة: ${zakat:,.2f}**")
    else:
        st.error("أدخل رمز الشركة")

st.caption("© 2026 - حاسبة زكاة الأسهم")
