from better_profanity import profanity
from langchain.schema import AIMessage, HumanMessage
from langchain.schema import HumanMessage
import json

from dotenv import load_dotenv
load_dotenv()

# 사용자 정의 비속어 리스트 로드 함수 
def load_custom_profanity(): 
    """ 
    사용자 정의 비속어 리스트를 로드하여 better-profanity에 추가합니다. 
    """ 
    custom_words_path = r".\data\fword_list_KOR.txt"  # 비속어 리스트 파일 경로 
    try: 
        with open(custom_words_path, "r", encoding="utf-8") as f: 
            # 사용자 정의 비속어 리스트를 set으로 저장
            custom_words = set(line.strip() for line in f.readlines()) 
        profanity.add_censor_words(custom_words)  # 사용자 정의 비속어 추가 
        return custom_words  # 추가: 비속어 리스트 반환
    except FileNotFoundError: 
        print(f"비속어 리스트 파일이 존재하지 않습니다: {custom_words_path}") 
        return set()  # 추가: 비속어 리스트가 없을 경우 빈 set 반환

# 비속어 감지 함수
def is_inappropriate_message(message):
    """ 
    better-profanity와 사용자 정의 리스트를 사용해 비속어를 감지하는 함수. 
    """ 
    custom_profanity_set = load_custom_profanity()  # 사용자 정의 비속어 리스트 로드 
    
    # 메시지를 단어 단위로 나누어 비속어 감지
    words = message.split()
    for word in words:
        if word in custom_profanity_set:  # 사용자 정의 비속어 리스트 확인
            return True
    return profanity.contains_profanity(message)  # better-profanity 확인

# 히스토리를 JSON 직렬화 가능하게 변환
def serialize_history(history):
    serialized = []
    for message in history:
        if isinstance(message, HumanMessage):
            serialized.append({"type": "human", "content": message.content})
        elif isinstance(message, AIMessage):
            serialized.append({"type": "ai", "content": message.content})
        else:
            serialized.append({"type": "unknown", "content": str(message)})
    return serialized

# JSON 데이터를 히스토리로 역변환
def deserialize_history(serialized_history):
    history = []
    for message in serialized_history:
        if message["type"] == "human":
            history.append(HumanMessage(content=message["content"]))
        elif message["type"] == "ai":
            history.append(AIMessage(content=message["content"]))
    return history

# 세션 선택
def select_session(conversations):
    if not conversations:
        print("저장된 대화 세션이 없습니다. 새 세션이 시작됩니다.")
        return None

    print("=== 기존 대화 세션 목록 ===")
    for idx, session in enumerate(conversations):
        print(f"{idx + 1}. {session['title']} ({session['date']})")

    while True:
        choice = input(f"세션 번호를 선택하세요 (1-{len(conversations)}) 또는 'new'를 입력하여 새 세션 시작: ").strip()
        if choice == "new":
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(conversations):
                return conversations[idx]
        except ValueError:
            pass
        print("잘못된 입력입니다. 다시 시도하세요.")

# 사이드바 출력 함수
def display_sidebar(conversations):
    """
    대화 목록을 사이드바 형태로 출력합니다.
    """
    print("=== 대화 히스토리 ===")
    for idx, convo in enumerate(conversations):
        print(f"{idx + 1}. {convo['title']} ({convo['date']})")

# 대화 기록 불러오기 함수
def load_conversations_from_file(filename="conversation_log.json"):
    """
    대화 기록을 파일에서 불러옵니다.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("sessions", [])
    except FileNotFoundError:
        print(f"{filename} 파일이 존재하지 않습니다.")
        return []