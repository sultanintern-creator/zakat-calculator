import streamlit as st
import pandas as pd
import json
from datetime import datetime
import requests
import time

st.set_page_config(page_title="حاسبة الزكاة", layout="wide", page_icon="🕌")

# بيانات التطبيق
if 'users' not in st.session_state:
    st.session_state.users = []
if 'calculations' not in st.session_state:
    st.session_state.calculations = 0
if 'visits' not in st.session_state:
    st.session_state.visits = 0
if 'history' not in st.session_state:
    st.session_state.history = []

st.session_state.visits += 1

# ====================== SIDEBAR ======================
st.sidebar.title("🕌 حاسبة الزكاة")

# تسجيل دخول الزائر
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    username = st.sidebar.text_input("اسم المستخدم")
    if st.sidebar.button("تسجيل الدخول"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.users.append({
                "user": username,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.sidebar.success(f"مرحباً {username}!")
        else:
            st.sidebar.warning("أدخل اسم مستخدم")
else:
    st.sidebar.success(f"👤 {st.session_state.username}")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.logged_in = False

# ====================== ADMIN PANEL ======================
st.sidebar.title("🔐 لوحة المدير")
admin_pass = st.sidebar.text_input("كلمة مرور المدير", type="password")
if st.sidebar.button("دخول مدير"):
    if admin_pass == "admin2026":   # غيرها إلى كلمة مرور قوية
        st.session_state.is_admin = True
    else:
        st.sidebar.error("كلمة مرور خاطئة")

# ====================== الصفحة الرئيسية ======================
st.title("🕌 حاسبة الزكاة على الأسهم الأمريكية")
st.markdown("**حساب دقيق وسريع لزكاة استثماراتك في السوق الأمريكي**")

if st.session_state.logged_in or st.session_state.get('is_admin', False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 البحث عن شركة")
        search = st.text_input("اكتب اسم الشركة أو الرمز (مثال: Apple أو AMD)")
        
        if search:
            try:
                url = f"https://query1.finance.yahoo.com/v1/finance/search?q={search}&quotesCount=15"
                data = requests.get(url, timeout=10).json()
                options = [f"{q['symbol']} - {q.get('shortname', '')}" for q in data.get('quotes', [])]
                selected = st.selectbox("اختر الشركة", options)
                symbol = selected.split(" - ")[0]
            except:
                symbol = st.text_input("أدخل الرمز يدوياً", "AMD")
        else:
            symbol = st.text_input("رمز الشركة", "AMD")
        
        shares = st.number_input("عدد الأسهم", min_value=1, value=100, step=1)
        
        method = st.radio("نوع الاستثمار", ["تداول / مضاربة", "استثمار طويل الأجل"])
        ratio = st.slider("نسبة الأصول الزكوية (%)", 20, 60, 40) / 100 if method == "استثمار طويل الأجل" else 1.0
        
        if st.button("🧮 حساب الزكاة", type="primary", use_container_width=True):
            try:
                # جلب السعر
                price_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                price = requests.get(price_url, timeout=8).json()['chart']['result'][0]['meta']['regularMarketPrice']
                
                market_value = shares * price
                zakat_base = market_value * ratio
                zakat = zakat_base * 0.025
                
                result = f"""
                **تقرير الزكاة - {symbol}**
                ---
                التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                المستخدم: {st.session_state.username}
                عدد الأسهم: {shares:,}
                سعر السهم: ${price:.2f}
                القيمة السوقية: ${market_value:,.2f}
                
                الطريقة: {method}
                الوعاء الزكوي: ${zakat_base:,.2f}
                **الزكاة المستحقة: ${zakat:,.2f}**
                """
                
                st.success(result)
                st.session_state.history.append(result)
                st.session_state.calculations += 1
                
            except Exception as e:
                st.error(f"خطأ في جلب البيانات: {str(e)}")
    
    with col2:
        st.subheader("📊 الإحصائيات")
        st.metric("عدد الزيارات", st.session_state.visits)
        st.metric("عدد الحسابات", st.session_state.calculations)
        st.metric("عدد المستخدمين", len(st.session_state.users))
        
        if st.session_state.get('is_admin'):
            st.subheader("👥 آخر المستخدمين")
            for u in st.session_state.users[-8:]:
                st.write(f"• {u['user']} - {u['time']}")
            
            if st.button("مسح السجلات"):
                st.session_state.history = []
                st.success("تم مسح السجلات")

else:
    st.warning("⚠️ يرجى تسجيل الدخول لاستخدام الحاسبة")
    st.info("اسم مستخدم بسيط يكفي (مثل اسمك)")

# Footer
st.caption("© 2026 - حاسبة زكاة الأسهم | للاستخدام الشخصي")
Initial commit

