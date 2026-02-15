# LangChain 버전 및 의존성 문제 해결 보고서

## 1. 개요 (Overview)
본 프로젝트는 기존 강의 자료 기반의 소스 코드(`requirements.txt` 포함)와 최신 LangChain 환경 간의 버전 불일치로 인해 여러 `ImportError` 및 의존성 충돌 문제가 발생했습니다.
특히 `langchain-classic` 패키지와 최신 `langchain 0.3.x` 패키지 간의 호환성 문제가 주된 원인이었습니다.

본 문서는 이러한 문제를 해결하기 위해 수행한 작업 내역을 기록합니다.

## 2. 문제 상황 (Issues Identified)

### 2.1 주요 에러
1.  **`ImportError: cannot import name 'AgentExecutor' from 'langchain.agents'`**
    *   원인: `langchain` 버전 0.2.0 이후 패키지 구조가 변경되었거나, `langchain-classic`과 `langchain-core` 버전 충돌로 인해 올바른 모듈을 로드하지 못함.
2.  **의존성 충돌 (Dependency Conflicts)**
    *   `langchain-classic 1.0.1`은 `langchain-core < 2.0.0`을 요구하지만, 최신 `langchain 0.3.x`는 `langchain-core >= 0.3.x`를 요구함. 두 패키지를 동시에 설치할 수 없음.
3.  **구버전 코드 호환성**
    *   기존 소스 코드들이 `langchain_classic` 패키지를 참조하고 있어, 최신 환경에서 실행 불가.

## 3. 해결 조치 (Actions Taken)

### 3.1 환경 재구성 (Environment Reset)
*   **조치:** `langchain-classic` 패키지를 사용하지 않고, **최신 `langchain` (0.3.x)** 기반으로 환경을 통일하기로 결정.
*   **작업:**
    1.  `requirements.txt`에서 `langchain-classic` 제거.
    2.  `env` 가상환경 삭제 후 `arch -arm64` 모드로 재생성.
    3.  패키지 재설치 (`pip install -r requirements.txt`).

### 3.2 소스 코드 일괄 수정 (Code Refactoring)
기존 코드들이 `langchain_classic`이나 구버전 경로를 참조하고 있어, 이를 최신 LangChain 경로로 수정했습니다.

#### A. `langchain_classic` -> `langchain`
*   `langchain_classic` 모듈을 사용하는 모든 `.py` 및 `.ipynb` 파일의 import 문을 `langchain`으로 일괄 변경.
*   대상 파일:
    *   `ch04/sequential_chain_01.py`, `ch04/sequential_chain_02.py`
    *   `ch06/app.py`
    *   `ch07/main.py`
    *   `ch12-13/rag_advanced_streamlit.py`
    *   `ch12-13/*.ipynb`
    *   `ch17/langchain_agent.py`

#### B. `document_loaders` 경로 수정
*   **변경 전:** `from langchain.document_loaders import ...`
*   **변경 후:** `from langchain_community.document_loaders import ...`
*   이유: 최신 버전에서 `document_loaders`는 `langchain-community` 패키지로 이동됨.

#### C. `BM25Retriever` 경로 수정
*   **변경 전:** `from langchain.retrievers import BM25Retriever, EnsembleRetriever`
*   **변경 후:**
    ```python
    from langchain_community.retrievers import BM25Retriever
    from langchain.retrievers import EnsembleRetriever
    ```
*   이유: `BM25Retriever`는 `langchain-community`로 이동하고, `EnsembleRetriever`는 `langchain`에 남아있어 import 경로를 분리해야 함.

## 4. 결과 (Result)
*   `ch16` 프로젝트 실행에 필요한 `AgentExecutor`가 `langchain.agents`에서 정상적으로 로드됨.
*   다른 챕터의 코드들도 최신 패키지 경로(`langchain`, `langchain_community`)를 참조하도록 수정되어 Import 에러가 해소됨.
*   **현재 상태:** 프로젝트 전반에 걸쳐 Import 에러 없이 정상적인 실행 환경이 구축됨.

## 5. 참고 사항 (Notes)
*   향후 LangChain 업데이트 시 패키지 이동이 또 발생할 수 있으므로, `ImportError` 발생 시 공식 문서를 확인하여 해당 컴포넌트가 `langchain-core` 또는 `langchain-community`로 이동했는지 확인이 필요합니다.
