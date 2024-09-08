# Weekly program no.1 - 자가 학습 KNN
<img src="https://github.com/user-attachments/assets/54bb1109-4a67-4dbb-b714-0893e9c6f420" width=600 />

## 프로그램 동작 방식
- [ ] 학습된 모델이 없는 상태에서 출발
- [ ] 사용자는 길이, 무게 데이터를 입력하고 프로그램을 예측 값을 출력 (이때 프로그램은 학습 데이터가 없어 임의의 값을 예측)
- [ ] 예측값에 대한 정답 유무 입력
- [ ] 프로그램에 입력된 데이터(훈련데이터)와 정답(타겟) 데이터를 저장
- [ ] 위 과정이 반복 되면서 모델을 진화 시켜 나간다.


## usage
```bash
# install
## use git url
$ pip install git+https://github.com/j25ng/knn_j25ng.git
## use pypi
$ pip install knn-j25ng

$ fish
🐟 물고기의 길이를 입력하세요 (cm): 10.8
🐟 물고기의 무게를 입력하세요  (g): 8.7
🐟 이 물고기는 빙어입니다.
🐟 예측이 맞습니까? (y/n): y
🐟 예측 성공🥳
```

## data
```bash
$ cd ~/code/data
$ tree
.
├── data.json
└── target.json

0 directories, 2 files
```
