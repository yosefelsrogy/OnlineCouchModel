import streamlit as st
import google.generativeai as genai

# إعداد صفحة الموقع بالعربي وتنسيق اليمين لليسار (RTL)
st.set_page_config(
    page_title="كوتش التغذية وكمال الأجسام الذكي", 
    page_icon="💪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم وتنسيق CSS لدعم اللغة العربية بشكل احترافي وجذاب
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# عنوان الموقع الرئيسي
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💪 الكوتش الشخصي الذكي - تغذية وكمال أجسام</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>مساعدك الاحترافي لحساب السعرات، وتصميم الجداول، والرد على كل استفساراتك التدريبية.</p>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# إعداد الاتصال بـ Google Gemini API
# -----------------------------------------------------------------
# يمكنك وضع مفتاح الـ API مباشرة هنا بين العلامتين أو عبر Streamlit Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاح_الـ_API_هنا")

if API_KEY == "ضع_مفتاح_الـ_API_هنا":
    st.warning("⚠️ تنبيه: يرجى وضع مفتاح Google AI Studio API Key الخاص بك لكي يعمل الذكاء الاصطناعي بسلاسة.")
else:
    genai.configure(api_key=API_KEY)

#System Prompt الصارم والاحترافي لتوجيه الـ AI
SYSTEM_INSTRUCTION = """
أنت خبير تغذية معتمد ومدرب كمال أجسام احترافي، تتحدث باللهجة المصرية المبسطة والودودة والمحفزة للمتدربين.
قواعدك الصارمة التي لا يمكنك حيادها:
1. ممنوع الهلوسة نهائياً في الأرقام: اعتمد فقط على الأرقام الحسابية والسعرات والماكروز التي يرسلها لك السيستم أو الكود في المحادثة.
2. البدائل الغذائية: التزم بالأكل المتاح في مصر والوطن العربي فقط (فراخ، لحمة، تونا، بيض، عدس، فول، أرز، بطاطس، مكرونة، جبنة قريش، شوفان، سوداني). وإذا سألك المتدرب عن بديل، اقترح فوراً بديلاً من هذه القائمة بنفس القيمة الغذائية والسعرات.
3. التمارين الرياضية: أجب عن أي لعبة أو تمرين رياضي، واشرح أداءه الصحيح والعضلات المستهدفة باحترافية تامة.
"""

generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 1200,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

# -----------------------------------------------------------------
# محاكاة قاعدة بيانات المتدربين (يمكن ربطها لاحقاً بـ Google Sheets أو قاعدة بيانات حقيقية)
# -----------------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "أحمد": {
            "weight": 80, "height": 175, "age": 25, "goal": "تنشيف وعضلات صافية", 
            "calories": 2400, "protein": 160, "carbs": 250, "fats": 70,
            "diet_plan": "وجبة 1: 4 بيضات مسلوقين + رغيف بلدي + سلطة\nوجبة 2: 150 جرام صدور فراخ + طبق أرز مصري كبير\nوجبة 3: علبة تونة مصفاة + سلطة خضراء\nوجبة 4: 150 جرام جبنة قريش + حفنة سوداني"
        },
        "محمد": {
            "weight": 70, "height": 170, "age": 22, "goal": "تضخيم عضلي وزيادة وزن", 
            "calories": 3000, "protein": 170, "carbs": 380, "fats": 80,
            "diet_plan": "وجبة 1: كوب شوفان + حليب + موز + معلقة عسل\nوجبة 2: 200 جرام لحم مفروم + مكرونة\nوجبة 3: 150 جرام صدور فراخ + بطاطس مسلوقة\nوجبة 4: 5 بيضات + خبز أبيض"
        }
    }

# -----------------------------------------------------------------
# القائمة الجانبية (Navigation)
# -----------------------------------------------------------------
st.sidebar.title("🎮 لوحة التحكم والخيارات")
app_mode = st.sidebar.radio("اختر القسم المطلوب:", [
    "🌐 الشات العام (بدون تسجيل)", 
    "🔐 بروفايل المتدرب (تسجيل الدخول)", 
    "📊 حاسبة السعرات والماكروز السريعة",
    "➕ إنشاء حساب متدرب جديد"
])

# -----------------------------------------------------------------
# 1. الشات العام (متاح للكل بدون تسجيل)
# -----------------------------------------------------------------
if app_mode == "🌐 الشات العام (بدون تسجيل)":
    st.subheader("💬 اسأل الكوتش عن التغذية، المكملات، أو التمارين الرياضية")
    st.info("💡 هذا القسم متاح للجميع. اسأل عن فوائد الكرياتين، كيفية تمرين الصدر، أو أي استفسار عام.")
    
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
            try:
                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.public_messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")

# -----------------------------------------------------------------
# 2. بروفايل المتدرب (لوحة التحكم الشخصية)
# -----------------------------------------------------------------
elif app_mode == "🔐 بروفايل المتدرب (تسجيل الدخول)":
    st.subheader("👤 بوابة المتدربين المسجلين")
    
    username = st.text_input("أدخل اسمك المسجل للوصول لبروفايلك وجدولك:")
    
    if username:
        if username in st.session_state.users_db:
            user_data = st.session_state.users_db[username]
            st.success(f"أهلاً بيك يا بطل، {username}! تم استدعاء بروفايلك وبياناتك بنجاح.")
            
            # عرض بيانات المتدرب (Dashboard)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("الوزن الحالي", f"{user_data['weight']} كجم")
            col2.metric("السعرات اليومية", f"{user_data['calories']} سعرة")
            col3.metric("البروتين المستهدف", f"{user_data['protein']} جرام")
            col4.metric("الهدف الحالي", user_data['goal'])
            
            st.markdown("---")
            st.markdown("### 🥗 جدولك الغذائي المخصص:")
            st.info(user_data['diet_plan'])
            
            st.markdown("---")
            st.markdown("### 🤖 دردش مع كوتشك الخاص (الذي يعرف تفاصيلك تماماً):")
            
            chat_key = f"chat_{username}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = []

            for msg in st.session_state[chat_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_prompt = st.chat_input("اطلب تعديل، بديل لأكلة غير متوفرة، أو اسأل عن تمرينك...")
            if user_prompt:
                st.session_state[chat_key].append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                with st.chat_message("assistant"):
                    # حقن بيانات المتدرب في الـ Prompt الخلفي للذكاء الاصطناعي
                    contextual_prompt = f"""
                    بيانات المتدرب الحالي:
                    الاسم: {username}
                    الوزن: {user_data['weight']} كجم
                    الهدف: {user_data['goal']}
                    السعرات والماكروز: {user_data['calories']} سعرة، بروتين {user_data['protein']}ج، كارب {user_data['carbs']}ج.
                    الجدول الغذائي الحالي: {user_data['diet_plan']}
                    
                    سؤال أو طلب المتدرب: {user_prompt}
                    """
                    try:
                        response = model.generate_content(contextual_prompt)
                        st.markdown(response.text)
                        st.session_state[chat_key].append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"خطأ في جلب الرد: {e}")
        else:
            st.warning("⚠️ هذا الاسم غير مسجل في قاعدة البيانات. برجاء التأكد من الاسم أو الانتقال لقسم 'إنشاء حساب جديد'.")

# -----------------------------------------------------------------
# 3. حاسبة السعرات والماكروز السريعة
# -----------------------------------------------------------------
elif app_mode == "📊 حاسبة السعرات والماكروز السريعة":
    st.subheader("🧮 حاسبة السعرات والماكروز الدقيقة (بدون هلوسة)")
    st.write("أدخل بياناتك بدقة لتحساب معادلتك الرياضية وسعراتك المناسبة لهدفك فوراً:")
    
    col1, col2 = st.columns(2)
    with col1:
        w = st.number_input("الوزن (كجم):", min_value=30.0, max_value=200.0, value=75.0)
        h = st.number_input("الطول (سم):", min_value=100.0, max_value=230.0, value=175.0)
    with col2:
        age = st.number_input("العمر (بالسنوات):", min_value=12, max_value=80, value=25)
        activity = st.selectbox("مستوى النشاط الأسبوعي:", [
            "قليل الحركة (تمرن نادراً)", 
            "نشاط خفيف (تمرن 1-3 أيام أسبوعياً)", 
            "نشاط متوسط (تمرن 3-5 أيام أسبوعياً)", 
            "نشاط عالي (تمرن بقوة 6-7 أيام أسبوعياً)"
        ])

    goal_type = st.selectbox("هدفك الحالي:", ["تنشيف (خسارة الدهون)", "تضخيم (بناء العضلات)", "ثبات الوزن وصيانة القوام"])

    if st.button("احسب سعراتي الآن بدقة"):
        # المعادلة الرياضية العلمية الثابتة (Mifflin-St Jeor)
        bmr = (10 * w) + (6.25 * h) - (5 * age) + 5
        
        multiplier = 1.2
        if "خفيف" in activity: multiplier = 1.375
        elif "متوسط" in activity: multiplier = 1.55
        elif "عالي" in activity: multiplier = 1.725
        
        tdee = bmr * multiplier
        
        if "تنشيف" in goal_type:
            final_cals = tdee - 500
        elif "تضخيم" in goal_type:
            final_cals = tdee + 300
        else:
            final_cals = tdee
            
        protein = w * 2.2 # 2.2 جرام لكل كيلو من وزن الجسم
        fats = (final_cals * 0.25) / 9
        carbs = (final_cals - ((protein * 4) + (fats * 9))) / 4
        
        st.success(f"🔥 سعرات الثبات الخاصة بك (TDEE): **{int(tdee)} سعرة حرارية**")
        st.info(f"🎯 السعرات المطلوبة لهدفك ({goal_type}): **{int(final_cals)} سعرة حرارية**")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("البروتين اليومي", f"{int(protein)} جرام")
        col_m2.metric("الكربوهيدرات", f"{int(carbs)} جرام")
        col_m3.metric("الدهون الصحية", f"{int(fats)} جرام")

# -----------------------------------------------------------------
# 4. إنشاء حساب متدرب جديد
# -----------------------------------------------------------------
elif app_mode == "➕ إنشاء حساب متدرب جديد":
    st.subheader("📝 تسجيل بروفايل جديد للمتدرب")
    
    new_name = st.text_input("اختر اسمك أو كودك السري:")
    new_w = st.number_input("الوزن (كجم):", value=75.0, key="nw")
    new_h = st.number_input("الطول (سم):", value=175.0, key="nh")
    new_age = st.number_input("العمر:", value=24, key="nage")
    new_goal = st.selectbox("الهدف:", ["تنشيف وعضلات صافية", "تضخيم عضلي وزيادة وزن", "ثبات وصحة عامة"])
    
    if st.button("حفظ البروفايل وإنشاء الحساب"):
        if new_name:
            # حساب مبدئي للسيستم
            cals = 2500 if "تضخيم" in new_goal else 2200
            prot = int(new_w * 2.2)
            st.session_state.users_db[new_name] = {
                "weight": new_w, "height": new_h, "age": new_age, "goal": new_goal,
                "calories": cals, "protein": prot, "carbs": 250, "fats": 70,
                "diet_plan": f"وجبة 1: بيض وأوفات\nوجبة 2: أرز وفراخ\nوجبة 3: تونة وسلطة"
            }
            st.success(f"🎉 تم إنشاء الحساب بنجاح يا بطل ({new_name})! انتقل الآن لـ 'بروفايل المتدرب' وادخل باسمك لاستعراض جدولك.")
        else:
            st.error("برجاء كتابة الاسم أو الكود بشكل صحيح.")
