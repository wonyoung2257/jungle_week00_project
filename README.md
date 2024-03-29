# 0주차 jungle wordle

# jungle wordle

정글 0주차 프로젝트 22.3.28 - 22.3.31(3인)

---

## 프로젝트 개요

> 정글에 입소한 동료들의 이름을 wordle이라는 게임을 통해 쉽게 외울 수 있게 하기위한 프로젝트
> 

## 게임 화면
![image](https://user-images.githubusercontent.com/54197518/183526742-fa798160-b51c-4743-af44-3f84ca3c6bbd.png)


## 핵심기능

### 워들 게임 로직

- 정답 적중시 : 녹색
- 정답 포함시 : 황색
- 정답 미포함시: 회색
- 기본적으로 정답과 위치가 일치하면 녹색, 정답에 포함되면 노란색, 정답에 포함되어 있지 않다면 회색으로 표시된다. 그리고 사용자가 정답을 맞히게 되면 정답 모달 창이 나오게 되고 6번의 기회를 모두 사용하여 실패하면 실패 모달창이 나오게 된다.

### 명예의 전당

- 플레이어의 정답을 맞춘 수를 기준으로 순위를 메긴다.
- jinja2를 사용하여 데이터를 서버에서 받아 렌더링 시킴

## 개발시 어려웠던 점

### 자음 모음 분리해서 받기

한글의 경우 글자 입력에서 하나의 글자가 명확하게 끝나다는 구분을 하기가 쉽지 않았다. 그렇기 때문에 유저가 입력한 값을 자음과 모음을 분리해서 입력 받는 것에 있어서 어려움이 있었다.

### 시도한 방법

1. input의 maxlength를 1로 제한하기
    - 한글자만 입력을 받을 수 있었으나 영어와 다르게 한글은 ㄱ, 가, 각 등 자음과 모음이 합쳐진 단어 모두가 length가 1이란 문제가 있었다.
2. 키보드 이벤트로 분리하기
    - keyup 이벤트 발생시 다음 focus로 이동시키는 방법으로 분리 시도
    - 사용자가 키보드를 동시에 입력하면 자음과 모음이 함께 나오는 문제 발생
3. 자음 모음 함께 들어온 글자 강제로 분리 후 자음만 입력
    - 사용자가 동시에 입력하여 자음과 모음이 함께 들어오면 모음을 분리하고 자음만을 남기게 만듬
    - 정상 동작은 하나 모음 데이터가 날아가 유저에게 불편한 경험을 제공

→ 2번과 3번을 함께하는 것이 최선이라고 판단하여 2과 3번을 함께 적용하여 구현

## 기술 스택

### Front-end

- HTML, Css, JS, jQuery

### Back-end

- Flask
