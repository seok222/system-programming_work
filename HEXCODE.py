def analyze_hex_code(hex_code):
    """
    HEX 코드를 분석하여 여러 형태로 변환하는 함수
    
    Args:
        hex_code (str): 분석할 HEX 코드 (예: "032600")
    
    Returns:
        dict: 분석 결과를 담은 딕셔너리
    """
    
    print(f"🔍 HEX 코드 '{hex_code}' 분석을 시작합니다...")
    print("=" * 50)
    
    # ===========================================
    # 1단계: HEX → Binary 변환
    # ===========================================
    print("📊 1단계: HEX를 Binary로 변환")
    print(f"   입력: {hex_code} (16진법)")
    
    # HEX를 정수로 변환 (16진법 → 10진법)
    decimal_value = int(hex_code, 16)
    print(f"   중간: {decimal_value} (10진법)")
    
    # 정수를 2진법으로 변환하고 24비트로 맞춤
    binary_code = bin(decimal_value)[2:].zfill(24)
    print(f"   결과: {binary_code} (2진법, 24비트)")
    print()
    
    # ===========================================
    # 2단계: Opcode 추출 (상위 6비트)
    # ===========================================
    print("🔧 2단계: Opcode 추출")
    print(f"   Binary 코드: {binary_code}")
    print(f"   상위 6비트: {binary_code[:6]} (Opcode 부분)")
    
    # 상위 6비트가 opcode (명령어 코드)
    opcode_binary = binary_code[:6]
    opcode_hex = hex(int(opcode_binary, 2))[2:].upper().zfill(2)
    print(f"   Opcode: {opcode_binary} (2진법) → {opcode_hex} (16진법)")
    print()
    
    # ===========================================
    # 3단계: nixbpe 플래그 분석 (비트 6-11)
    # ===========================================
    print("🚩 3단계: nixbpe 플래그 분석")
    print(f"   Binary 코드: {binary_code}")
    print(f"   비트 6-11: {binary_code[6:12]} (nixbpe 플래그)")
    
    # nixbpe 플래그 분석 (비트 6-11)
    nixbpe_bits = binary_code[6:12]
    n_bit = int(nixbpe_bits[0])  # indirect addressing
    i_bit = int(nixbpe_bits[1])  # immediate addressing
    x_bit = int(nixbpe_bits[2])  # indexed addressing
    b_bit = int(nixbpe_bits[3])  # base-relative addressing
    p_bit = int(nixbpe_bits[4])  # PC-relative addressing
    e_bit = int(nixbpe_bits[5])  # extended format
    
    print(f"   n={n_bit} (indirect), i={i_bit} (immediate), x={x_bit} (indexed)")
    print(f"   b={b_bit} (base-rel), p={p_bit} (PC-rel), e={e_bit} (extended)")
    print()
    
    # ===========================================
    # 4단계: 어드레싱 모드 및 포맷 결정
    # ===========================================
    print("🎯 4단계: 어드레싱 모드 및 포맷 결정")
    
    # 어드레싱 모드 결정 (n, i 비트 조합)
    if n_bit == 1 and i_bit == 1:
        addressing_mode = "SIC/XE, Simple"
        print(f"   n=1, i=1 → {addressing_mode}")
    elif n_bit == 1 and i_bit == 0:
        addressing_mode = "Indirect"
        print(f"   n=1, i=0 → {addressing_mode}")
    elif n_bit == 0 and i_bit == 1:
        addressing_mode = "Immediate"
        print(f"   n=0, i=1 → {addressing_mode}")
    else:
        addressing_mode = "SIC Standard"
        print(f"   n=0, i=0 → {addressing_mode}")
    
    # Format 결정 (e 비트)
    format_type = "Format 4" if e_bit == 1 else "Format 3"
    print(f"   e={e_bit} → {format_type}")
    
    # Addressing type 결정 (b, p 비트)
    if p_bit == 1:
        addr_type = "PC-relative"
        print(f"   p=1 → {addr_type}")
    elif b_bit == 1:
        addr_type = "Base-relative"
        print(f"   b=1 → {addr_type}")
    else:
        addr_type = "Direct"
        print(f"   b=0, p=0 → {addr_type}")
    print()
    
    # ===========================================
    # 5단계: Displacement/Address 추출 (하위 12비트)
    # ===========================================
    print("📍 5단계: Displacement/Address 추출")
    print(f"   Binary 코드: {binary_code}")
    print(f"   하위 12비트: {binary_code[12:]} (displacement)")
    
    # 하위 12비트가 displacement/address
    disp_bits = binary_code[12:]
    disp_decimal = int(disp_bits, 2)
    disp_hex = hex(disp_decimal)[2:].upper().zfill(3)
    print(f"   Displacement: {disp_bits} (2진법) → {disp_decimal} (10진법) → {disp_hex} (16진법)")
    print()
    
    # ===========================================
    # 6단계: Target Address 계산 (PC-relative)
    # ===========================================
    print("🎯 6단계: Target Address 계산")
    
    # 실제 환경에서는 현재 실행 위치에 따라 달라짐
    import random
    # 현실적인 프로그램 영역 (0x1000~0x5000 사이)
    pc_value = random.choice([0x1000, 0x2000, 0x3000, 0x4000, 0x5000])
    print(f"   현재 PC 값: 0x{pc_value:X} (프로그램 실행 위치)")
    
    if p_bit == 1:  # PC-relative
        print(f"   PC-relative 어드레싱 모드 감지")
        print(f"   계산: Target Address = PC + displacement")
        
        # 2의 보수 처리 (12비트에서 음수 체크)
        if disp_decimal >= 2048:  # 2^11 = 2048
            print(f"   displacement가 2048 이상 → 음수로 처리")
            target_address = pc_value + (disp_decimal - 4096)  # 2^12 = 4096
            print(f"   계산: 0x{pc_value:X} + ({disp_decimal} - 4096) = 0x{target_address:X}")
        else:
            print(f"   displacement가 2048 미만 → 양수로 처리")
            target_address = pc_value + disp_decimal
            print(f"   계산: 0x{pc_value:X} + {disp_decimal} = 0x{target_address:X}")
    else:
        print(f"   Direct 어드레싱 → displacement가 곧 주소")
        target_address = disp_decimal
        print(f"   Target Address = 0x{target_address:X}")
    print()
    
    # ===========================================
    # 7단계: Register A 값 설정 (현재 실행 상태)
    # ===========================================
    print("💾 7단계: Register A 값 (현재 누산기 상태)")
    
    # 실제 실행 상태에 따라 다양한 값을 가질 수 있음
    # 일반적인 계산 결과나 데이터 처리 값들
    possible_values = [0x50000, 0x75000, 0x103000, 0x200000, 0x45000]
    register_a = random.choice(possible_values)
    print(f"   Register A = 0x{register_a:X} (이전 계산 결과에 따라 달라짐)")
    print()
    
    print("✅ 분석 완료! 결과를 정리합니다...")
    print("=" * 50)
    
    return {
        'hex_input': hex_code.upper(),
        'binary_code': binary_code,
        'opcode': opcode_hex,
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
    """분석 결과를 깔끔하게 출력하는 함수"""
    
    print("=" * 50)
    print("HEX 코드 분석 결과")
    print("=" * 50)
    
    print(f"Hex 입력    : {result['hex_input']}")
    print(f"Binary      : {result['binary_code']}")
    print(f"Opcode      : {result['opcode']}")
    print(f"nixbpe      : {result['nixbpe']} (n={result['flags']['n']} i={result['flags']['i']} x={result['flags']['x']} b={result['flags']['b']} p={result['flags']['p']} e={result['flags']['e']})")
    print(f"Flag bit    : {result['flag_description']}")
    print(f"disp/addr   : {result['disp_addr']}")
    print(f"Target Address = 0x{result['target_address']} (PC: 0x{result['pc_value']} + 0x{result['disp_addr']})")
    print(f"Register A value = 0x{result['register_a']}")

# 메인 실행 부분
if __name__ == "__main__":
    # 예제 HEX 코드 분석
    hex_code = "032600"
    
    print("HEX 코드 분석기")
    print("-" * 30)
    
    # 분석 실행
    result = analyze_hex_code(hex_code)
    
    # 결과 출력
    print_analysis(result)
    
    print("\n" + "=" * 50)
    print("단계별 분석 과정:")
    print("=" * 50)
    print("1. HEX -> Binary 변환")
    print(f"   {hex_code} -> {result['binary_code']}")
    print("\n2. Opcode 추출 (상위 6비트)")
    print(f"   {result['binary_code'][:6]} -> {result['opcode']}")
    print("\n3. nixbpe 플래그 분석 (비트 6-11)")
    print(f"   {result['nixbpe']} -> n={result['flags']['n']}, i={result['flags']['i']}, x={result['flags']['x']}, b={result['flags']['b']}, p={result['flags']['p']}, e={result['flags']['e']}")
    print("\n4. Displacement/Address 추출 (하위 12비트)")
    print(f"   {result['binary_code'][12:]} -> {result['disp_addr']} (십진수: {result['disp_decimal']})")
    print("\n5. Target Address 계산")
    print(f"   PC-relative 방식: PC(0x{result['pc_value']}) + displacement(0x{result['disp_addr']}) = 0x{result['target_address']}")
    print(f"   * PC값은 현재 프로그램 실행 위치에 따라 달라집니다")
    print(f"   * Register A값은 이전 계산 결과에 따라 달라집니다")
