from abc import ABC, abstractmethod

# 1. 최상위 부모 추상 클래스
class Semiconductor(ABC):
    def __init__(self, name, process_nm, power):
        self.name = name          # 모델명
        self.process_nm = process_nm  # 공정 (nm)
        self.power = power        # 소비전력 (W)

    @abstractmethod
    def get_description(self):
        """자식 클래스에서 각자의 물리적 특성을 기술하도록 강제"""
        pass


# 2. 중간 부모 클래스 1: 시스템 반도체
class SystemSemiconductor(Semiconductor):
    def __init__(self, name, process_nm, power, cores):
        super().__init__(name, process_nm, power)
        self.cores = cores

    @abstractmethod
    def execute_compute(self, data_size):
        """연산 반도체들의 다형성을 위한 추상 메서드"""
        pass


# 3. 중간 부모 클래스 2: 메모리 반도체
class MemorySemiconductor(Semiconductor):
    def __init__(self, name, process_nm, power, transfer_speed):
        super().__init__(name, process_nm, power)
        self.transfer_speed = transfer_speed  # GB/s

    @abstractmethod
    def access_data(self, data_size):
        """메모리 반도체들의 다형성을 위한 추상 메서드"""
        pass


# 4. 최하위 구체적 자식 클래스들 (상속 및 오버라이딩)
class CPU(SystemSemiconductor):
    def get_description(self):
        return f"직렬 연산 및 제어에 최적화된 고클럭 CPU ({self.cores} Cores)"

    def execute_compute(self, data_size):
        # CPU는 코어당 성능이 좋지만 대량 병렬엔 불리 (데이터당 가중치 높음)
        return (data_size * 0.5) / self.cores


class GPU(SystemSemiconductor):
    def get_description(self):
        return f"대규모 그래픽 및 행렬 연산에 최적화된 고병렬 GPU ({self.cores} Cores)"

    def execute_compute(self, data_size):
        # GPU는 대량 데이터 병렬 처리에 매우 유리 (코어 수로 나눔)
        return (data_size * 0.05) / (self.cores * 0.1)


class DRAM(MemorySemiconductor):
    def get_description(self):
        return f"휘발성 고속 메인 메모리 (대역폭: {self.transfer_speed} GB/s)"

    def access_data(self, data_size):
        # 주 기억장치: 매우 빠름
        return data_size / self.transfer_speed


class SSD(MemorySemiconductor):
    def get_description(self):
        return f"비휘발성 대용량 보조저장장치 (대역폭: {self.transfer_speed} GB/s)"

    def access_data(self, data_size):
        # 보조 기억장치: 상대적으로 느림
        return (data_size / self.transfer_speed) * 5  # 물리적 탐색 지연 가중치


# --- 가상 시스템 빌더 및 실행부 ---
class ComputerSystem:
    """상속받은 객체들을 조합하여 하나의 시스템을 만드는 클래스 (Composition)"""
    def __init__(self, processor: SystemSemiconductor, memory: MemorySemiconductor):
        self.processor = processor  # 다형성 덕분에 CPU, GPU 모두 수용 가능
        self.memory = memory        # 다형성 덕분에 DRAM, SSD 모두 수용 가능

    def run_benchmark(self, data_size):
        print(f"\n🖥️ [시스템 구성 분석]")
        print(f" - 연산 장치: {self.processor.name} | {self.processor.get_description()}")
        print(f" - 메모리 장치: {self.memory.name} | {self.memory.get_description()}")
        
        # 다형성(Polymorphism) 호출: 어떤 객체가 연결되었느냐에 따라 알아서 다른 메서드가 실행됨
        mem_time = self.memory.access_data(data_size)
        comp_time = self.processor.execute_compute(data_size)
        total_time = mem_time + comp_time
        
        print(f"⏳ 데이터 접근 시간: {mem_time:.4f}초")
        print(f"⚡ 순수 연산 처리 시간: {comp_time:.4f}초")
        print(f"🏆 총 벤치마크 소요 시간: {total_time:.4f}초")
        return total_time


# --- 사용자 선택 인터페이스 ---
def main():
    # 미리 부모 클래스를 상속받아 정의해 둔 반도체 '객체 수영장(Pool)'
    processors = [
        CPU("Intel Core i7", process_nm=7, power=125, cores=16),
        GPU("NVIDIA RTX 4090", process_nm=4, power=450, cores=16384)
    ]
    
    memories = [
        DRAM("Samsung DDR5", process_nm=12, power=1.2, transfer_speed=64),
        SSD("SK Hynix NVMe", process_nm=16, power=5.0, transfer_speed=7)
    ]

    print("=" * 50)
    print("      상속과 다형성 기반 반도체 조합 시뮬레이터      ")
    print("=" * 50)

    # 1. 프로세서 선택 (상속 관계 확인용)
    print("\n[단계 1] 연산 처리 반도체(SystemSemiconductor)를 선택하세요.")
    for i, p in enumerate(processors):
        print(f" {i+1}. {p.name} ({p.__class__.__name__})")
    p_idx = int(input("선택 (번호 입력): ")) - 1

    # 2. 메모리 선택 (상속 관계 확인용)
    print("\n[단계 2] 저장/메모리 반도체(MemorySemiconductor)를 선택하세요.")
    for i, m in enumerate(memories):
        print(f" {i+1}. {m.name} ({m.__class__.__name__})")
    m_idx = int(input("선택 (번호 입력): ")) - 1

    # 3. 작업량 입력
    print("\n[단계 3] 처리할 대규모 데이터 셋의 크기를 입력하세요.")
    data_size = float(input("데이터 크기 (추천: 1000 ~ 50000): "))

    # 4. 조합된 객체로 시스템 가동 (OOP의 핵심: 다형성 구현)
    selected_processor = processors[p_idx]
    selected_memory = memories[m_idx]

    my_computer = ComputerSystem(selected_processor, selected_memory)
    my_computer.run_benchmark(data_size)

if __name__ == "__main__":
    main()