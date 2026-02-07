import fitz  # PyMuPDF
import pdfplumber
import os
import pandas as pd
from pathlib import Path

def extract_pdf_elements(path: str, fname: str):
    """
    PyMuPDF와 pdfplumber를 사용하여 PDF에서 텍스트, 테이블, 이미지를 추출합니다.

    :param path: 이미지를 저장할 디렉토리 경로
    :param fname: 처리할 PDF 파일의 전체 경로
    :return: 텍스트와 테이블(마크다운 형식)이 혼합된 요소 리스트
    """
    full_path = Path(fname)
    if not full_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {fname}")

    # 이미지 저장 경로 확인 및 생성
    image_path = Path(path)
    image_path.mkdir(exist_ok=True)

    raw_pdf_elements = []

    # 텍스트 및 이미지 추출 (PyMuPDF 사용)
    doc = fitz.open(fname)
    
    print(f"'{full_path.name}' 파일 처리 중: 총 {len(doc)} 페이지")

    for page_num, page in enumerate(doc):
        # 페이지별 텍스트 추출
        text = page.get_text()
        if text.strip():  # 비어있지 않은 텍스트만 추가
            raw_pdf_elements.append(text)

        # 이미지 추출 및 저장
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
            image_save_path = image_path / image_filename
            
            with open(image_save_path, "wb") as img_file:
                img_file.write(image_bytes)
    
    doc.close()

    # 테이블 추출 (pdfplumber 사용)
    with pdfplumber.open(fname) as pdf:
        for page_num, page in enumerate(pdf.pages):
            try:
                tables = page.extract_tables()
                for table_data in tables:
                    if table_data:
                        # 리스트의 리스트 형태인 테이블 데이터를 Markdown 문자열로 변환
                        # 첫 번째 행을 헤더로 사용하고 나머지 행을 데이터로 사용
                        df = pd.DataFrame(table_data[1:], columns=table_data[0])
                        markdown_table = df.to_markdown(index=False)
                        raw_pdf_elements.append(markdown_table)
            except AttributeError:
                print(f"{page_num + 1}페이지에서 테이블을 추출하는 동안 AttributeError가 발생했지만, 계속 진행합니다.")
                continue # 예외 발생 시에도 중단하지 않고 계속 진행

    return raw_pdf_elements

def categorize_elements(raw_pdf_elements: list):
    """
    추출된 요소 리스트를 텍스트와 테이블로 분류합니다.

    :param raw_pdf_elements: 텍스트와 테이블(마크다운)이 섞인 리스트
    :return: (texts 리스트, tables 리스트) 튜플
    """
    texts = []
    tables = []
    for element in raw_pdf_elements:
        # Markdown 테이블 형식인지 간단히 확인 ( '|' 문자로 시작하고 끝나는지)
        # Markdown 테이블은 헤더와 구분선이 필수적으로 포함되므로 이를 기준으로 판단
        if isinstance(element, str) and element.strip().startswith("|") and "---" in element:
            tables.append(element)
        else:
            texts.append(element)
    return texts, tables

if __name__ == '__main__':
    # 테스트를 위한 설정
    # 현재 디렉토리 (ch14)를 기준으로 상대 경로 설정
    pdf_directory = "invest"
    pdf_filename = "market.pdf"
    output_image_directory = "extracted_data"
    
    # PDF 파일의 전체 경로
    pdf_filepath = os.path.join(os.getcwd(), pdf_directory, pdf_filename)

    # 출력 이미지 디렉토리 생성 (현재 디렉토리 기준)
    output_image_full_path = os.path.join(os.getcwd(), output_image_directory)

    # PDF 요소 추출
    if os.path.exists(pdf_filepath):
        print("PDF 요소 추출을 시작합니다...")
        raw_elements = extract_pdf_elements(path=output_image_full_path, fname=pdf_filepath)
        
        # 요소 분류
        texts, tables = categorize_elements(raw_elements)
        
        print("\n--- 추출된 텍스트 (일부) ---")
        for i, txt in enumerate(texts[:2]): # 처음 2개 텍스트 블록만 출력
            print(f"[텍스트 블록 {i+1}]")
            print(txt[:300] + "...") # 300자까지만 출력
            print("-" * 20)

        print(f"\n총 {len(texts)}개의 텍스트 블록 추출 완료.")

        print("\n--- 추출된 테이블 (일부) ---")
        for i, tbl in enumerate(tables[:2]): # 처음 2개 테이블만 출력
            print(f"[테이블 {i+1}]")
            print(tbl)
            print("-" * 20)
            
        print(f"\n총 {len(tables)}개의 테이블 추출 완료.")
        
        print(f"\n이미지는 '{output_image_full_path}' 디렉토리에 저장되었습니다.")

    else:
        print(f"오류: 테스트 PDF 파일 '{pdf_filepath}'을(를) 찾을 수 없습니다.")
        print("스크립트를 실행하기 전에 'invest' 디렉토리에 'market.pdf' 파일이 있는지 확인해주세요.")
