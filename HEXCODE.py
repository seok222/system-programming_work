 def analyze_hex_code(hex_code):
    """
    SIC/XE 기계어 HEX 코드를 분석하여 각 필드를 추출하고 Target Address를 계산하는 함수
    
    Args:
        hex_code (str): 분석할 HEX 코드 (예: "032600")
    
    Returns:
        dict: 분석 결과를 담은 딕셔너리
    """
    
    # 분석 시작 메시지 출력
    print(f"HEX 코드 '{hex_code}' 분석을 시작합니다.")
    print("=" * 60)
    
    # ========================================================================
    # 1단계: HEX 코드를 24비트 Binary 코드로 변환
    # ========================================================================
    print("1단계: HEX to Binary 변환")
    print(f"   입력 HEX: {hex_code}")
    
    # HEX 문자열을 정수로 변환 (16진법 → 10진법)
    # int() 함수의 두 번째 매개변수 16은 16진법을 의미
    decimal_value = int(hex_code, 16)
    print(f"   10진수 변환: {decimal_value}")
    
    # bin() 함수로 2진법 변환, [2:]로 '0b' 접두사 제거
    # zfill(24)로 24비트 길이에 맞춰 앞에 0으로 패딩
    binary_code = bin(decimal_value)[2:].zfill(24)
    print(f"   24비트 Binary: {binary_code}")
    print()

    # ========================================================================
    # 2단계: Opcode 추출 (비트 0-5, 상위 6비트)
    # ========================================================================
    print("2단계: Opcode 추출")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   Opcode 영역: {binary_code[:6]}******************")
    
    # Python 슬라이싱으로 상위 6비트 추출 (인덱스 0부터 5까지)
    opcode_binary = binary_code[:6]
    
    # 2진법 문자열을 정수로 변환한 후 다시 16진법으로 변환
    opcode_decimal = int(opcode_binary, 2)  # 2진법을 10진법으로
    opcode_hex = hex(opcode_decimal)[2:].upper().zfill(2)  # 10진법을 16진법으로, 대문자 변환, 2자리 맞춤
    
    print(f"   Opcode Binary: {opcode_binary}")
    print(f"   Opcode HEX: {opcode_hex}")
    print()

    # ========================================================================
    # 3단계: nixbpe 플래그 추출 및 분석 (비트 6-11)
    # ========================================================================
    print("3단계: nixbpe 플래그 분석")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   nixbpe 영역: ******{binary_code[6:12]}************")
    
    # 슬라이싱으로 비트 6부터 11까지 추출 (총 6비트)
    nixbpe_bits = binary_code[6:12]
    
    # 각 플래그 비트를 개별적으로 추출하여 정수로 변환
    n_bit = int(nixbpe_bits[0])  # bit 6: indirect addressing flag (간접 어드레싱)
    i_bit = int(nixbpe_bits[1])  # bit 7: immediate addressing flag (즉시 어드레싱)
    x_bit = int(nixbpe_bits[2])  # bit 8: indexed addressing flag (인덱스 어드레싱)
    b_bit = int(nixbpe_bits[3])  # bit 9: base-relative addressing flag (베이스 상대 어드레싱)
    p_bit = int(nixbpe_bits[4])  # bit 10: PC-relative addressing flag (PC 상대 어드레싱)
    e_bit = int(nixbpe_bits[5])  # bit 11: extended format flag (확장 포맷)
    
    print(f"   nixbpe: {nixbpe_bits}")
    print(f"   n={n_bit} (indirect), i={i_bit} (immediate), x={x_bit} (indexed)")
    print(f"   b={b_bit} (base-relative), p={p_bit} (PC-relative), e={e_bit} (extended)")
    print()

    # ========================================================================
    # 4단계: 어드레싱 모드 및 명령어 포맷 결정
    # ========================================================================
    print("4단계: 어드레싱 모드 및 포맷 결정")
    
    # 어드레싱 모드 결정: n, i 비트 조합에 따른 분류
    print("   어드레싱 모드 결정 (n, i 비트 조합):")
    
    # n=1, i=1인 경우: 일반적인 SIC/XE Simple addressing
    if n_bit == 1 and i_bit == 1:
        addressing_mode = "SIC/XE, Simple"
        print(f"   n=1, i=1 → Simple addressing (일반적인 SIC/XE 어드레싱)")
    # n=1, i=0인 경우: 간접 어드레싱 모드
    elif n_bit == 1 and i_bit == 0:
        addressing_mode = "Indirect"
        print(f"   n=1, i=0 → Indirect addressing (간접 어드레싱)")
    # n=0, i=1인 경우: 즉시 어드레싱 모드
    elif n_bit == 0 and i_bit == 1:
        addressing_mode = "Immediate"
        print(f"   n=0, i=1 → Immediate addressing (즉시 어드레싱)")
    # n=0, i=0인 경우: 표준 SIC 어드레싱
    else:
        addressing_mode = "SIC Standard"
        print(f"   n=0, i=0 → SIC Standard (표준 SIC 어드레싱)")
    
    # 명령어 포맷 결정: e 비트에 따른 분류
    print("   명령어 포맷 결정 (e 비트):")
    
    # e=1이면 Format 4 (확장 포맷), e=0이면 Format 3 (기본 포맷)
    if e_bit == 1:
        format_type = "Format 4"
        print(f"   e=1 → Format 4 (확장 포맷, 4바이트 명령어)")
    else:
        format_type = "Format 3"
        print(f"   e=0 → Format 3 (기본 포맷, 3바이트 명령어)")
    
    # 상대 어드레싱 타입 결정: b, p 비트에 따른 분류
    print("   상대 어드레싱 타입 결정 (b, p 비트):")
    
    # p=1인 경우: PC 상대 어드레싱
    if p_bit == 1:
        addr_type = "PC-relative"
        print(f"   p=1 → PC-relative addressing (프로그램 카운터 상대 어드레싱)")
    # p=0, b=1인 경우: 베이스 상대 어드레싱
    elif b_bit == 1:
        addr_type = "Base-relative"
        print(f"   b=1 → Base-relative addressing (베이스 레지스터 상대 어드레싱)")
    # p=0, b=0인 경우: 직접 어드레싱
    else:
        addr_type = "Direct"
        print(f"   b=0, p=0 → Direct addressing (직접 어드레싱)")
    print()

    # ========================================================================
    # 5단계: Displacement/Address 필드 추출 (비트 12-23, 하위 12비트)
    # ========================================================================
    print("5단계: Displacement/Address 필드 추출")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   disp 영역:   ************{binary_code[12:]}")
    
    # 슬라이싱으로 비트 12부터 23까지 추출 (총 12비트)
    disp_bits = binary_code[12:]
    
    # displacement를 2진법에서 10진법으로 변환
    disp_decimal = int(disp_bits, 2)
    
    # displacement를 16진법으로 변환, 대문자로 변환, 3자리 맞춤
    disp_hex = hex(disp_decimal)[2:].upper().zfill(3)
    
    print(f"   Displacement Binary: {disp_bits}")
    print(f"   Displacement Decimal: {disp_decimal}")
    print(f"   Displacement HEX: {disp_hex}")
    print()

    # ========================================================================
    # 6단계: Target Address 계산 (PC-relative 어드레싱 기준)
    # ========================================================================
    print("6단계: Target Address 계산")
    
    # random 모듈을 import하여 PC 값을 동적으로 설정
    import random
    
    # 실제 시스템에서는 프로그램 로더가 메모리에 프로그램을 적재할 때 PC 값이 결정됨
    # 일반적인 사용자 프로그램 메모리 영역에서 선택 (0x1000~0x5000)
    possible_pc_values = [0x1000, 0x2000, 0x3000, 0x4000, 0x5000]
    pc_value = random.choice(possible_pc_values)
    
    print(f"   현재 PC (Program Counter): 0x{pc_value:04X}")
    print(f"   (주의: PC 값은 프로그램 로드 위치에 따라 실행 시마다 달라질 수 있음)")
    
    # p_bit가 1인 경우 PC-relative addressing 적용
    if p_bit == 1:
        print("   PC-relative addressing 모드 적용")
        print("   공식: Target Address = PC + displacement")
        
        # 12비트 2의 보수 처리
        # 12비트에서 최상위 비트가 1이면 음수를 의미
        # 2^11 = 2048이므로, displacement가 2048 이상이면 음수로 처리
        if disp_decimal >= 2048:
            print(f"   displacement {disp_decimal} >= 2048 → 2의 보수로 음수 처리")
            
            # 12비트 2의 보수: 4096(2^12)에서 displacement를 빼면 실제 음수 값
            signed_displacement = disp_decimal - 4096
            
            # PC 값에 음수 displacement를 더함
            target_address = pc_value + signed_displacement
            
            print(f"   계산: 0x{pc_value:04X} + ({disp_decimal} - 4096) = 0x{pc_value:04X} + ({signed_displacement}) = 0x{target_address:04X}")
        else:
            print(f"   displacement {disp_decimal} < 2048 → 양수 처리")
            
            # PC 값에 양수 displacement를 더함
            target_address = pc_value + disp_decimal
            
            print(f"   계산: 0x{pc_value:04X} + {disp_decimal} = 0x{target_address:04X}")
    else:
        # Direct addressing인 경우 displacement가 곧 절대 주소
        print("   Direct addressing 모드 적용")
        print("   Target Address = displacement (절대 주소)")
        target_address = disp_decimal
        print(f"   Target Address = 0x{target_address:04X}")
    print()

    # ========================================================================
    # 7단계: Register A 값 설정 (현재 누산기 상태 시뮬레이션)
    # ========================================================================
    print("7단계: Register A 값 (누산기 레지스터 현재 상태)")
    
    # Register A는 SIC/XE의 주요 누산기 레지스터
    # 실제 시스템에서는 이전 명령어의 실행 결과에 따라 값이 결정됨
    possible_register_values = [0x50000, 0x75000, 0x103000, 0x200000, 0x45000]
    
    # random.choice()로 가능한 값 중 하나를 선택
    register_a = random.choice(possible_register_values)
    
    print(f"   Register A = 0x{register_a:06X}")
    print(f"   (주의: Register A 값은 이전 명령어 실행 결과에 따라 달라짐)")
    print()
    
    # 분석 완료 메시지 출력
    print("분석 완료. 최종 결과를 출력합니다.")
    print("=" * 60)

    # ========================================================================
    # 8단계: 분석 결과를 딕셔너리로 반환
    # ========================================================================
    # 모든 분석 결과를 딕셔너리 형태로 정리하여 반환
    return {
        'hex_input': hex_code.upper(),                    # 입력된 HEX 코드 (대문자)
        'binary_code': binary_code,                       # 24비트 2진법 코드
        'opcode': opcode_binary,                         # Opcode (2진법으로 출력)
        'nixbpe': nixbpe_bits,                           # nixbpe 플래그 (2진법)
        'flags': {                                       # 각 플래그 비트
            'n': n_bit,                                  # indirect addressing flag
            'i': i_bit,                                  # immediate addressing flag
            'x': x_bit,                                  # indexed addressing flag
            'b': b_bit,                                  # base-relative addressing flag
            'p': p_bit,                                  # PC-relative addressing flag
            'e': e_bit                                   # extended format flag
        },
        'flag_description': f"SIC/XE, {addressing_mode}, {addr_type}, {format_type}",  # 플래그 설명
        'disp_addr': disp_hex,                           # displacement (16진법)
        'disp_decimal': disp_decimal,                    # displacement (10진법)
        'target_address': hex(target_address)[2:].upper(),  # Target Address (16진법)
        'register_a': hex(register_a)[2:].upper(),       # Register A 값 (16진법)
        'pc_value': hex(pc_value)[2:].upper()            # PC 값 (16진법)
    }

def print_analysis(result):
    """
    분석 결과를 체계적으로 출력하는 함수
    
    Args:
        result (dict): analyze_hex_code 함수에서 반환된 분석 결과 딕셔너리
    """
    
    # 최종 결과 출력 헤더
    print("=" * 60)
    print("SIC/XE 기계어 HEX 코드 분석 최종 결과")
    print("=" * 60)
    
    # 각 분석 결과를 형식에 맞춰 출력
    print(f"Hex 입력          : {result['hex_input']}")                      # 원본 HEX 입력
    print(f"Binary            : {result['binary_code']}")                   # 24비트 2진법 변환 결과
    print(f"Opcode            : {result['opcode']}")                        # 명령어 코드
    
    # nixbpe 플래그와 각 비트값을 함께 출력
    print(f"nixbpe            : {result['nixbpe']} (n={result['flags']['n']} i={result['flags']['i']} x={result['flags']['x']} b={result['flags']['b']} p={result['flags']['p']} e={result['flags']['e']})")
    
    print(f"Flag bit          : {result['flag_description']}")              # 플래그 종합 설명
    print(f"disp/addr         : {result['disp_addr']}")                     # displacement 값
    
    # Target Address 계산 과정을 함께 표시
    print(f"Target Address    = 0x{result['target_address']} (PC: 0x{result['pc_value']} + 0x{result['disp_addr']})")
    
    print(f"Register A value  = 0x{result['register_a']}")                  # 누산기 레지스터 값

# ============================================================================
# 메인 실행 부분 - 프로그램의 진입점
# ============================================================================
if __name__ == "__main__":
    # 분석 대상 HEX 코드 정의
    hex_code = "032600"
    
    # 프로그램 시작 메시지 출력
    print("SIC/XE 기계어 HEX 코드 분석 프로그램")
    print("=" * 60)
    
    # HEX 코드 분석 함수 호출하여 결과 받기
    result = analyze_hex_code(hex_code)
    
    # 분석 결과를 체계적으로 출력
    print_analysis(result)
    
    # 분석 과정 요약 출력
    print("\n" + "=" * 60)
    print("분석 과정 요약")
    print("=" * 60)
    
    # 1단계 요약: HEX to Binary 변환
    print("1. HEX to Binary 변환:")
    print(f"   {hex_code} → {result['binary_code']}")
    
    # 2단계 요약: Opcode 추출
    print("\n2. Opcode 추출 (비트 0-5):")
    print(f"   {result['binary_code'][:6]} → {result['opcode']}")
    
    # 3단계 요약: nixbpe 플래그 추출
    print("\n3. nixbpe 플래그 추출 (비트 6-11):")
    print(f"   {result['nixbpe']} → n={result['flags']['n']}, i={result['flags']['i']}, x={result['flags']['x']}, b={result['flags']['b']}, p={result['flags']['p']}, e={result['flags']['e']}")
    
    # 4단계 요약: Displacement 추출
    print("\n4. Displacement 추출 (비트 12-23):")
    print(f"   {result['binary_code'][12:]} → {result['disp_addr']} (십진수: {result['disp_decimal']})")
    
    # 5단계 요약: Target Address 계산
    print("\n5. Target Address 계산:")
    print(f"   PC-relative: PC(0x{result['pc_value']}) + displacement(0x{result['disp_addr']}) = 0x{result['target_address']}")
    
    # 주의사항 안내
    print("\n주의사항:")
    print("- PC 값은 프로그램 메모리 로드 위치에 따라 실행 시마다 달라질 수 있습니다.")
    print("- Register A 값은 이전 명령어 실행 결과에 따라 달라집니다.")
