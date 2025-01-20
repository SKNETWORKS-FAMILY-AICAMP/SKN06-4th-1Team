# <br>🧐**내게 필요한 청년정책 알려줘! 챗봇**🤖
> **SK Networks AI CAMP 6기 - 1Team** <br/> **개발기간: 2025.01.16 ~ 2025.01.20**
---

# **개발 팀** <br>
## <br> **팀명** <br>
![team_name](https://github.com/user-attachments/assets/c623e101-7db5-4e9e-8d26-b04ec270185f)

## <br> **팀 소개** <br>
| 고성주 | 김지영 | 이세화 | 정유진 | 정지원 |
|:----------:|:----------:|:----------:|:----------:|:----------:|
| ![1_sj](https://github.com/user-attachments/assets/9fb495e0-732f-4eb3-9dc0-541eccbcd2e4)| ![2_jy](https://github.com/user-attachments/assets/f3940834-2f8e-4b5d-9988-d85c0f4c6cab)| ![3_sh](https://github.com/user-attachments/assets/8b62f945-e894-49e0-abd4-35f4e5d4010b)| ![4_yj](https://github.com/user-attachments/assets/16dd5434-fd43-42f6-aaa9-1b6b2a90a812)| ![5_jw](https://github.com/user-attachments/assets/4aaa4891-38ea-4679-be53-6d3741c33255)|
|  |  |  |  |  |
<br>

---

# **프로젝트 개요** <br>
## <br> **소개** <br>
> &nbsp;정부에서 진행 중인 청년 정책을 소개해 주는 RAG기반 챗봇 시스템입니다. 대화를 통해 사용자의 조건에 적합한 청년 정책들을 추천해 줍니다.

## <br> **필요성** <br>
> - 정부는 청년들의 경제적·사회적 자립을 돕기 위해 다양한 분야에 막대한 예산을 투입하여 여러 청년 정책을 시행하고 있습니다. 그러나 많은 청년들이 이런 기회들을 놓치고 있습니다.
> - 청년 정책은 매우 방대하여 자신에게 맞는 정책을 찾기가 쉽지 않습니다. 정보가 산발적으로 흩어져 있어 존재하는지도 모르고 지나치는 정책들도 있으며, 본인이 지원 대상에 해당하는지 일일이 확인해야 하고 어떤 정책이 더 큰 혜택을 제공하는지 비교하는 것도 많은 시간과 노력이 필요합니다. 이러한 복잡성은 청년들이 정책을 적극적으로 활용하지 못하게 만드는 주요 원인 중 하나입니다.
> - 이러한 상황에서 질문과 답변을 통해 맞춤형 청년 정책을 추천하는 RAG 기반 챗봇은 큰 도움이 됩니다. 이 챗봇은 사용자에게 적합한 정책들을 빠르고 정확하게 소개합니다. 이를 통해 청년들은 복잡한 정보 탐색 과정 없이 손쉽게 지원 가능한 정책을 확인하고, 더 많은 혜택을 누릴 수 있을 것입니다.

## <br> **주요 기능** <br>
> - **정책 추천**: 대화를 통해 사용자의 조건에 적합한 청년 정책들을 추천해 줍니다.
> - **정확한 정보 제공**: 자체 데이터베이스를 통해 정확한 정보를 제공합니다.
> - **최신 정보 제공**: 검색을 통해 최신 정보를 제공합니다.
> - **사용자 맞춤**: 로그인 기능을 제공합니다.
---

# **요구사항 정의서** <br>
- File_url: 

# **시스템 구성도** <br>
![System_Architecture](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN06-4th-1Team/blob/main/IMG/Sys_Architecture.png)

> ## **account**
> - **account_user** : 사용자의 정보 저장 테이블
> - **컬럼 정보**
> ![account_user]
> - **제약조건**
>   - PRIMARY KEY : ID에 대한 기본 키 제약 조건

<br>

> ## **poll**
> - **poll_question** : 설문조사 질문 저장 테이블
> - **컬럼 정보**
> ![poll_question]
> - **제약조건**
>   - PRIMARY KEY : ID에 대한 기본 키 제약 조건
>  <br>
>
> - **poll_choice**: 설문조사 응답 저장 테이블
> - **컬럼 정보**
> ![poll_choice]
> - **제약조건**
>   - PRIMARY KEY : ID에 대한 기본 키 제약 조건
>   - FOREIGN KEY : question_id에 대한 외래 키 제약 조건(poll_question 테이블 참조)

# **화면 구성도** <br>
- File_url:


# **테스트 계획 및 결과 보고서** <br>


---

# **Review** <br>

> 고성주: 
> 
> 김지영: 
> 
> 이세화: 
> 
> 정유진: 
> 
> 정지원: 


