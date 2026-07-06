import random
import time

#최상위 부모 클래스 정의-------------------------------------------
class Semiconductor:
    def __init__(self, name, process_nm, power):
        self.name = name #반도체 제품명
        self.process_nm = process_nm #공정 미세도
        self.power = power #소비 전력

    #반도체 별 소개 정보
    def get_description(self):
        pass


#중간 부모 클래스 정의---------------------------------------------
#시스템반도체 정의
class SystemSemiconductor(Semiconductor):
    def __init__(self, name, process_nm, power, cores):
        super().__init__(name, process_nm, power)
        self.cores = cores #코어 수

    def execute_compute(self, data_size): #연산 기능 
        pass

#메모리 반도체 정의
class MemorySemiconductor(Semiconductor):
    def __init__(self, name, process_nm, power, transfer_speed):
        super().__init__(name, process_nm, power)
        self.transfer_speed = transfer_speed #전송 속도

    def access_data(self, data_size): #데이터 접근 기능
        pass


#최하위 자식 클래스 정의-------------------------------------------
#시스템 반도체 상속 CPU 정의
class CPU(SystemSemiconductor):
    def get_description(self): #설명
        return f"복잡한 제어 및 범용 연산용 CPU (공정: {self.process_nm}nm, 코어: {self.cores}개)"

    def execute_compute(self, data_size): #범용 연산 특성을 고려해 코어 수로 나누는 시간 계산
        return (data_size * 0.4) / self.cores

#시스템 반도체 상속 GPU 정의
class GPU(SystemSemiconductor):
    def get_description(self): #설명
        return f"대규모 행렬 및 그래픽 병렬 연산용 GPU (공정: {self.process_nm}nm, 코어: {self.cores}개)"

    def execute_compute(self, data_size): #병렬 연산 특성 고려해 가중치로 구현
        return (data_size * 0.08) / (self.cores * 0.05)

#시스템 반도체 상속 NPU 정의
class NPU(SystemSemiconductor): 
    def get_description(self): #설명
        return f"AI 딥러닝 추론 특화 가속기 NPU (공정: {self.process_nm}nm, 코어: {self.cores}개)"

    def execute_compute(self, data_size): #AI 행렬 연산 고려해 높은 가중치 적용
        return (data_size * 0.01) / (self.cores * 0.2)

#메모리 반도체 상속 DRAM 정의
class DRAM(MemorySemiconductor):
    def get_description(self): #설명
        return f"주기억장치 일반 범용 DRAM (대역폭: {self.transfer_speed} GB/s)"

    def access_data(self, data_size): #데이터 접근 시간 계산
        return data_size / self.transfer_speed

#메모리 반도체 상속 HBM 정의
class HBM(MemorySemiconductor):
    def get_description(self): #설명
        return f"실리콘 관통 전극(TSV) 기반 초고속 고대역폭 메모리 HBM (대역폭: {self.transfer_speed} GB/s)"

    def access_data(self, data_size): #수직 적층 구조 특성 고려해 가중치 적용
        return data_size / (self.transfer_speed * 1.5)

#메모리 반도체 상속 SSD 정의
class SSD(MemorySemiconductor):
    def get_description(self): #설명
        return f"비휘발성 대용량 보조저장장치 NVMe SSD (대역폭: {self.transfer_speed} GB/s)"

    def access_data(self, data_size): #탐색 지연이 존재하는 특성 고려해 가중치 적용
        return (data_size / self.transfer_speed) * 4


#시스템 조립 및 벤치마크-------------------------------------------
#시스템 조립 클래스 정의
class ComputerSystem:
    def __init__(self, processor: SystemSemiconductor, memory: MemorySemiconductor):
        self.processor = processor #연산 장치 객체 조립, 보관
        self.memory = memory #저장 장치 객체 조립, 보관

    def run_benchmark(self, data_size): #벤치마크 테스트 수행
        print(f"\n" + "="*60)
        print(f"🖥️ [가상 시스템 빌드 완료 및 하드웨어 분석]")
        print(f" └ [연산] {self.processor.name} -> {self.processor.get_description()}")
        print(f" └ [메모리] {self.memory.name} -> {self.memory.get_description()}")
        print(f" " + "-"*56)
        
        #반도체 스펙 기반 전력 효율성 점수 계산
        efficiency_score = int((100 / self.processor.process_nm) * (100 / self.processor.power) * 10)
        
        mem_time = self.memory.access_data(data_size) #데이터 접근 시간 계산
        comp_time = self.processor.execute_compute(data_size) #연산 처리 시간 계산
        total_time = mem_time + comp_time #총 처리 시간 합산
        
        print(f" ⏳ 데이터 로드 시간    : {mem_time:.4f} 초")
        print(f" ⚡ 순수 연산 처리 시간 : {comp_time:.4f} 초")
        print(f" 🏆 최종 시스템 처리 속도: {total_time:.4f} 초")
        print(f" 🍃 예상 아키텍처 전력 효율성 점수: {efficiency_score}점")
        print(f"==" * 30)
        return total_time


#실행부-----------------------------------------------------------
def main():  #프로그램 실행 함수
    #시스템 반도체 객체 생성
    processors = [  
        CPU("Intel Core i5 (보급형)", process_nm=10, power=65, cores=6),  
        CPU("AMD Ryzen 9 (최고급형)", process_nm=4, power=170, cores=16),  
        GPU("NVIDIA RTX 4060 (메인스트림)", process_nm=5, power=115, cores=3072),  
        GPU("NVIDIA H100 (AI 서버용)", process_nm=4, power=700, cores=18432),
        NPU("Apple Neural Engine (모바일)", process_nm=3, power=15, cores=16),  
        NPU("Google TPU v5e (클라우드)", process_nm=5, power=175, cores=128)  
    ] 
    
    #메모리 반도체 객체 생성
    memories = [  
        DRAM("Samsung DDR4 8GB", process_nm=18, power=1.2, transfer_speed=25),  
        DRAM("SK Hynix DDR5 16GB", process_nm=12, power=1.1, transfer_speed=64),  
        HBM("Samsung HBM3E 24GB", process_nm=10, power=15.0, transfer_speed=1228),  
        HBM("SK Hynix HBM4 초고속형", process_nm=5, power=20.0, transfer_speed=2048),  
        SSD("Crucial SATA SSD", process_nm=20, power=3.5, transfer_speed=0.5),  
        SSD("Samsung NVMe M.2 SSD", process_nm=14, power=6.0, transfer_speed=7.5)  
    ]  

    print("=" * 60)
    print("      🚀 다중 상속 계층 기반 반도체 커스텀 매칭 시뮬레이터 🚀      ")
    print("=" * 60) 

    
    while True:  #오류 시 재입력 받기 위한 무한 루프 생성
        print("\n[단계 1] 연산 처리 반도체(SystemSemiconductor) 목록")  
        for i, p in enumerate(processors):  
            print(f" [{i+1}] {p.name:<28} | 타입: {p.__class__.__name__:<4}")   
        
        try:  
            p_idx = int(input(" ➔ 장착할 프로세서 번호 입력: ")) - 1  
            if 0 <= p_idx < len(processors):  
                break  
            else:  
                print(f"❌ 에러: 1부터 {len(processors)} 사이의 번호만 입력할 수 있습니다. 다시 시도하세요.") 
        except ValueError: 
            print("❌ 에러: 문자가 아닌 '숫자(정수)'를 정확히 입력해야 합니다. 다시 시도하세요.")

    while True:  #오류 시 재입력 받기 위한 무한 루프 생성
        print("\n[단계 2] 저장/메모리 반도체(MemorySemiconductor) 목록")  
        for i, m in enumerate(memories):  
            print(f" [{i+1}] {m.name:<28} | 타입: {m.__class__.__name__:<4}")  
        
        try:  
            m_idx = int(input(" ➔ 장착할 메모리 번호 입력: ")) - 1  
            if 0 <= m_idx < len(memories): 
                break 
            else:  
                print(f"❌ 에러: 1부터 {len(memories)} 사이의 번호만 입력할 수 있습니다. 다시 시도하세요.")  
        except ValueError: 
            print("❌ 에러: 문자가 아닌 '숫자(정수)'를 정확히 입력해야 합니다. 다시 시도하세요.")  

  
    while True:  
        print("\n[단계 3] 처리할 부하 데이터 용량(MB)을 입력하세요.")  
        try: 
            data_size = float(input(" ➔ 데이터 용량 입력 (추천: 500 ~ 10000): ")) 
            if data_size > 0:  
                break  
            else:  
                print("❌ 에러: 데이터 용량은 0보다 큰 양수여야 합니다. 다시 시도하세요.")
        except ValueError: 
            print("❌ 에러: 유효한 숫자(실수/정수)를 입력해야 합니다. 다시 시도하세요.") 

    selected_processor = processors[p_idx]
    selected_memory = memories[m_idx] 

    my_computer = ComputerSystem(selected_processor, selected_memory)  #매칭된 객체들로 가상 본체 조립
    my_computer.run_benchmark(data_size)  #벤치마크 테스트 시작


if __name__ == "__main__":  #프로그램이 직접 실행될 때만 main() 함수 호출
    main()