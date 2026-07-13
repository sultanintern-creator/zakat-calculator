import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="حاسبة الزكاة", layout="wide", page_icon="🕌")

st.title("🕌 حاسبة الزكاة على الأسهم الأمريكية")

# تسجيل دخول بسيط
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("اسم المستخدم (مثل اسمك)")
    if st.button("دخول"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.rerun()
        else:
            st.warning("أدخل اسم مستخدم")
    st.stop()

# الحاسبة
st.write(f"مرحباً **{st.session_state.username}**")

symbol_input = st.text_input("رمز الشركة (مثال: AAPL أو AMD)", "AAPL")

if st.button("حساب الزكاة", type="primary"):
    try:
        # جلب السعر
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_input.upper()}"
        data = requests.get(url, timeout=10).json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        shares = st.number_input("عدد الأسهم", min_value=1, value=100)
        market_value = shares * price
        
        st.success(f"**سعر {symbol_input.upper()}: ${price:.2f}**")
        st.info(f"القيمة السوقية: **${market_value:,.2f}**")
        
        zakat = market_value * 0.025
        st.success(f"**الزكاة المستحقة: ${zakat:,.2f}**")
        
    except:
        st.error("❌ خطأ في جلب البيانات. تأكد من كتابة الرمز الصحيح (AAPL, AMD, MSFT...)")

st.caption("© 2026 - حاسبة زكاة الأسهم")
