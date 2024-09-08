from sklearn.neighbors import KNeighborsClassifier

class FishClassifier:
    def __init__(self, neighbors=5):
        # 데이터 초기화
        self.fish_data = []
        self.fish_target = []
        self.neighbors = neighbors
        
        # KNN 모델 초기화
        self.kn = KNeighborsClassifier(n_neighbors=self.neighbors)

    def add_initial_data(self):
        # 초기 데이터 입력받기
        length = float(input("물고기의 길이를 입력하세요: "))
        weight = float(input("물고기의 무게를 입력하세요: "))

        # 초기 정답 설정
        if length + weight > 30:
            answer = '도미'
        else:
            answer = '빙어'
        print(f"이 녀석은 바로 {answer}")

        # 정답 입력받기
        answer = input("정답을 입력하세요: ")

        for _ in range(self.neighbors):
            # 초기 데이터 추가
            self.fish_data.append([length, weight])
            self.fish_target.append(answer)

        # 모델 학습
        self.kn.fit(self.fish_data, self.fish_target)

    def fit_and_predict(self):
        length = float(input("물고기의 길이를 입력하세요: "))
        weight = float(input("물고기의 무게를 입력하세요: "))
        
        # 입력받은 데이터를 예측
        predict = self.kn.predict([[length, weight]])[0]
        
        print(f"이 녀석은 바로 {predict}")
        
        # 정답 입력받기
        answer = input("정답을 입력하세요: ")
        
        # 새로운 데이터 추가
        self.fish_data.append([length, weight])
        self.fish_target.append(answer)

        # 모델 다시 학습
        self.kn.fit(self.fish_data, self.fish_target)

    def run(self):
        self.add_initial_data()
        # 반복적으로 입력받기
        while True:
            self.fit_and_predict()
            finish = input("나가기를 원하면 'exit'를 입력하세요: ")
            if finish.lower() == "exit":
                break

# 프로그램 실행
fish_classifier = FishClassifier()
fish_classifier.run()
