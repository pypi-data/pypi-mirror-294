import ctypes
import pypandoc
import os
import base64
from bs4 import BeautifulSoup
from moapy.auto_convert import auto_schema
from moapy.data_pre import MemberForce, ReportType
from moapy.data_post import ResultMD
from moapy.steel_pre import SteelMaterial, SteelSection

def rtf_to_markdown(file_path):
    # 파일 경로가 bytes로 주어진 경우 문자열로 변환
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # RTF 파일을 Markdown으로 변환
        markdown_content = pypandoc.convert_file(file_path, 'md', format='rtf')

        # HTML로 변환된 이미지 태그를 찾아서 처리
        soup = BeautifulSoup(markdown_content, 'html.parser')
        for img in soup.find_all('img'):
            img_path = img['src']
            if os.path.exists(img_path):
                with open(img_path, 'rb') as image_file:
                    # 이미지를 base64로 인코딩
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    # 이미지 태그를 base64로 교체
                    img['src'] = f"data:image/png;base64,{encoded_string}"

        # HTML을 다시 Markdown으로 변환
        markdown_with_images = str(soup)
        return markdown_with_images

    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error converting RTF to Markdown: {e}")

def read_txt_file(file_path):
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # 파일 열기 및 내용 읽기
        with open(file_path, 'r', encoding='utf-16') as file:
            file_content = file.read()
        return file_content
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

@auto_schema
def calc_steel_bc(matl: SteelMaterial, sect: SteelSection, load: MemberForce):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()

    # process_data 함수 정의 및 호출
    dll.Calc_Steel.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Calc_Steel.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Calc_Steel(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'))

    # JSON 문자열을 Python 딕셔너리로 변환
    return result

@auto_schema
def report_steel_bc(matl: SteelMaterial, sect: SteelSection, load: MemberForce, rptType: ReportType) -> ResultMD:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()
    rptType_json = rptType.json()

    # process_data 함수 정의 및 호출
    dll.Report_Steel.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_Steel.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_Steel(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'), rptType_json.encode('utf-8'))

    report = ResultMD()
    report.md = rtf_to_markdown(result)

    return report

@auto_schema
def report_ec3_beam_column(matl: SteelMaterial, sect: SteelSection, load: MemberForce, rptType: ReportType) -> ResultMD:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    matl_json = matl.json()
    sect_json = sect.json()
    load_json = load.json()
    rptType_json = rptType.json()

    # process_data 함수 정의 및 호출
    dll.Report_EC3_BeamColumn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_EC3_BeamColumn.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_EC3_BeamColumn(matl_json.encode('utf-8'), sect_json.encode('utf-8'), load_json.encode('utf-8'), rptType_json.encode('utf-8'))

    report = ResultMD()
    report.md = rtf_to_markdown(result)

    return report