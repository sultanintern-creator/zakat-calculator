import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="حاسبة الزكاة", layout="wide", page_icon="🕌")

# إعدادات الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'visits' not in st.session_state:
    st.session_state.visits = 0
if 'calculations' not in st.session_state:
    st.session_state.calculations = 0

st.session_state.visits += 1

# ====================== صفحة الدخول ======================
if not st.session_state.logged_in and not st.session_state.is_admin:
    st.title("🕌 تسجيل الدخول")
    tab1, tab2 = st.tabs(["زائر", "مدير"])
    
    with tab1:
        st.subheader("تسجيل دخول زائر")
        username = st.text_input("اسم المستخدم (مثل اسمك)")
        email = st.text_input("الإيميل (اختياري)")
        if st.button("دخول كزائر"):
            if username.strip():
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success("تم تسجيل الدخول!")
                st.rerun()
    
    with tab2:
        st.subheader("دخول المدير")
        admin_user = st.text_input("اسم المستخدم المدير")
        admin_pass = st.text_input("كلمة المرور", type="password")
        if st.button("دخول كمدير"):
            if admin_user == "admin" and admin_pass == "admin2026":
                st.session_state.is_admin = True
                st.success("تم الدخول كمدير!")
                st.rerun()
            else:
                st.error("بيانات خاطئة")

else:
    # Sidebar
    with st.sidebar:
        st.title("🕌 حاسبة الزكاة")
        if st.session_state.logged_in:
            st.success(f"👤 {st.session_state.username}")
            if st.button("تسجيل خروج"):
                st.session_state.logged_in = False
                st.session_state.is_admin = False
                st.rerun()
        
        if st.session_state.is_admin:
            st.subheader("📊 إحصائيات")
            st.metric("الزيارات", st.session_state.visits)
            st.metric("الحسابات", st.session_state.calculations)
    
    # الحاسبة الرئيسية
    st.title("حاسبة الزكاة على الأسهم الأمريكية")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        symbol = st.text_input("رمز الشركة (مثال: AMD)", "AMD")
        shares = st.number_input("عدد الأسهم", min_value=1, value=100)
        
        method = st.radio("نوع الاستثمار", ["تداول / مضاربة", "استثمار طويل الأجل"])
        
        if st.button("حساب الزكاة", type="primary"):
            try:
                price_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                price = requests.get(price_url, timeout=10).json()['chart']['result'][0]['meta']['regularMarketPrice']
                market_value = shares * price
                
                ratio = 1.0 if method == "تداول / مضاربة" else 0.40
                zakat_base = market_value * ratio
                zakat = zakat_base * 0.025
                
                st.success(f"**الزكاة المستحقة: ${zakat:,.2f}**")
                st.info(f"القيمة السوقية: ${market_value:,.2f} | الوعاء: ${zakat_base:,.2f}")
                
                st.session_state.calculations += 1
            except:
                st.error("خطأ في جلب البيانات، تأكد من الرمز")
    
    with col2:
        st.metric("عدد الحسابات", st.session_state.calculations)

st.caption("© 2026 - حاسبة زكاة الأسهم")
