import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="حاسبة الزكاة", layout="wide", page_icon="🕌")

st.title("🕌 حاسبة الزكاة على الأسهم الأمريكية")

# تسجيل دخول
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

symbol = st.text_input("رمز الشركة (AAPL, AMD, MSFT...)", "AAPL").upper()

if st.button("حساب الزكاة", type="primary"):
    try:
        # طريقة أكثر استقراراً
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        shares = st.number_input("عدد الأسهم", min_value=1, value=100)
        market_value = shares * price
        zakat = market_value * 0.025
        
        st.success(f"**سعر {symbol}: ${price:.2f}**")
        st.info(f"القيمة السوقية: **${market_value:,.2f}**")
        st.success(f"**الزكاة المستحقة: ${zakat:,.2f}**")
        
    except:
        st.error("❌ تعذر جلب البيانات. تأكد من كتابة الرمز الصحيح (AAPL, AMD, MSFT, NVDA...)")

st.caption("© 2026 - حاسبة زكاة الأسهم")
