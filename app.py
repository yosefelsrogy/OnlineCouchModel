import streamlit as st
from groq import Groq

# إعداد صفحة الموقع
st.set_page_config(
    page_title="كوتش التغذية وكمال الأجسام الذكي", 
    page_icon="💪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق CSS للواجهة (دعم اللغة العربية والخط العربي العريض)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-header { text-align: center; color: #FF4B4B; font-weight: 900; margin-bottom: 5px; }
    .sub-header { text-align: center; color: #6c757d; margin-bottom: 30px; }
    .stTextInput input, .stNumberInput input, .stSelectbox select { direction: rtl; text-align: right; border-radius: 8px; }
    .info-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-right: 5px solid #FF4B4B; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# جلب مفتاح Groq API بأمان من إعدادات Streamlit Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error("⚠️ تنبيه للمطور: يرجى إضافة مفتاح GROQ_API_KEY في إعدادات Streamlit Secrets (الإعدادات السرية للموقع).")
    client = None

# System Prompt للذكاء الاصطناعي (قواعد صارمة ولهجة مصرية ودودة)
SYSTEM_INSTRUCTION = """
أنت خبير تغذية معتمد ومدرب كمال أجسام احترافي، تتحدث باللهجة المصرية المبسطة والودودة والمحفزة للمتدربين.
قواعدك الصارمة:
1. ممنوع الهلوسة نهائياً في الأرقام: اعتمد فقط على الأرقام الحسابية والسعرات والماكروز التي يرسلها لك السيستم.
2. البدائل الغذائية: التزم بالأكل المتاح في مصر والوطن العربي فقط (فراخ، لحمة، تونا، بيض، عدس، فول، أرز، بطاطس، مكرونة، جبنة قريش، شوفان، سوداني). واقترح بدائل فورية من هذه القائمة.
3. التمارين الرياضية: أجب عن أي لعبة أو تمرين رياضي واشرح أداءه الصحيح باحترافية.
"""

# القائمة الجانبية للتنقل بين أقسام التطبيق
st.sidebar.title("🎮 الأقسام الرئيسية")
app_mode = st.sidebar.radio("اختر القسم:", [
    "🌐 الشات العام (بدون تسجيل)", 
    "🔐 بروفايل المتدرب (لوحة التحكم)", 
    "📊 حاسبة السعرات الدقيقة",
    "➕ إنشاء حساب جديد"
])

st.markdown("<h1 class='main-header'>💪 الكوتش الشخصي الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>مساعدك الاحترافي لتصميم الجداول، حساب السعرات، والإجابة على كل استفساراتك الرياضية.</p>", unsafe_allow_html=True)

# قاعدة بيانات وهمية في الذاكرة لتجربة المتدربين
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "أحمد": {
            "weight": 80, "height": 175, "age": 25, "goal": "تنشيف وعضلات صافية", 
            "calories": 2400, "protein": 160, "carbs": 250, "fats": 70,
            "diet_plan": "وجبة 1: 4 بيضات مسلوقين + رغيف بلدي\nوجبة 2: 150 جرام صدور فراخ + طبق أرز مصري\nوجبة 3: علبة تونة مصفاة + سلطة\nوجبة 4: 150 جرام جبنة قريش + سوداني"
        }
    }

# 1. الشات العام (بدون تسجيل)
if app_mode == "🌐 الشات العام (بدون تسجيل)":
    st.markdown("### 💬 اسأل الكوتش عن التغذية والتمارين")
    st.info("💡 هذا القسم متاح للجميع بدون تسجيل. اسأل عن الكرياتين، التمارين، أو السعرات بشكل عام.")
    
    if "public_messages" not in st.session_state:
        st.session_state.public_messages = []

    for message in st.session_state.public_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("مثال: ما هي فوائد الكرياتين وكيف أستخدمه؟"):
        st.session_state.public_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if client is None:
                st.error("لم يتم تكوين اتصال الذكاء الاصطناعي بشكل صحيح.")
            else:
                try:
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_INSTRUCTION},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                    )
                    reply = chat_completion.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.public_messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")

# 2. بروفايل المتدرب (لوحة التحكم الخاصة)
elif app_mode == "🔐 بروفايل المتدرب (لوحة التحكم)":
    st.markdown("### 👤 بوابة المتدربين المسجلين")
    username = st.text_input("أدخل اسمك المسجل للوصول لبروفايلك وجدولك:")
    
    if username:
        if username in st.session_state.users_db:
            user_data = st.session_state.users_db[username]
            st.success(f"أهلاً بيك يا بطل، {username}! تم استدعاء بروفايلك بنجاح.")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("الوزن الحالي", f"{user_data['weight']} كجم")
            col2.metric("السعرات اليومية", f"{user_data['calories']} سعرة")
            col3.metric("البروتين المستهدف", f"{user_data['protein']} جرام")
            col4.metric("الهدف الحالي", user_data['goal'])
            
            st.markdown("---")
            st.markdown("### 🥗 جدولك الغذائي المخصص:")
            st.markdown(f"<div class='info-card'>{user_data['diet_plan'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🤖 دردش مع كوتشك الخاص:")
            
            chat_key = f"chat_{username}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = []

            for msg in st.session_state[chat_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_prompt = st.chat_input("اطلب تعديل، بديل لأكلة غير متوفرة، أو استشر الكوتش...")
            if user_prompt:
                st.session_state[chat_key].append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                with st.chat_message("assistant"):
                    contextual_prompt = f"""
                    بيانات المتدرب الحالي:
                    الاسم: {username}
                    الوزن: {user_data['weight']} كجم
                    الهدف: {user_data['goal']}
                    السعرات والماكروز: {user_data['calories']} سعرة، بروتين {user_data['protein']}ج.
                    الجدول الحالي: {user_data['diet_plan']}
                    طلب المتدرب: {user_prompt}
                    """
                    if client is None:
                        st.error("لم يتم تكوين اتصال الذكاء الاصطناعي.")
                    else:
                        try:
                            chat_completion = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                                    {"role": "user", "content": contextual_prompt}
                                ],
                                temperature=0.7,
                            )
                            reply = chat_completion.choices[0].message.content
                            st.markdown(reply)
                            st.session_state[chat_key].append({"role": "assistant", "content": reply})
                        except Exception as e:
                            st.error(f"خطأ: {e}")
        else:
            st.warning("⚠️ هذا الاسم غير مسجل. انتقل لقسم 'إنشاء حساب جديد' لتسجيل بروفايلك.")

# 3. حاسبة السعرات الدقيقة
elif app_mode == "📊 حاسبة السعرات الدقيقة":
    st.markdown("### 🧮 حاسبة السعرات والماكروز (بدون هلوسة)")
    
    col1, col2 = st.columns(2)
    with col1:
        w = st.number_input("الوزن (كجم):", min_value=30.0, max_value=200.0, value=75.0)
        h = st.number_input("الطول (سم):", min_value=100.0, max_value=230.0, value=175.0)
    with col2:
        age = st.number_input("العمر (سنوات):", min_value=12, max_value=80, value=25)
        activity = st.selectbox("مستوى النشاط الأسبوعي:", [
            "قليل الحركة (تمرن نادراً)", 
            "نشاط خفيف (تمرن 1-3 أيام)", 
            "نشاط متوسط (تمرن 3-5 أيام)", 
            "نشاط عالي (تمرن بقوة 6-7 أيام)"
        ])

    goal_type = st.selectbox("هدفك الحالي:", ["تنشيف (خسارة الدهون)", "تضخيم (بناء العضلات)", "ثبات الوزن وصيانة القوام"])

    if st.button("احسب سعراتي الآن", use_container_width=True):
        bmr = (10 * w) + (6.25 * h) - (5 * age) + 5
        multiplier = 1.2
        if "خفيف" in activity: multiplier = 1.375
        elif "متوسط" in activity: multiplier = 1.55
        elif "عالي" in activity: multiplier = 1.725
        
        tdee = bmr * multiplier
        final_cals = tdee - 500 if "تنشيف" in goal_type else (tdee + 300 if "تضخيم" in goal_type else tdee)
            
        protein = w * 2.2
        fats = (final_cals * 0.25) / 9
        carbs = (final_cals - ((protein * 4) + (fats * 9))) / 4
        
        st.success(f"🔥 سعرات الثبات الخاصة بك (TDEE): **{int(tdee)} سعرة حرارية**")
        st.info(f"🎯 السعرات المطلوبة لهدفك ({goal_type}): **{int(final_cals)} سعرة حرارية**")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("البروتين اليومي", f"{int(protein)} جرام")
        col_m2.metric("الكربوهيدرات", f"{int(carbs)} جرام")
        col_m3.metric("الدهون الصحية", f"{int(fats)} جرام")

# 4. إنشاء حساب جديد
elif app_mode == "➕ إنشاء حساب جديد":
    st.markdown("### 📝 تسجيل بروفايل جديد للمتدرب")
    
    new_name = st.text_input("اختر اسمك أو كودك السري:")
    col_1, col_2 = st.columns(2)
    with col_1:
        new_w = st.number_input("الوزن (كجم):", value=75.0, key="nw")
        new_h = st.number_input("الطول (سم):", value=175.0, key="nh")
    with col_2:
        new_age = st.number_input("العمر:", value=24, key="nage")
        new_goal = st.selectbox("الهدف الأساسي:", ["تنشيف وعضلات صافية", "تضخيم عضلي وزيادة وزن", "ثبات وصحة عامة"])
    
    if st.button("حفظ البروفايل وإنشاء الحساب", use_container_width=True):
        if new_name:
            cals = 2500 if "تضخيم" in new_goal else 2200
            prot = int(new_w * 2.2)
            st.session_state.users_db[new_name] = {
                "weight": new_w, "height": new_h, "age": new_age, "goal": new_goal,
                "calories": cals, "protein": prot, "carbs": 250, "fats": 70,
                "diet_plan": f"وجبة 1: بيض مسلوق + رغيف بلدي\nوجبة 2: أرز مصري + صدور فراخ\nوجبة 3: علبة تونة + سلطة"
            }
            st.success(f"🎉 تم إنشاء الحساب بنجاح يا بطل ({new_name})! انتقل الآن لـ 'بروفايل المتدرب' وادخل باسمك لاستعراض جدولك.")
        else:
            st.error("برجاء كتابة الاسم أو الكود بشكل صحيح.")
