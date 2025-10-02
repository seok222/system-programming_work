def analyze_hex_code(hex_code):
    """
    SIC/XE 기계어 HEX 코드를 분석하여 각 필드를 추출하고 Target Address를 계산하는 함수
    
    Args:
        hex_code (str): 분석할 HEX 코드 (예: "032600")
    
    Returns:
        dict: 분석 결과를 담은 딕셔너리
    
    중요: SIC/XE Format 3는 24비트(3바이트) 구조
          - Opcode: 6비트 (비트 0-5)
          - nixbpe: 6비트 (비트 6-11)
          - displacement: 12비트 (비트 12-23)
    """
    
    print(f"HEX 코드 '{hex_code}' 분석을 시작합니다.")
    print("=" * 60)
    
    # ========================================================================
    # 1단계: HEX 코드를 24비트 Binary 코드로 변환
    # SIC/XE Format 3 명령어는 3바이트(24비트) 구조를 가짐
    # 
    # 중요: 문제 풀이 순서
    # 1) HEX -> Binary (24비트)
    # 2) Opcode 추출 (앞 6비트)
    # 3) nixbpe 추출 (중간 6비트)
    # 4) displacement 추출 (뒤 12비트)
    # 5) Target Address 계산
    # ========================================================================
    print("1단계: HEX to Binary 변환")
    print(f"   입력 HEX: {hex_code}")
    
    # HEX → 10진수 → Binary 변환 과정
    decimal_value = int(hex_code, 16)
    print(f"   10진수 변환: {decimal_value}")
    
    # zfill(24)로 24비트 맞추기
    # 주의: zfill을 안하면 앞의 0이 사라져서 비트 위치가 틀어짐 (실수 많이 함)
    binary_code = bin(decimal_value)[2:].zfill(24)
    print(f"   24비트 Binary: {binary_code}")
    print()

    # ========================================================================
    # 2단계: Opcode 추출 (비트 0-5, 상위 6비트)
    # 명령어 종류를 결정하는 Opcode는 항상 상위 6비트에 위치
    # ========================================================================
    print("2단계: Opcode 추출")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   Opcode 영역: {binary_code[:6]}******************")
    
    opcode_binary = binary_code[:6]
    opcode_decimal = int(opcode_binary, 2)
    opcode_hex = hex(opcode_decimal)[2:].upper().zfill(2)
    
    print(f"   Opcode Binary: {opcode_binary}")
    print(f"   Opcode HEX: {opcode_hex}")
    print()

    # ========================================================================
    # 3단계: nixbpe 플래그 추출 및 분석 (비트 6-11)
    # nixbpe 6개 플래그가 어드레싱 모드와 포맷을 결정하는 핵심 요소
    # 
    # 각 플래그의 의미 (시험 단골):
    # n, i 조합 -> 어드레싱 모드 결정
    #   n=1, i=1: Simple (가장 일반적)
    #   n=1, i=0: Indirect
    #   n=0, i=1: Immediate
    # x: 인덱스 레지스터 사용 여부
    # b, p 조합 -> 주소 계산 방법
    #   p=1: PC-relative (가장 흔함)
    #   b=1: Base-relative
    # e: 포맷 결정
    #   e=0: Format 3 (3바이트)
    #   e=1: Format 4 (4바이트)
    # ========================================================================
    print("3단계: nixbpe 플래그 분석")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   nixbpe 영역: ******{binary_code[6:12]}************")
    
    nixbpe_bits = binary_code[6:12]
    
    # 각 플래그의 의미
    n_bit = int(nixbpe_bits[0])  # n=1: 간접 어드레싱 가능
    i_bit = int(nixbpe_bits[1])  # i=1: 즉시 어드레싱 가능
    x_bit = int(nixbpe_bits[2])  # x=1: 인덱스 레지스터 사용
    b_bit = int(nixbpe_bits[3])  # b=1: Base 레지스터 기준
    p_bit = int(nixbpe_bits[4])  # p=1: PC 기준 (가장 많이 사용)
    e_bit = int(nixbpe_bits[5])  # e=1: Format 4 (확장), e=0: Format 3
    
    print(f"   nixbpe: {nixbpe_bits}")
    print(f"   n={n_bit} (indirect), i={i_bit} (immediate), x={x_bit} (indexed)")
    print(f"   b={b_bit} (base-relative), p={p_bit} (PC-relative), e={e_bit} (extended)")
    print()

    # ========================================================================
    # 4단계: 어드레싱 모드 및 명령어 포맷 결정
    # ========================================================================
    print("4단계: 어드레싱 모드 및 포맷 결정")
    
    # n, i 비트 조합으로 어드레싱 모드 결정
    # n=1, i=1 -> Simple (가장 일반적으로 사용됨)
    # n=1, i=0 -> Indirect (간접)
    # n=0, i=1 -> Immediate (즉시)
    # n=0, i=0 -> SIC Standard (레거시)
    print("   어드레싱 모드 결정 (n, i 비트 조합):")
    
    if n_bit == 1 and i_bit == 1:
        addressing_mode = "SIC/XE, Simple"
        print(f"   n=1, i=1 → Simple addressing (일반적인 SIC/XE 어드레싱)")
    elif n_bit == 1 and i_bit == 0:
        addressing_mode = "Indirect"
        print(f"   n=1, i=0 → Indirect addressing (간접 어드레싱)")
    elif n_bit == 0 and i_bit == 1:
        addressing_mode = "Immediate"
        print(f"   n=0, i=1 → Immediate addressing (즉시 어드레싱)")
    else:
        addressing_mode = "SIC Standard"
        print(f"   n=0, i=0 → SIC Standard (표준 SIC 어드레싱)")
    
    print("   명령어 포맷 결정 (e 비트):")
    
    # e 비트로 Format 3 vs Format 4 구분
    if e_bit == 1:
        format_type = "Format 4"
        print(f"   e=1 → Format 4 (확장 포맷, 4바이트 명령어)")
    else:
        format_type = "Format 3"
        print(f"   e=0 → Format 3 (기본 포맷, 3바이트 명령어)")
    
    print("   상대 어드레싱 타입 결정 (b, p 비트):")
    
    # p=1이 가장 흔하게 사용됨 (PC-relative가 기본 방식)
    if p_bit == 1:
        addr_type = "PC-relative"
        print(f"   p=1 → PC-relative addressing (프로그램 카운터 상대 어드레싱)")
    elif b_bit == 1:
        addr_type = "Base-relative"
        print(f"   b=1 → Base-relative addressing (베이스 레지스터 상대 어드레싱)")
    else:
        addr_type = "Direct"
        print(f"   b=0, p=0 → Direct addressing (직접 어드레싱)")
    print()

    # ========================================================================
    # 5단계: Displacement/Address 필드 추출 (비트 12-23, 하위 12비트)
    # Format 3에서는 12비트 displacement 사용
    # ========================================================================
    print("5단계: Displacement/Address 필드 추출")
    print(f"   전체 Binary: {binary_code}")
    print(f"   비트 위치:   012345678901234567890123")
    print(f"   disp 영역:   ************{binary_code[12:]}")
    
    disp_bits = binary_code[12:]
    disp_decimal = int(disp_bits, 2)
    disp_hex = hex(disp_decimal)[2:].upper().zfill(3)
    
    print(f"   Displacement Binary: {disp_bits}")
    print(f"   Displacement Decimal: {disp_decimal}")
    print(f"   Displacement HEX: {disp_hex}")
    print()

    # ========================================================================
    # 6단계: Target Address 계산 (PC-relative 어드레싱 기준)
    # 이 부분이 가장 중요한 계산 과정
    # 
    # 공식: Target Address = PC + displacement
    # 
    # 주의: 12비트 2의 보수 처리 (실수 많이 하는 부분)
    #   - displacement < 2048: 양수 그대로 사용
    #   - displacement >= 2048: displacement - 4096으로 음수 처리
    #   - 범위: -2048 ~ +2047
    # 
    # 예: displacement = 2600(16진수) = 9728(10진수)
    #     9728 >= 2048이므로 9728 - 4096 = 5632로 계산
    # ========================================================================
    print("6단계: Target Address 계산")
    
    import random
    
    # 실제 환경에서는 프로그램 로더가 결정
    possible_pc_values = [0x1000, 0x2000, 0x3000, 0x4000, 0x5000]
    pc_value = random.choice(possible_pc_values)
    
    print(f"   현재 PC (Program Counter): 0x{pc_value:04X}")
    print(f"   (주의: PC 값은 프로그램 로드 위치에 따라 실행 시마다 달라질 수 있음)")
    
    if p_bit == 1:
        print("   PC-relative addressing 모드 적용")
        print("   공식: Target Address = PC + displacement")
        
        # 12비트 2의 보수 처리
        # 중요: 12비트에서 최상위 비트가 1이면 음수를 의미
        # 2^11 = 2048이 기준점
        if disp_decimal >= 2048:
            print(f"   displacement {disp_decimal} >= 2048 → 2의 보수로 음수 처리")
            
            # 2^12 = 4096을 빼면 음수 값이 됨
            # 예: 9728 - 4096 = 5632 (음수로 처리)
            signed_displacement = disp_decimal - 4096
            target_address = pc_value + signed_displacement
            
            print(f"   계산: 0x{pc_value:04X} + ({disp_decimal} - 4096) = 0x{pc_value:04X} + ({signed_displacement}) = 0x{target_address:04X}")
        else:
            print(f"   displacement {disp_decimal} < 2048 → 양수 처리")
            target_address = pc_value + disp_decimal
            print(f"   계산: 0x{pc_value:04X} + {disp_decimal} = 0x{target_address:04X}")
    else:
        # Direct addressing인 경우
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
    possible_register_values = [0x50000, 0x75000, 0x103000, 0x200000, 0x45000]
    register_a = random.choice(possible_register_values)
    
    print(f"   Register A = 0x{register_a:06X}")
    print(f"   (주의: Register A 값은 이전 명령어 실행 결과에 따라 달라짐)")
    print()
    
    print("분석 완료. 최종 결과를 출력합니다.")
    print("=" * 60)

    # ========================================================================
    # 8단계: 분석 결과를 딕셔너리로 반환
    # ========================================================================
    return {
        'hex_input': hex_code.upper(),
        'binary_code': binary_code,
        'opcode': opcode_binary,
        'nixbpe': nixbpe_bits,
        'flags': {
            'n': n_bit,
            'i': i_bit,
            'x': x_bit,
            'b': b_bit,
            'p': p_bit,
            'e': e_bit
        },
        'flag_description': f"SIC/XE, {addressing_mode}, {addr_type}, {format_type}",
        'disp_addr': disp_hex,
        'disp_decimal': disp_decimal,
        'target_address': hex(target_address)[2:].upper(),
        'register_a': hex(register_a)[2:].upper(),
        'pc_value': hex(pc_value)[2:].upper()
    }

def print_analysis(result):
    """
    분석 결과를 체계적으로 출력하는 함수
    
    Args:
        result (dict): analyze_hex_code 함수에서 반환된 분석 결과 딕셔너리
    """
    
    print("=" * 60)
    print("SIC/XE 기계어 HEX 코드 분석 최종 결과")
    print("=" * 60)
    
    print(f"Hex 입력          : {result['hex_input']}")
    print(f"Binary            : {result['binary_code']}")
    print(f"Opcode            : {result['opcode']}")
    print(f"nixbpe            : {result['nixbpe']} (n={result['flags']['n']} i={result['flags']['i']} x={result['flags']['x']} b={result['flags']['b']} p={result['flags']['p']} e={result['flags']['e']})")
    print(f"Flag bit          : {result['flag_description']}")
    print(f"disp/addr         : {result['disp_addr']}")
    print(f"Target Address    = 0x{result['target_address']} (PC: 0x{result['pc_value']} + 0x{result['disp_addr']})")
    print(f"Register A value  = 0x{result['register_a']}")

# ============================================================================
# 메인 실행 부분
# ============================================================================
if __name__ == "__main__":
    hex_code = "032600"
    
    print("SIC/XE 기계어 HEX 코드 분석 프로그램")
    print("=" * 60)
    
    result = analyze_hex_code(hex_code)
    print_analysis(result)
    
    # 분석 과정 요약
    print("\n" + "=" * 60)
    print("분석 과정 요약")
    print("=" * 60)
    
    print("\n1. SIC/XE Format 3 구조 (필수 암기)")
    print("   - Opcode: 6비트 (비트 0-5)")
    print("   - nixbpe: 6비트 (비트 6-11)")
    print("   - displacement: 12비트 (비트 12-23)")
    
    print("\n2. nixbpe 플래그 조합 (시험 단골)")
    print("   - n=1, i=1 -> Simple addressing (가장 일반적)")
    print("   - p=1 -> PC-relative (가장 많이 사용)")
    print("   - e=0 -> Format 3, e=1 -> Format 4")
    
    print("\n3. Target Address 계산 공식 (가장 중요)")
    print("   - PC-relative: TA = PC + displacement")
    print("   - 2의 보수 처리: disp >= 2048이면 disp - 4096")
    print("   - 범위: -2048 ~ +2047")
    
    print("\n4. 변환 순서 (문제 풀이 순서)")
    print("   1) HEX -> Binary (24비트, zfill 필수)")
    print("   2) Opcode 추출 (앞 6비트)")
    print("   3) nixbpe 추출 (중간 6비트)")
    print("   4) displacement 추출 (뒤 12비트)")
    print("   5) Target Address 계산")
    
    print("\n5. 실수하기 쉬운 부분")
    print("   - zfill(24) 안하면 앞의 0이 사라짐")
    print("   - displacement >= 2048일 때 2의 보수 처리 안함")
    print("   - PC 값과 displacement 더할 때 16진수/10진수 혼동")
    
    print("\n6. 시험 예시")
    print(f"   입력: {hex_code}")
    print(f"   Binary: {result['binary_code']}")
    print(f"   nixbpe: {result['nixbpe']}")
    print(f"   해석: n=1,i=1 -> Simple, p=1 -> PC-relative")
    print(f"   displacement: {result['disp_decimal']} (>= 2048이면 2의 보수 필요)")
    
    print("\n" + "=" * 60)
