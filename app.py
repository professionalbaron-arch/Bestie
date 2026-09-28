import streamlit as st

st.set_page_config(page_title="Trio Bestie Quiz 🚀", page_icon="🧸", layout="centered")

# Custom Dark Pink Styling
st.markdown("""
    <style>
    /* Dark Pink Theme Customization */
    .stApp { background-color: #FFF0F5; max-width: 800px; margin: 0 auto; }
    
    /* Main Title & Subtitle */
    .main-title { color: #FF1493; text-align: center; font-weight: 800; font-size: 32px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin-bottom: 10px; }
    .sub-title { color: #C71585; text-align: center; font-weight: 600; font-size: 18px; margin-bottom: 25px; }
    
    /* Quiz Cards */
    .quiz-card { background-color: #FFFFFF; padding: 18px; border-radius: 15px; box-shadow: 0 4px 12px rgba(255, 20, 147, 0.12); margin-bottom: 15px; border-left: 6px solid #FF1493; font-size: 18px; color: #C71585; font-weight: 700; }
    
    /* Radio Option Text Styling */
    div[class*="stRadio"] label { color: #FF1493 !important; font-weight: 600 !important; font-size: 16px !important; }
    
    /* Submit Button */
    div.stButton > button:first-child { background-color: #FF1493 !important; color: white !important; font-size: 18px !important; font-weight: bold !important; border-radius: 12px !important; border: none !important; padding: 10px 25px !important; width: 100% !important; box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3) !important; }
    div.stButton > button:first-child:hover { background-color: #C71585 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🧸 The Ultimate Trio Quiz: Besties Edition! ✨</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Welcome Ankita! Kanan aur Kartik ke saath tumhari dosti ka sach aaj saamne aayega! 😂🔥</div>", unsafe_allow_html=True)
st.markdown("---")

QUESTIONS = [
    {
        "q": "1. Hum teeno (Kanan, Kartik, Ankita) me se sabse pehle late-night gaming match ya phone call par kaun so jaata hai?",
        "opts": ["Kanan - Pro gamer, poori raat jaag sakta hai! 🎮", "Kartik - Thoda der tikta hai fir khraate lene lagta hai 😴", "Ankita - Pehle hi bolti hai 'mujhe neend aa rahi hai' 💤", "Sab ke sab ek sath so jaate hain 😂"],
        "ans": "Ankita - Pehle hi bolti hai 'mujhe neend aa rahi hai' 💤"
    },
    {
        "q": "2. College me agar class bunk karke kahin bahar ghoomne ka plan bane, toh mastermind kaun hota hai?",
        "opts": ["Kanan - Brain behind every plan 😎", "Kartik - Instigator jo sabko uksata hai 🔥", "Ankita - Pehle mana karti hai fir sabse pehle tayar ho jaati hai 🎒", "Hum teeno milkar hi chaos machate hain 💥"],
        "ans": "Hum teeno milkar hi chaos machate hain 💥"
    },
    {
        "q": "3. Squad gaming match (Free Fire / Mech Arena / Uncharted) me jab sabse tight situation hoti hai, toh clutch kaun marta hai aur sabse pehle knockout kaun hota hai?",
        "opts": ["Kanan Clutch God hai, baki sab revive maangte hain 🏆", "Kartik Rambo bane bina soche ghus jaata hai 💣", "Ankita peeche se support/medic banti hai 🩺", "Sabse pehle panic button daba kar bhaagne wale hum teeno hain 🏃‍♂️"],
        "ans": "Kanan Clutch God hai, baki sab revive maangte hain 🏆"
    },
    {
        "q": "4. Raat ke 3 baje agar kisi ko weird musibat me help chahiye ho, toh Kartik aur Kanan me se sabse pehle phone kaun uthayega?",
        "opts": ["Kanan - Hamesha ready for rescue 🦸‍♂️", "Kartik - Pehle 10 min roast karega fir aayega 🤣", "Dono ek sath phone uthaye bina nahi rahenge 📞", "Dono bolenge 'subah baat karte hain' 💤"],
        "ans": "Dono ek sath phone uthaye bina nahi rahenge 📞"
    },
    {
        "q": "5. Hum teeno me sabse zyada 'Drama Queen / Overthinker' kaun hai?",
        "opts": ["Kanan - Chill rehta hai par andar se overthinker 🤔", "Kartik - Full dramatic baatein karta hai 🎭", "Ankita - Choti baat pe 10 page ka essay soch leti hai 📝", "Teeno ke teeno pagal hain 😜"],
        "ans": "Teeno ke teeno pagal hain 😜"
    },
    {
        "q": "6. College Canteen me jab bill aata hai, toh sabse pehle kaun bolta hai 'Aaj tum de do, kal main doonga'?",
        "opts": ["Kanan - Sahi time pe wallet gayab kar leta hai 💸", "Kartik - Bolta hai 'bhai Google Pay nahi chal raha' 📲", "Ankita - chupchap khana khane me busy rehti hai 🍔", "Hum humesha divide kar lete hain (ya Kartik deta hai) 😂"],
        "ans": "Hum humesha divide kar lete hain (ya Kartik deta hai) 😂"
    },
    {
        "q": "7. Teeno me se sabse 'Secret Keeper' kaun hai jiske pet me baat pachti hai?",
        "opts": ["Kanan - Vault ki tarah locked 🔒", "Kartik - Depend karta hai kiska secret hai 🤫", "Ankita - 'Kisi ko batana mat' bolke leak kar deti hai 📢", "Teeno ke paas ek doosre ke saare kaand hain 💣"],
        "ans": "Teeno ke paas ek doosre ke saare kaand hain 💣"
    },
    {
        "q": "8. College exam ke ek din pehle, group chat par sabse zyada panic kaun karta hai?",
        "opts": ["Kanan - Silent killer, chupchap padh leta hai 📚", "Kartik - 'Bhai kuch nahi padha, pass kara do!' 😂", "Ankita - Important notes maangne ke liye spam karti hai 📄", "Teeno ek doosre ke bharose rehte hain 🤝"],
        "ans": "Teeno ek doosre ke bharose rehte hain 🤝"
    },
    {
        "q": "9. Agar hum teeno me fight ho jaye, toh sabse pehle 'Sorry' bolke patch-up kaun karwata hai?",
        "opts": ["Kanan - Maturity se mamla solve karta hai 😇", "Kartik - Meme bhej kar sab normal kar deta hai 📲", "Ankita - Ego side me karke baat kar leti hai 💕", "Koi nahi bolta, 2 ghante baad apne aap bakchodi shuru ho jaati hai 🔥"],
        "ans": "Koi nahi bolta, 2 ghante baad apne aap bakchodi shuru ho jaati hai 🔥"
    },
    {
        "q": "10. Hum teeno ke group ka sabse bada Reel/TikTok addict kaun hai jo din bhar Instagram me rehta hai?",
        "opts": ["Kanan - Video Editor hai toh Reels analyze karta hai 🎥", "Kartik - Din me 50 brain-rot memes bhejta hai 🤪", "Ankita - Continuous scrolling mode 📱", "Kartik aur Ankita dono milke DM bhar dete hain 📩"],
        "ans": "Kartik aur Ankita dono milke DM bhar dete hain 📩"
    },
    {
        "q": "11. Agar teeno kisi trip par jayein, toh sabse zyada photos & aesthetic clicks kisko chahiye hoti hain?",
        "opts": ["Ankita - Dynamic angles & aesthetic vibes 📸", "Kanan - Bas landmark ki ek pic leke free ho jata hai 🏛️", "Kartik - Weirdly pose karke photo khinchwata hai 🤪", "Ankita cameraman banati hai baki dono ko 目录"],
        "ans": "Ankita cameraman banati hai baki dono ko 目录"
    },
    {
        "q": "12. Teeno me sabse bada Foodie kaun hai jo hamesha 'Kuch khane chalein?' bolta rehta hai?",
        "opts": ["Kanan - Fast food specialist 🍕", "Kartik - Kuch bhi khila do, bas milna chahiye 🍔", "Ankita - Craving queen 🍟", "Teeno bas khane ke bahane milte hain ✨"],
        "ans": "Teeno bas khane ke bahane milte hain ✨"
    },
    {
        "q": "13. Kisi stranger ke saath arguing ya lafda ho jaye toh sabse pehle aage kaun aayega?",
        "opts": ["Kanan & Kartik - Brotherly squad ready for battle 🥊", "Ankita - Apni baaton se hi saamne wale ko harade 🗣️", "Teeno milkar full support me khade ho jayenge 🤝", "Peeth dikha ke bhaag jayenge 😂"],
        "ans": "Teeno milkar full support me khade ho jayenge 🤝"
    },
    {
        "q": "14. Hum teeno me se sabse zyada Savage / Roast karne wala member kaun hai?",
        "opts": ["Kanan - One-liner se bolti band 🤐", "Kartik - Non-stop roasting machine 🔥", "Ankita - Masoom ban kar sabse bada taana marti hai 😉", "Sab ek doosre ki tang kheenchte hain 24/7 😂"],
        "ans": "Sab ek doosre ki tang kheenchte hain 24/7 😂"
    },
    {
        "q": "15. Final Question: Ankita, kya tum Kanan aur Kartik ki bakwaas zindagi bhar jhelne ko tayar ho?",
        "opts": ["Haan, koi aur option bhi hai kya? 🙄", "Haan, thoda jhel lungi 💖", "Locked & Signed 🔒", "All of the above! 😄"],
        "ans": "All of the above! 😄"
    }
]

score = 0
with st.form("quiz_form"):
    for idx, item in enumerate(QUESTIONS):
        st.markdown(f'<div class="quiz-card">{item["q"]}</div>', unsafe_allow_html=True)
        user_choice = st.radio("Choose your answer:", item["opts"], key=idx, label_visibility="collapsed")
        if user_choice == item["ans"]:
            score += 1
        st.write("")
    submitted = st.form_submit_button("Submit & Reveal Results 🧸🎉")

if submitted:
    st.balloons()
    st.snow()
    st.markdown("---")
    st.success(f"🎉 Quiz Finished! Your Score: {score}/15 ✨")
    st.markdown("""
        <div style="text-align: center; padding: 25px; background-color: #FFFFFF; border-radius: 20px; border: 3px dashed #FF1493; box-shadow: 0 4px 15px rgba(255, 20, 147, 0.2);">
            <h2 style="color: #FF1493; font-weight: 800;">🧸 OFFICIAL TRIO VERDICT 🧸</h2>
            <p style="font-size: 19px; color: #C71585; font-weight: bold; line-height: 1.6;">
                Ankita, tumne Kanan aur Kartik ke saare mazaak aur questions pass kar liye!<br>
                The Three Musketeers / Besties for Life! ❤️🔥
            </p>
            <p style="font-size: 32px;">🧸🎈✨💖🎮</p>
        </div>
    """, unsafe_allow_html=True)
