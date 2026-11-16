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
# 2. 질문 목록
#    (id, 질문 ko, 질문 en, [(값, 보기 ko, 보기 en), ...], 표시 조건)
#    표시 조건: 앞선 답변을 보고 이 질문을 보여 줄지 정하는 함수
# ---------------------------------------------------------------
def always(a):
    return True


def no_account(a):
    return a.get("account") == "none"


def has_account(a):
    return a.get("account") in ("limited", "full")


QUESTIONS = [
    ("stay", "한국에 온 지 얼마나 되었나요?", "How long have you been in Korea?", [
        ("before", "아직 입국 전이에요", "I haven't arrived yet"),
        ("short", "3개월 미만", "Less than 3 months"),
        ("long", "3개월 이상", "3 months or more"),
    ], always),
    ("arc", "외국인등록증이 있나요?", "Do you have a Residence Card (ARC)?", [
        ("yes", "네, 받았어요", "Yes, I have it"),
        ("applied", "신청하고 기다리는 중이에요", "I applied and am waiting"),
        ("no", "아직 신청하지 않았어요", "Not yet applied"),
    ], always),
    ("phone", "본인 이름으로 개통한 한국 휴대폰 번호가 있나요?",
     "Do you have a Korean mobile number registered in your own name?", [
        ("yes", "네", "Yes"),
        ("no", "아니요 (없거나 다른 사람 명의)", "No (none, or under someone else's name)"),
    ], always),
    ("account", "한국 은행 계좌가 있나요?", "Do you have a Korean bank account?", [
        ("none", "없어요", "No"),
        ("limited", "있는데 이체 한도가 낮게 제한되어 있어요", "Yes, but with a low transfer limit"),
        ("full", "있고 한도 제한도 풀었어요", "Yes, and the limit has been lifted"),
    ], always),
    ("open_way", "계좌를 어떤 방법으로 만들고 싶나요?", "How would you like to open your account?", [
        ("branch", "은행 지점에 직접 가서", "In person at a branch"),
        ("online", "가능하면 앱으로 (지점 방문 없이)", "By app if possible (no branch visit)"),
        ("unsure", "잘 모르겠어요", "Not sure"),
    ], no_account),
    ("bank_pick", "은행을 고를 때 가장 중요한 것은 무엇인가요?", "What matters most when you pick a bank?", [
        ("near", "학교나 집에서 가까운 지점", "A branch close to campus or home"),
        ("lang", "외국어 지원 (창구, 앱)", "Foreign-language support (counter, app)"),
        ("app", "쓰기 편한 앱", "An easy-to-use app"),
    ], no_account),
    ("card", "한국에서 발급받은 체크카드가 있나요?", "Do you have a Korean debit (check) card?", [
        ("yes", "네", "Yes"),
        ("no", "아니요", "No"),
    ], has_account),
    ("app", "은행 앱(모바일뱅킹)으로 이체할 수 있나요?",
     "Can you make transfers with a bank app (mobile banking)?", [
        ("yes", "네, 쓰고 있어요", "Yes, I use it"),
        ("no", "아니요", "No"),
    ], has_account),
    ("transit", "버스나 지하철을 탈 때 무엇으로 결제하나요?", "How do you pay for buses and subways?", [
        ("debit", "체크카드의 교통카드 기능", "Transit function on my debit card"),
        ("prepaid", "충전식 교통카드", "A rechargeable transit card"),
        ("none", "현금을 쓰거나 아직 없어요", "Cash, or nothing yet"),
    ], always),
    ("remit", "본국과 돈을 주고받을 일이 있나요?", "Do you send or receive money from your home country?", [
        ("receive", "본국에서 생활비·학비를 받아요", "I receive living costs or tuition from home"),
        ("send", "한국에서 본국으로 보내기도 해요", "I also send money home from Korea"),
        ("none", "거의 없어요", "Rarely"),
    ], always),
    ("income", "한국에서 받는 돈(아르바이트 급여, 장학금)이 있나요?",
     "Do you get paid in Korea (part-time wages, scholarship)?", [
        ("yes", "네, 있거나 곧 받을 예정이에요", "Yes, or I will soon"),
        ("no", "아니요", "No"),
    ], always),
    ("benefit", "은행이나 카드를 고를 때 가장 끌리는 혜택은 무엇인가요?",
     "Which benefit matters most when you choose a bank or card?", [
        ("fee", "이체·ATM 수수료 면제", "No transfer or ATM fees"),
        ("cashback", "카페·편의점·배달 할인이나 캐시백", "Discounts or cashback at cafes, stores, delivery"),
        ("transit", "교통비·통신비 할인", "Transit or phone bill discounts"),
        ("fx", "환율 우대와 저렴한 해외송금", "Better exchange rates and cheap remittance"),
    ], always),
    ("korean", "은행 창구에서 한국어로 대화하는 것이 편한가요?",
     "Are you comfortable speaking Korean at a bank counter?", [
        ("low", "어려워요", "It is difficult"),
        ("mid", "간단한 대화는 가능해요", "Simple conversation is fine"),
        ("high", "편해요", "I am comfortable"),
    ], always),
]

# ---------------------------------------------------------------
# 3. 준비 단계 7개: (id, 이름 ko, 이름 en, 방법 ko, 방법 en)
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
     "계좌를 만들 때 함께 신청하면 한 번에 끝납니다. 이미 계좌가 있다면 신분증을 가지고 지점에서 신청하세요.",
     "Apply when you open the account to finish in one visit. If you already have an account, apply at a "
     "branch with your ID."),
    ("transit", "교통카드 준비하기", "Get a transit card",
     "충전식 교통카드는 편의점에서 바로 사서 현금으로 충전할 수 있어 계좌가 없어도 쓸 수 있습니다. "
     "체크카드에 교통카드 기능을 넣으면 충전 없이 탈 수 있는데, 외국인 발급 조건은 은행마다 다릅니다.",
     "You can buy a rechargeable transit card at any convenience store and top it up with cash, even without "
     "an account. A debit card with a transit function needs no top-up, but eligibility for foreigners "
     "differs by bank."),
    ("app", "모바일뱅킹 등록하기", "Set up mobile banking",
     "은행 앱을 설치하고 창구에서 모바일뱅킹 가입을 함께 요청하세요. "
     "영어 화면을 지원하는 앱도 있으니 은행을 고를 때 확인해 보세요.",
     "Install the bank's app and ask the teller to register you for mobile banking. "
     "Some apps offer an English interface, so check when choosing a bank."),
]

# ---------------------------------------------------------------
# 4. 유형 = 준비 단계(5가지) x 이용 성향(3가지) = 15가지
# ---------------------------------------------------------------
# 준비 단계: 아직 끝내지 못한 첫 번째 단계가 무엇인지로 정한다
STAGE_OF_STEP = {
    "arc": "S1", "phone": "S2", "account": "S2",
    "limit": "S3", "card": "S3", "transit": "S4", "app": "S4", "done": "S5",
}
STAGES = {
    "S1": ("🛬", "도착 준비", "Just Landed",
           "지금은 금융 생활의 출발선입니다. 외국인등록증이 거의 모든 금융 서비스의 열쇠입니다.",
           "You are at the starting line. The Residence Card is the key to almost every financial service."),
    "S2": ("📱", "계좌 개설 준비", "Account Starter",
           "신분증은 준비됐습니다. 휴대폰과 계좌만 만들면 일상 결제가 해결됩니다.",
           "Your ID is ready. A phone number and an account will cover everyday payments."),
    "S3": ("🧩", "기본 세팅", "Basic Setup",
           "계좌는 있지만 아직 제약이 남아 있습니다. 한도와 카드를 정리하면 불편이 크게 줄어듭니다.",
           "You have an account but some limits remain. Sorting out the limit and card removes most hassles."),
    "S4": ("📲", "편의 확장", "Going Convenient",
           "기본은 다 갖췄습니다. 교통카드와 은행 앱까지 챙기면 창구에 갈 일이 거의 없어집니다.",
           "The basics are done. With a transit card and the bank app you will rarely need a branch."),
    "S5": ("🎓", "금융 독립", "Finance Pro",
           "한국 금융 생활의 기본을 모두 갖췄습니다. 이제 수수료를 줄이고 혜택을 챙기는 단계입니다.",
           "You have all the basics. Now it is about cutting fees and collecting benefits."),
}
# 이용 성향: 돈이 주로 어떻게 움직이는지로 정한다
STYLES = {
    "R": ("💸", "송금형", "Remitter",
          "본국과 돈을 주고받는 일이 금융 생활의 중심입니다. 은행을 고를 때 송금 수수료와 환율 우대를 먼저 비교하세요.",
          "Moving money to and from home is central for you. Compare remittance fees and exchange-rate "
          "discounts first when choosing a bank."),
    "I": ("💼", "수입형", "Earner",
          "한국에서 받는 급여나 장학금이 중심입니다. 돈을 받는 계좌의 한도를 풀고, 급여 이체 혜택이 있는지 확인하세요.",
          "Wages or scholarships earned in Korea are central for you. Lift the limit on the receiving account "
          "and check for salary-transfer benefits."),
    "D": ("🛒", "생활형", "Daily Spender",
          "일상 결제가 중심입니다. 자주 쓰는 곳에서 혜택이 있는 체크카드 하나를 잘 고르는 것이 가장 중요합니다.",
          "Everyday payments are central for you. Picking one debit card with benefits where you spend most "
          "matters the most."),
}

# 선호 혜택별 안내
BENEFIT_TIPS = {
    "fee": ("수수료 면제를 원한다면: 학생·외국인 전용 계좌나 급여 이체 조건으로 이체·ATM 수수료가 면제되는지 물어보세요. "
            "다른 은행 ATM은 수수료가 붙는 경우가 많습니다.",
            "For fee waivers: ask whether a student or foreigner account, or a salary-transfer condition, waives "
            "transfer and ATM fees. Other banks' ATMs often charge a fee."),
    "cashback": ("할인·캐시백을 원한다면: 내가 자주 쓰는 곳(카페, 편의점, 배달)이 혜택 업종인지, "
                 "지난달 사용 금액 조건이 있는지 확인하고 체크카드를 고르세요.",
                 "For discounts or cashback: check that the places you use most (cafes, stores, delivery) are "
                 "covered and whether a minimum monthly spend applies before choosing a debit card."),
    "transit": ("교통·통신 할인을 원한다면: 교통카드 기능이 있고 대중교통이나 통신요금 할인이 붙은 체크카드를 찾아보세요. "
                "대중교통을 자주 타면 정부·지자체 교통비 환급 제도도 확인해 볼 만합니다.",
                "For transit or phone discounts: look for a debit card with a transit function and transit or "
                "phone-bill discounts. Frequent riders should also check government transit refund programs."),
    "fx": ("환율 우대를 원한다면: 은행마다 환율 우대율과 송금 수수료가 다릅니다. "
           "외국인 전용 송금 서비스가 있는지 함께 비교하세요.",
           "For better exchange rates: discount rates and remittance fees differ by bank. "
           "Also compare whether a remittance service for foreigners is offered."),
}

# ---------------------------------------------------------------
# 5. 화면 진행 상태
# ---------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

st.title("🏦 " + L("한국 금융 첫걸음", "First Steps in Korean Banking"))
st.caption(L("외국인 유학생을 위한 금융 준비 진단", "A banking readiness check for international students"))

a = st.session_state.answers
visible = [q for q in QUESTIONS if q[4](a)]   # 지금까지의 답변으로 보여 줄 질문만 고른다
# 계좌가 있든 없든 추가 질문이 2개씩 붙으므로 전체 질문 수는 항상 같다
total = sum(1 for q in QUESTIONS if q[4] is always) + 2
step = st.session_state.step

# ---------------------------------------------------------------
# 6. 질문 화면
# ---------------------------------------------------------------
if step < len(visible):
    qid, q_ko, q_en, options, _ = visible[step]
    st.progress(step / total, text=L(f"질문 {step + 1} / {total}", f"Question {step + 1} of {total}"))

    with st.chat_message("assistant"):
        st.markdown("**" + L(q_ko, q_en) + "**")

    values = [o[0] for o in options]
    labels = {o[0]: L(o[1], o[2]) for o in options}
    saved = a.get(qid)
    choice = st.radio(
        L("답을 골라 주세요", "Choose your answer"),
        values,
        index=values.index(saved) if saved in values else 0,
        format_func=lambda v: labels[v],
        key=f"q_{qid}",
    )

    left, right = st.columns(2)
    if left.button(L("← 이전", "← Back"), disabled=(step == 0), use_container_width=True):
        a[qid] = choice
        st.session_state.step -= 1
        st.rerun()
    next_label = L("결과 보기", "See result") if step == total - 1 else L("다음 →", "Next →")
    if right.button(next_label, type="primary", use_container_width=True):
        a[qid] = choice
        st.session_state.step += 1
        st.rerun()

# ---------------------------------------------------------------
# 7. 결과 화면
# ---------------------------------------------------------------
else:
    has_acc = a["account"] != "none"

    # (가) 단계별 완료 여부. 계좌가 없으면 한도·카드·앱은 자동으로 미완료
    done = {
        "arc": a["arc"] == "yes",
        "phone": a["phone"] == "yes",
        "account": has_acc,
        "limit": a["account"] == "full",
        "card": has_acc and a.get("card") == "yes",
        "transit": a["transit"] != "none",
        "app": has_acc and a.get("app") == "yes",
    }
    done_count = sum(done.values())
    next_step = next((s[0] for s in STEPS if not done[s[0]]), "done")
    stage = STAGE_OF_STEP[next_step]

    # (나) 이용 성향
    if a["remit"] == "send":
        style = "R"
    elif a["income"] == "yes":
        style = "I"
    elif a["remit"] == "receive":
        style = "R"
    else:
        style = "D"

    s_icon, s_ko, s_en, sd_ko, sd_en = STAGES[stage]
    y_icon, y_ko, y_en, yd_ko, yd_en = STYLES[style]

    # (1) 유형 카드
    st.subheader(L("진단 결과", "Your result"))
    with st.container(border=True):
        st.caption(L(f"유형 코드 {stage}-{style}", f"Type code {stage}-{style}"))
        st.markdown(f"## {s_icon}{y_icon} {L(s_ko + ' ' + y_ko, s_en + ' · ' + y_en)}")
        st.markdown("**" + L("준비 단계: ", "Stage: ") + L(s_ko, s_en) + "**")
        st.write(L(sd_ko, sd_en))
        st.markdown("**" + L("이용 성향: ", "Style: ") + L(y_ko, y_en) + "**")
        st.write(L(yd_ko, yd_en))
        st.progress(done_count / len(STEPS),
                    text=L(f"금융 준비도 {done_count} / {len(STEPS)} 단계 완료",
                           f"Readiness: {done_count} of {len(STEPS)} steps done"))

    # (2) 단계별 체크리스트
    st.subheader(L("나의 준비 단계", "Your checklist"))
    for sid, st_ko, st_en, h_ko, h_en in STEPS:
        if done[sid]:
            st.markdown("✅ " + L(st_ko, st_en))
        else:
            is_next = sid == next_step
            title = ("👉 " if is_next else "⬜ ") + L(st_ko, st_en)
            if is_next:
                title += L("  (지금 할 일)", "  (do this next)")
            with st.expander(title, expanded=is_next):
                st.write(L(h_ko, h_en))

    # (3) 응답에 따른 맞춤 안내
    st.subheader(L("나에게 맞는 안내", "Tips for you"))
    tips = [L(*BENEFIT_TIPS[a["benefit"]])]
    if a["stay"] == "before":
        tips.append(L(
            "입국 직후에는 계좌가 없으니, 첫 몇 주 동안 쓸 현금이나 해외 결제가 되는 카드를 준비해 오세요.",
            "You will not have an account right after arrival, so bring cash or a card that works abroad "
            "for the first few weeks."))
    if a["arc"] == "applied":
        tips.append(L(
            "등록증을 기다리는 동안 재학증명서를 미리 발급받고, 방문할 은행 지점을 정해 두세요.",
            "While waiting for the card, get your certificate of enrollment and decide which branch to visit."))
    if a.get("open_way") == "online" and not has_acc:
        tips.append(L(
            "외국인등록증과 본인 명의 휴대폰이 있으면 앱으로 계좌를 만들 수 있는 은행도 있습니다. "
            "다만 은행마다 가능 여부가 다르고, 등록증이 없으면 지점 방문이 필요합니다.",
            "Some banks let you open an account by app if you have a Residence Card and a phone in your name. "
            "Availability differs by bank, and without the card a branch visit is needed."))
    if a.get("open_way") in ("branch", "unsure") and not has_acc:
        tips.append(L(
            "지점은 학교 안이나 학교 근처를 고르세요. 유학생 계좌 개설 경험이 많아 진행이 빠릅니다. "
            "평일 오후 4시 전에 가야 하고, 학기 초에는 대기가 깁니다.",
            "Choose a branch on or near campus. They handle many student accounts, so it goes faster. "
            "Go before 4 p.m. on a weekday, and expect long waits at the start of a semester."))
    if not has_acc and a.get("bank_pick") == "near":
        tips.append(L(
            "가까운 지점을 원한다면 학교 안이나 정문 근처에 지점이나 ATM이 있는 은행을 먼저 살펴보세요. "
            "등록금 납부나 장학금 수령 은행이 정해져 있는지도 국제처에 물어보세요.",
            "If you want a nearby branch, first look at banks with a branch or ATM on or next to campus. "
            "Also ask your international office whether tuition or scholarships go through a specific bank."))
    if not has_acc and a.get("bank_pick") == "lang":
        tips.append(L(
            "외국어 지원이 중요하다면 외국인 전용 창구가 있는 지점인지, 앱이 내 언어를 지원하는지 "
            "방문 전에 확인하세요. 같은 은행이어도 지점마다 다릅니다.",
            "If language support matters, check before visiting whether the branch has a foreigner desk and "
            "whether the app supports your language. It differs by branch even within one bank."))
    if not has_acc and a.get("bank_pick") == "app":
        tips.append(L(
            "앱 편의성이 중요하다면 외국인등록증으로 가입과 본인 인증이 되는지를 먼저 확인하세요. "
            "외국인은 일부 기능이 제한되는 앱도 있습니다.",
            "If app convenience matters, first check that sign-up and identity verification work with a "
            "Residence Card. Some apps restrict certain features for foreigners."))
    if a["transit"] == "prepaid" and has_acc:
        tips.append(L(
            "충전식 교통카드를 쓰고 있다면, 체크카드의 교통카드 기능으로 바꾸면 충전할 필요가 없어집니다.",
            "If you use a rechargeable transit card, switching to the transit function on a debit card "
            "removes the need to top up."))
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
            "유학생이 아르바이트를 하려면 시간제 취업 허가가 필요하니 학교 국제처에 먼저 문의하세요.",
            "International students need a part-time work permit, so ask your international office first."))
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
        "이 결과는 일반적인 안내입니다. 필요 서류, 한도, 혜택은 은행, 지점, 체류자격에 따라 다르므로 "
        "방문 전에 해당 은행에 확인하세요.",
        "This result is general guidance. Documents, limits and benefits vary by bank, branch and visa status, "
        "so confirm with the bank before visiting."))

    if st.button(L("처음부터 다시 하기", "Start over"), use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
