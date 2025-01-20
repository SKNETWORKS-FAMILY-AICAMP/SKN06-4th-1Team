import os
from .file import load_json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnableLambda
from langchain.schema import HumanMessage
from operator import itemgetter
from textwrap import dedent
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 경로 설정
DIRECTORY_PATH = r".\data"
PERSIST_DIRECTORY = r".\data\vector_store\policy"
COLLECTION_NAME = "policy"
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
TOKENIZED_DATA_PATH = os.path.join(DIRECTORY_PATH, "policy_result.json")


# JSON 데이터 불러오기
data = load_json("./data/policy_result.json")

# Document 객체로 변환
documents = []
for policy_name, contents in data.items():
    merged_text = " ".join(contents)
    documents.append(
        Document(
            page_content=merged_text,
            metadata={"name": policy_name, "source": TOKENIZED_DATA_PATH},
        )
    )

# 임베딩 모델 초기화
embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

# Vector Store 생성/로드
if os.path.exists(PERSIST_DIRECTORY):
    print(f"기존 Vector Store를 {PERSIST_DIRECTORY}에서 로드합니다.")
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
    )
else:
    print(f"새로운 Vector Store를 {PERSIST_DIRECTORY}에 생성합니다.")
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )



# Retriever 설정 - 검색 설정
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 10,
        "lambda_mult": 0.2,
    },
)
print(f"vector store가 {PERSIST_DIRECTORY}에서 성공적으로 생성/로드되었습니다.")


class Chatting:
    """
    대화형 AI 채팅 클래스.

    GPT 모델을 사용하여 사용자와 대화를 수행하고, 대화 기록을 관리한다.
    """

    # db 검색 tool
    @tool
    def search_policy(query: str) -> list[Document]:
        """
        Vector Store에 저장된 청년 지원 정책과 해당 정책의 정보를 검색한다.
        이 도구는 청년 지원 정책 관련 질문에 대해 실행한다.
        """
        result = retriever.invoke(query)
        return result if result else [Document(page_content="검색 결과가 없습니다.")]

    # web 검색 tool
    @tool
    def search_web(query: str) -> list[Document]:
        """
        Web에서 청년 지원 정책과 해당 정책의 정보를 검색한다.
        이 도구는 청년 지원 정책 관련 질문에 대해 실행한다.
        """
        try:
            tavily_search = TavilySearchResults(max_results=2)
            result = tavily_search.invoke(query)
            if result:
                return [
                    Document(
                        page_content=item.get("content", ""),
                        metadata={"title": item.get("title", "")},
                    )
                    for item in result
                ]
            else:
                return [Document(page_content="검색 결과가 없습니다.")]
        except Exception as e:
            return [Document(page_content=f"오류 발생: {str(e)}")]

    def __init__(self, agent=None):

        model = ChatOpenAI(model="gpt-4o-mini")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder("agent_scratchpad"),
                (
                    "ai",
                    dedent(
                        """
                당신은 유능한 청년지원정책 추천 전문 AI 챗봇입니다.
                주요 목표는 사용자의 요청에 따라 알맞는 청년지원정책을 추천하는 것입니다.
                다음은 답변을 작성하기 위한 지침(guidelines)입니다:
                1. 주어진 context(데이터 및 검색 결과)를 바탕으로만 대답해주세요.
                2. 모든 답변은 학습된 정책 데이터를 바탕으로 사용자가 물어본 질문에 대한 정확한 정보만 작성하세요.
                3. 답변에 불필요한 정보는 제공하지 마세요. 
                4. 해당 데이터에 없는 내용은 검색해서 대답세요. 다만, 검색 도구(TavilySearch 등)에서도 찾을 수 없는 경우, 답변을 추측하거나 임의로 생성하지 말고 "잘 모르겠습니다."라고 답변하세요.검색으로도 정보를 찾을 수 없을 경우 답변을 추측하거나 임의로 생성하지말고, "잘 모르겠습니다."라고 답변하세요.
                5. 답변은 체계적이고, 비전문가 사용자도 이해하기 쉽게 답변을 작성하세요.
                6. 항상 최신의 정확한 정보를 제공하기 위해 노력하세요.
                7. 질문을 완전히 이해하지 못할 경우, 구체적인 질문을 다시 받을 수 있도록 사용자에게 유도 질문을 하세요.     
                8. 답변 스타일은 간결하고 논리적으로 작성하세요. 필요시, 리스트 형식으로 정리하세요.
                
                위 지침을 따라 사용자의 요청에 맞는 적절한 청년지원정책 정보를 제공합니다.
                {context}
            """
                    ),
                ),
                MessagesPlaceholder("history"),
                ("human", "{question}"),
            ]
        )
        memory = ConversationBufferMemory()  # 메모리 설정
        model = ChatOpenAI(model="gpt-4o", temperature=0)
        parser = StrOutputParser()

        # agent 구성
        agent = create_tool_calling_agent(
            llm=model,
            tools=[self.search_policy, self.search_web],
            prompt=prompt_template,
        )
        self.agent = agent

        runnable = (
            {
                "context": RunnableLambda(lambda x: retriever.invoke(x["question"])),
                "question": itemgetter("question"),
                "history": itemgetter("history"),
            }
            | prompt_template
            | model
            | parser
        )

        chain = RunnableWithMessageHistory(
            runnable=runnable,
            get_session_history=lambda session_id: memory.chat_memory,
            input_messages_key="question",
            history_messages_key="history",
        )

    def send_message(self, message: str, history: list):
        """
        사용자 메시지를 처리하고 AI 응답을 반환.
        Parameter:
            message: str 사용자가 입력한 메시지
            history: list - 사용자와 AI간의 이전까지의 대화 기록

        Returns:
            str: AI의 응답 메시지
        """
        query = message.strip()
        toolkit = [self.search_policy, self.search_web]

        agent_executor = AgentExecutor(agent=self.agent, tools=toolkit, verbose=True)
        context = "기본 context가 비어 있습니다. 적절한 데이터를 제공하세요."
        history = []

        result_from_db = self.search_policy.invoke(query)
        result_from_web = self.search_web.invoke(query)
        print(result_from_db)
        print(result_from_web)
        combined_context = [
            "저장된 데이터에서 찾은 정보:\n",
            *[doc.page_content for doc in result_from_db],
            "실시간 web 검색에서 확인된 정보:\n",
        ]
        if result_from_web:
            combined_context.extend(
                [
                    f"[{idx}] {doc.metadata.get('title', '제목 없음')}: {doc.page_content}"
                    for idx, doc in enumerate(result_from_web, start=1)
                ]
            )
        else:
            combined_context.append("web 검색 결과가 없습니다.")
        response = agent_executor.invoke(
            {
                "question": query,
                "context": combined_context,
                "history": history,
            }
        )

        return response


def add_message_to_history(
    history: list[tuple[str, str]], message: tuple[str, str], max_history=20
):
    """
    Message를 history에 추가하는 util 메소드.
    파라미터로 받은 history에 message를 추가한다.
    max_history 개수를 넘어가면 오래된 것 부터 지운다.
    Parameter:
        history: list - 대화 기록
        message: tuple - (speaker, message) 형태의 메시지
        max_history: int - 저장할 최대 대화 기록 개수
    """
    while len(history) >= max_history:
        history.pop(0)
    history.append(message)
    