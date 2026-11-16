import streamlit as st

st.set_page_config(page_title="한국 금융 첫걸음", page_icon="🏦", layout="centered")

PASSWORD = "pnumis"

# ---------------------------------------------------------------
# 0. 언어 선택 (한국어 / English)
# ---------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "한국어"


def L(ko, en):
    """현재 언어에 맞는 문장을 돌려준다."""
    return ko if st.session_state.lang == "한국어" else en


st.sidebar.radio("Language / 언어", ["한국어", "English"], key="lang")

# ---------------------------------------------------------------
# 1. 비밀번호
# ---------------------------------------------------------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏦 " + L("한국 금융 첫걸음", "First Steps in Korean Banking"))
    pw = st.text_input(L("비밀번호를 입력하세요", "Enter the password"), type="password")
    if pw == PASSWORD:
        st.session_state.auth = True
        st.rerun()
    elif pw:
        st.error(L("비밀번호가 올바르지 않습니다.", "Wrong password."))
    st.stop()

# ---------------------------------------------------------------
# 2. 질문 목록: (id, 질문 ko, 질문 en, [(값, 보기 ko, 보기 en), ...])
# ---------------------------------------------------------------
QUESTIONS = [
    ("stay", "한국에 온 지 얼마나 되었나요?", "How long have you been in Korea?", [
        ("before", "아직 입국 전이에요", "I haven't arrived yet"),
        ("short", "3개월 미만", "Less than 3 months"),
        ("long", "3개월 이상", "3 months or more"),
    ]),
    ("arc", "외국인등록증이 있나요?", "Do you have a Residence Card (ARC)?", [
        ("yes", "네, 받았어요", "Yes, I have it"),
        ("applied", "신청하고 기다리는 중이에요", "I applied and am waiting"),
        ("no", "아직 신청하지 않았어요", "Not yet applied"),
    ]),
    ("phone", "본인 이름으로 개통한 한국 휴대폰 번호가 있나요?",
     "Do you have a Korean mobile number registered in your own name?", [
        ("yes", "네", "Yes"),
        ("no", "아니요 (없거나 다른 사람 명의)", "No (none, or under someone else's name)"),
    ]),
    ("account", "한국 은행 계좌가 있나요?", "Do you have a Korean bank account?", [
        ("none", "없어요", "No"),
        ("limited", "있는데 이체 한도가 낮게 제한되어 있어요", "Yes, but with a low transfer limit"),
        ("full", "있고 한도 제한도 풀었어요", "Yes, and the limit has been lifted"),
    ]),
    ("card", "한국에서 발급받은 체크카드가 있나요?", "Do you have a Korean debit (check) card?", [
        ("yes", "네", "Yes"),
        ("no", "아니요", "No"),
    ]),
    ("app", "은행 앱(모바일뱅킹)으로 이체할 수 있나요?",
     "Can you make transfers with a bank app (mobile banking)?", [
        ("yes", "네, 쓰고 있어요", "Yes, I use it"),
        ("no", "아니요", "No"),
    ]),
    ("remit", "본국과 돈을 주고받을 일이 있나요?", "Do you send or receive money from your home country?", [
        ("receive", "본국에서 생활비·학비를 받아요", "I receive living costs or tuition from home"),
        ("send", "한국에서 본국으로 보내기도 해요", "I also send money home from Korea"),
        ("none", "거의 없어요", "Rarely"),
    ]),
    ("income", "한국에서 받는 돈(아르바이트 급여, 장학금)이 있나요?",
     "Do you get paid in Korea (part-time wages, scholarship)?", [
        ("yes", "네, 있거나 곧 받을 예정이에요", "Yes, or I will soon"),
        ("no", "아니요", "No"),
    ]),
    ("korean", "은행 창구에서 한국어로 대화하는 것이 편한가요?",
     "Are you comfortable speaking Korean at a bank counter?", [
        ("low", "어려워요", "It is difficult"),
        ("mid", "간단한 대화는 가능해요", "Simple conversation is fine"),
        ("high", "편해요", "I am comfortable"),
    ]),
]

# ---------------------------------------------------------------
# 3. 준비 단계 6개: (id, 이름 ko, 이름 en, 방법 ko, 방법 en)
# ---------------------------------------------------------------
STEPS = [
    ("arc", "외국인등록증 받기", "Get your Residence Card",
     "입국 후 출입국·외국인관서에 방문 예약을 하고 신청하세요. 학교 국제처에서 단체 신청을 도와주는 경우도 많습니다. "
     "등록증이 나오기 전에는 여권만으로 계좌를 만들 수 있는지가 은행과 지점에 따라 다릅니다.",
     "After arrival, book a visit at the immigration office and apply. Many university international offices "
     "help with group applications. Before the card is issued, whether you can open an account with a passport "
     "alone depends on the bank and branch."),
    ("phone", "본인 명의 휴대폰 개통하기", "Get a phone number in your own name",
     "은행 앱의 본인 인증은 본인 명의 휴대폰으로 합니다. 개통할 때 이름을 외국인등록증과 "
     "똑같이(띄어쓰기, 미들네임 포함) 등록해야 인증이 막히지 않습니다.",
     "Bank apps verify your identity through a phone in your own name. Register your name exactly as it appears "
     "on your Residence Card (spacing and middle name included), or verification may fail."),
    ("account", "입출금 계좌 만들기", "Open a bank account",
     "외국인등록증, 여권, 재학증명서를 가지고 학교 근처 지점을 방문하세요. "
     "요구 서류는 은행마다 조금씩 다르니 방문 전에 전화나 홈페이지로 확인하면 헛걸음을 줄일 수 있습니다.",
     "Visit a branch near campus with your Residence Card, passport and certificate of enrollment. "
     "Required documents differ slightly by bank, so check by phone or website first."),
    ("limit", "이체 한도 제한 풀기", "Lift the transfer limit",
     "새 계좌는 보통 하루 이체 금액이 낮게 제한된 '한도제한계좌'로 시작합니다. "
     "재학증명서, 장학금 증서, 급여 명세처럼 계좌를 쓰는 목적을 보여 주는 서류를 내면 풀 수 있습니다.",
     "New accounts usually start as 'limited accounts' with a low daily transfer cap. You can lift it by "
     "submitting papers that show why you use the account, such as enrollment, scholarship or payslip documents."),
    ("card", "체크카드 만들기", "Get a debit card",
     "계좌를 만들 때 함께 신청하면 한 번에 끝납니다. 교통카드 기능을 넣으면 버스와 지하철에서도 쓸 수 있습니다.",
     "Apply when you open the account to finish in one visit. Add the transit function to use it on buses "
     "and subways."),
    ("app", "모바일뱅킹 등록하기", "Set up mobile banking",
     "은행 앱을 설치하고 창구에서 모바일뱅킹 가입을 함께 요청하세요. "
     "영어 화면을 지원하는 앱도 있으니 은행을 고를 때 확인해 보세요.",
     "Install the bank's app and ask the teller to register you for mobile banking. "
     "Some apps offer an English interface, so check when choosing a bank."),
]

# 다음에 할 단계에 따라 정해지는 유형 5가지
TYPES = {
    "arc": ("🛬", "도착 준비형", "Just Landed",
            "지금은 금융 생활의 출발선입니다. 외국인등록증이 거의 모든 금융 서비스의 열쇠입니다.",
            "You are at the starting line. The Residence Card is the key to almost every financial service."),
    "phone": ("📱", "계좌 개설 준비형", "Account Starter",
              "신분증은 준비됐습니다. 휴대폰과 계좌만 만들면 일상 결제가 해결됩니다.",
              "Your ID is ready. A phone number and an account will cover everyday payments."),
    "account": ("📱", "계좌 개설 준비형", "Account Starter",
                "신분증은 준비됐습니다. 휴대폰과 계좌만 만들면 일상 결제가 해결됩니다.",
                "Your ID is ready. A phone number and an account will cover everyday payments."),
    "limit": ("🧩", "기본 세팅형", "Basic Setup",
              "계좌는 있지만 아직 제약이 남아 있습니다. 한도와 카드를 정리하면 불편이 크게 줄어듭니다.",
              "You have an account but some limits remain. Sorting out the limit and card removes most hassles."),
    "card": ("🧩", "기본 세팅형", "Basic Setup",
             "계좌는 있지만 아직 제약이 남아 있습니다. 한도와 카드를 정리하면 불편이 크게 줄어듭니다.",
             "You have an account but some limits remain. Sorting out the limit and card removes most hassles."),
    "app": ("📲", "모바일 전환형", "Going Mobile",
            "기본은 다 갖췄습니다. 은행 앱만 쓰기 시작하면 창구에 갈 일이 거의 없어집니다.",
            "The basics are done. Once you use the bank app you will rarely need to visit a branch."),
    "done": ("🎓", "금융 독립형", "Finance Pro",
             "한국 금융 생활의 기본을 모두 갖췄습니다. 이제 수수료를 줄이고 안전하게 쓰는 단계입니다.",
             "You have all the basics. Now it is about cutting fees and staying safe."),
}

# ---------------------------------------------------------------
# 4. 화면 진행 상태
# ---------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

st.title("🏦 " + L("한국 금융 첫걸음", "First Steps in Korean Banking"))
st.caption(L("외국인 유학생을 위한 금융 준비 진단", "A banking readiness check for international students"))

total = len(QUESTIONS)
step = st.session_state.step

# ---------------------------------------------------------------
# 5. 질문 화면
# ---------------------------------------------------------------
if step < total:
    qid, q_ko, q_en, options = QUESTIONS[step]
    st.progress(step / total, text=L(f"질문 {step + 1} / {total}", f"Question {step + 1} of {total}"))

    with st.chat_message("assistant"):
        st.markdown("**" + L(q_ko, q_en) + "**")

    values = [o[0] for o in options]
    labels = {o[0]: L(o[1], o[2]) for o in options}
    saved = st.session_state.answers.get(qid)
    choice = st.radio(
        L("답을 골라 주세요", "Choose your answer"),
        values,
        index=values.index(saved) if saved in values else 0,
        format_func=lambda v: labels[v],
        key=f"q_{qid}",
    )

    left, right = st.columns(2)
    if left.button(L("← 이전", "← Back"), disabled=(step == 0), use_container_width=True):
        st.session_state.answers[qid] = choice
        st.session_state.step -= 1
        st.rerun()
    next_label = L("결과 보기", "See result") if step == total - 1 else L("다음 →", "Next →")
    if right.button(next_label, type="primary", use_container_width=True):
        st.session_state.answers[qid] = choice
        st.session_state.step += 1
        st.rerun()

# ---------------------------------------------------------------
# 6. 결과 화면
# ---------------------------------------------------------------
else:
    a = st.session_state.answers

    # 단계별 완료 여부
    done = {
        "arc": a["arc"] == "yes",
        "phone": a["phone"] == "yes",
        "account": a["account"] != "none",
        "limit": a["account"] == "full",
        "card": a["card"] == "yes",
        "app": a["app"] == "yes",
    }
    done_count = sum(done.values())
    next_step = next((s[0] for s in STEPS if not done[s[0]]), "done")
    icon, t_ko, t_en, d_ko, d_en = TYPES[next_step]

    # (1) 유형 카드
    st.subheader(L("진단 결과", "Your result"))
    with st.container(border=True):
        st.markdown(f"## {icon} {L(t_ko, t_en)}")
        st.write(L(d_ko, d_en))
        st.progress(done_count / len(STEPS),
                    text=L(f"금융 준비도 {done_count} / {len(STEPS)} 단계 완료",
                           f"Readiness: {done_count} of {len(STEPS)} steps done"))

    # (2) 단계별 체크리스트
    st.subheader(L("나의 준비 단계", "Your checklist"))
    for sid, s_ko, s_en, h_ko, h_en in STEPS:
        if done[sid]:
            st.markdown("✅ " + L(s_ko, s_en))
        else:
            is_next = sid == next_step
            title = ("👉 " if is_next else "⬜ ") + L(s_ko, s_en)
            if is_next:
                title += L("  (지금 할 일)", "  (do this next)")
            with st.expander(title, expanded=is_next):
                st.write(L(h_ko, h_en))

    # (3) 응답에 따른 맞춤 안내
    st.subheader(L("나에게 맞는 안내", "Tips for you"))
    tips = []
    if a["stay"] == "before":
        tips.append(L(
            "입국 직후에는 계좌가 없으니, 첫 몇 주 동안 쓸 현금이나 해외 결제가 되는 카드를 준비해 오세요.",
            "You will not have an account right after arrival, so bring cash or a card that works abroad "
            "for the first few weeks."))
    if a["arc"] == "applied":
        tips.append(L(
            "등록증을 기다리는 동안 재학증명서를 미리 발급받고, 방문할 은행 지점을 정해 두세요.",
            "While waiting for the card, get your certificate of enrollment and decide which branch to visit."))
    if a["remit"] == "receive":
        tips.append(L(
            "본국에서 돈을 받으려면 은행 영문명, SWIFT 코드, 계좌번호, 영문 이름을 가족에게 알려 주세요. "
            "받는 쪽에서도 수수료가 붙을 수 있습니다.",
            "To receive money from home, give your family the bank's English name, SWIFT code, account number "
            "and your name in English. A receiving fee may apply."))
    if a["remit"] == "send":
        tips.append(L(
            "외국인의 해외송금은 한도와 필요 서류가 내국인과 다르고, 거래 은행을 한 곳 지정해야 할 수 있습니다. "
            "보내기 전에 은행에 본인 체류자격 기준의 한도를 확인하세요.",
            "For foreign residents, remittance limits and documents differ from those for Korean nationals, "
            "and you may need to designate one bank. Ask the bank about the limit for your visa status first."))
    if a["income"] == "yes":
        tips.append(L(
            "급여나 장학금을 받을 계좌는 한도 제한을 먼저 풀어 두세요. "
            "유학생이 아르바이트를 하려면 시간제 취업 허가가 필요하니 학교 국제처에 먼저 문의하세요.",
            "Lift the transfer limit on the account that receives wages or scholarships. International students "
            "need a part-time work permit, so ask your international office first."))
    if a["korean"] == "low":
        tips.append(L(
            "외국인 전용 창구나 외국어 상담이 있는 지점을 고르면 훨씬 수월합니다. "
            "학교 국제처나 버디 프로그램에 동행을 부탁하는 것도 방법입니다.",
            "Choose a branch with a foreigner desk or foreign-language service. You can also ask the "
            "international office or a buddy program to come with you."))
    tips.append(L(
        "통장, 카드, 비밀번호를 다른 사람에게 빌려주거나 파는 것은 불법입니다. "
        "귀국할 때는 계좌를 직접 해지하세요.",
        "Lending or selling your bankbook, card or PIN is illegal. Close your account yourself before "
        "leaving Korea."))
    for tip in tips:
        st.info(tip)

    st.caption(L(
        "이 결과는 일반적인 안내입니다. 필요 서류와 한도는 은행, 지점, 체류자격에 따라 다르므로 "
        "방문 전에 해당 은행에 확인하세요.",
        "This result is general guidance. Documents and limits vary by bank, branch and visa status, "
        "so confirm with the bank before visiting."))

    if st.button(L("처음부터 다시 하기", "Start over"), use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
