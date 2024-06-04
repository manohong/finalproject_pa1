# 2019310615 홍마노

# Reference

[1] https://github.com/Winter091/MarioPygame "MarioPygame"

[2] https://github.com/pygame/pygame "pygame"

[3] https://www.pngegg.com/en/png-wplps#google_vignette "Mario.png"

# 지원 Operating Systems 및 실행 방법

## 지원 Operating Systems

| OS      | 지원 여부 |
| ------- | --------- |
| windows | :o:       |
| Linux   | :o:       |
| MacOS   | :o:       |

## 실행 방법

### Windows

1. python3.12를 설치

2. powershell 창에서 아래 pip3 library를 설치

```
pip3 install pygame
```

3. 재부팅 이후 python main.py를 실행하면 게임 창이 뜨면서 실행

### Linux

1. python을 설치

```
sudo apt update
sudo apt install python3 python3-pip
```

2. pygame을 설치

```
pip3 install pygame
```

3. 해당디렉토리에서 게임을 실행한다.

```
python3 main.py
```

### MacOS

1. homebrew를 설치

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

```

2. python3 설치

```
brew install python
```

3. pygame을 설치

```
pip3 install pygame
```

4. 해당디렉토리에서 게임을 실행한다.

```
python3 main.py
```

# 실행 예시

<span style="color:red">1.게임 시작 후 마리오를 잡아당겨 발사</span>

<span style="color:red">2.마리오가 벽돌을 맞출 시 알파벳 등장</span>

<span style="color:red">3.알파벳을 조합하여 단어를 유추한 후 enter키 => 정답일시 게임종료화면</span>

![게임 실행 영상-1](https://github.com/manohong/finalproject_pa1/assets/164157143/03d5136f-8a92-4932-ab7d-daf67819ceed)

![게임 실행 영상-2](https://github.com/manohong/finalproject_pa1/assets/164157143/33e1fe0f-b506-4083-8dc0-949aaadcd003)

# 코드 설명

## main.py

## game.py

### class FallingAlphabetGame:

- Description : 전체적인 게임을 관리하는 클래스
  1. Def **init** : 모든ui, 폰트크기, 화면 크기 초기화
  2. Def reset_game : 게임 재실행시 객체 초기화
  3. Def load_assets : obstacles와 map크기를 불러옴
  4. Def handle_event : 마리오 발사 기능, 알파벳 입력 및 정답확인 기능, 게임 재실행 기능을 담음
  5. Def update : 마리오 클래스의 update함수 사용
  6. Def draw : 변화하는 ui를 실제로 세팅하는 단계

## mario.py

### class Mario

- Description : 메인 캐릭터의 위치 관련 클래스
  1. Def **init** : 마리오의 이미지를 불러와 위치와 크기 초기화하는 단계
  2. Def reset : 마리오가 발사되어 사라졌을 때 다시 마리오의 위치를 초기값으로 위치
  3. Def update : 마리오가 발사되어 벽돌에 부딪히는 애니메이션 생성

## obstacles.py

### def create_obstacles

- Description : 위치를 고려하여 벽돌을 생성, 벽돌끼리 겹치지 않게 하기,알파벳의 크기가 벽돌보다 클 시 벽돌 수정

## alphabet.py

### class Alphabet

- Description : 게임의 주 컨텐츠인 알파벳의 위치 관련 클래스
  1. Def **init** : 최초 게임시작시 알파벳을 초기화하는 단계, 알파벳의 해당 위치에 해당 외형을 위치하고 바닥으로 떨어지지 않게끔 함
  2. Def update : Alphabet 객체가 화면에서 아래로 떨어지는 동작을 업데이트함, 이때 객체가 바닥이나 벽돌에 닿으면 멈추게 함
  3. Def draw : 알파벳을 그려주는 단계

### def hide_alphabets_behind_obstacles

- Description : 알파벳을 장애물 뒤에 숨길 수 있는 알파벳 위치를 공유하여 alphabet class를 생성 후 class를 보관

### def add_alphabet_line

- Description : user가 알파벳을 입력할 때 화면에 송출

## timer.py

### class Timer

- Description : 게임의 주 컨텐츠인 알파벳의 위치 관련 클래스
  1. Def **init** : 최초 게임시작시 타이머를 초기화하는 단계
  2. Def start : 타이머 시작
  3. Def pause : 타이머 멈춤
  4. Def resume : 타이머 재개
  5. Def stop : 타이머를 끝냄
  6. Def get_elapsed_time : 게임이 끝났을 때 타이머의 시간을 반환

## picture

### block.png

- Description : 알파벳을 보관할 벽돌 사진 파일

### map.png

- Description : 백그라운드 사진 파일

### mario.png

- Description : 캐릭터 사진 파일

## sound

### gameover.wav

- Description : 게임 종료시 나오는 음악

### blockhit.wav

- Description : 벽돌이 부서지고 알파벳이 떨어질 때 나오는 음악

### overworld-fast.wav

- Description : 게임 수행 중 나오는 음악

# TODO List

- 데이터 베이스를 활용한 단어별 유저들 중 최고기록 저장
- ui를 icon을 활용해 디자인 수정
- 일반 장애물뿐 아니라 새로운 유형의 장애물 생성(여러번 마리오로 블락을 부셔야 알파벳이 나옴)
- 화면 비율에 따라 ui 비율에 맞게끔 수정해야함
- 메인 메뉴 추가(메인 메뉴에서 옵션기능을 추가하여 캐릭터(루이지,쿠파등) 교체), 게임 종료 버튼 추가

