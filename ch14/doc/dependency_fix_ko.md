# PDF 처리 스크립트 종속성 해결

## 문제: Apple Silicon (M-시리즈) Mac에서의 아키텍처 비호환성

Python PDF 처리 스크립트를 실행하려고 할 때, "아키텍처 비호환성" 메시지(예: `arm64`가 필요한데 `x86_64`를 가지고 있음)로 인한 여러 `ImportError` 예외가 발생했습니다. 이 문제는 `pymupdf`, `cryptography` (`pdfminer.six`를 통해), `cffi`, `numpy` (`pandas`를 통해)를 포함한 여러 C 확장 라이브러리에서 발생했습니다.

조사 결과, 가상 환경 `/Users/kks/Desktop/Laboratory/jocoding_langchain/env/`에서 실행 중인 Python 인터프리터 자체가 `x86_64` 빌드였습니다. `arm64` Apple Silicon Mac에서 `x86_64` Python 인터프리터는 Rosetta 2 에뮬레이션 하에서 실행되며, 기본적으로 `pip`은 이러한 환경을 위해 `x86_64`로 사전 컴파일된 휠(`.whl` 파일)을 설치하는 경향이 있습니다. 이로 인해 시스템이 `arm64` 바이너리를 기대할 때 충돌이 발생했습니다.

## 해결 단계:

1.  **가상 환경 활성화:** 사용자님의 초기 제안에 따라 올바른 가상 환경(`/Users/kks/Desktop/Laboratory/jocoding_langchain/env/`)이 활성화되었는지 확인했습니다. 이것이 아키텍처 문제를 즉시 해결하지는 못했지만, 이후의 `pip` 작업이 올바른 환경 내에서 이루어지도록 보장했습니다.

2.  **핵심 종속성 강제 재설치:** `pip install --upgrade` 및 `ARCHFLAGS="-arch arm64" pip install` 명령이 `arm64` 휠을 강제하지 못했기 때문에 (`pip`이 `x86_64` Python 인터프리터와 호환되는 `x86_64` 휠을 우선적으로 설치했기 때문입니다), 일련의 강제 재설치를 수행했습니다:
    *   문제가 되는 모든 패키지(`pymupdf`, `pdfplumber`, `pandas`, `numpy`, `cryptography`, `cffi`, `pdfminer.six`)를 제거했습니다.
    *   `pip install --force-reinstall --no-cache-dir <package_name>`을 사용하여 다시 설치했습니다. 대부분의 패키지에 대해 `pip`이 계속해서 `x86_64` 휠을 다운로드했지만, 이 과정은 패키지 설치 및 내부 연결을 새로 고치는 데 도움이 된 것으로 보입니다.

3.  **누락된 `tabulate` 라이브러리 설치:** `pandas.DataFrame.to_markdown()`에서 필요한 `tabulate` 라이브러리의 `ModuleNotFoundError`는 `pip install tabulate` 명령으로 해결되었습니다.

## 결과:

Python 인터프리터가 `x86_64`로 실행되고 `x86_64` 바이너리 휠이 설치되었음에도 불구하고, 연속적인 재설치는 `ImportError` 문제를 해결했습니다. 필요한 모든 라이브러리(`fitz`, `pdfplumber`, `pandas`)가 성공적으로 임포트 가능하게 되었고, `process_pdf.py` 스크립트는 추가적인 종속성 오류 없이 PDF에서 텍스트, 테이블, 이미지를 성공적으로 추출했습니다.

## 향후 권장 사항:

최적의 성능을 위해 그리고 Apple Silicon Mac에서 유사한 종속성 충돌을 피하기 위해, 네이티브 `arm64` Python 인터프리터(예: `pyenv`, `miniforge` 또는 네이티브 Homebrew Python 빌드를 통해 설치)를 사용하는 것을 강력히 권장합니다. 이렇게 하면 `pip`이 `arm64` 휠을 우선적으로 설치하여 더 나은 호환성과 성능을 제공할 수 있습니다.
