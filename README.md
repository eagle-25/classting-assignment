# Classting Server
이 서버는 '학교소식 뉴스피드' 서비스를 위한 서버입니다. 

학교 소식을 발행하거나, 구독한 학교의 소식을 모아보는 기능을 제공합니다.

## 목차 
- [Test Coverage](##Test-Coverage)
- [실행 가이드](#개발-환경)
- [API 문서](#API-문서)
- [아키텍처](#아키텍처)
- [개발 가이드](#개발-가이드)


## Test Coverage
테스트 커버리지는 아래 뱃지와 같습니다. 

뱃지를 클릭하시면 코드별로 자세한 커버리지를 확인할 수 있습니다.

[![codecov](https://codecov.io/gh/eagle-25/classting-assignment/graph/badge.svg?token=OJX47V24E3)](https://codecov.io/gh/eagle-25/classting-assignment)

> 💡 테스트 커버리지는 main 브렌치에 푸쉬 발생시 자동으로 업데이트 됩니다. (Github Actions 사용)

### 테스트 작성시 고려한 부분

- 핵심 로직 위주 테스트 작성 (usecase, repo, etc..)
- 외부 의존성 참조 금지
- 빠른 실행 속도
- 멱등성 보장


## 실행 가이드

이 프로젝트는 make 커맨드를 사용해 로컬 환경에서 실행할 수 있습니다.

### 사전 요구사항

- Docker
  - 프로젝트는 docker 기반으로 실행됩니다. 로컬 머신에 docker가 설치되어 있어야 합니다.

### 실행 방법

1. 서버 실행
   
    로컬 환경에서 서버가 실행됩니다. 

    ```bash
    make up
    ```
   > 💡 실행된 서버의 endpoint는 `http://localhost:9001` 입니다. 
2. 테스트 실행
    
    프로젝트의 모든 테스트가 실행됩니다.    
    ```bash
    make test
    ```
3. 린트 실행
    
    python 코드에 대해 린트가 실행됩니다.
    ```bash
    make lint
    ```

   린트는 다음 순서로 실행됩니다.
   - isort: 임포트를 정렬합니다.
   - black: 가독성 향상을 위해 코드를 포맷팅합니다.
   - flake8: 코드 스타일을 검사합니다.
   - mypy: 정적 타입을 검사합니다.

## API 문서

API 문서는 [여기](./docs/APISpecs.md)에서 확인할 수 있습니다.

## 아키텍처

프로젝트의 아키텍처에 대해 소개합니다.

### Hexagonal Architecture
프로젝트의 아키텍처는 Clean Architecture의 한 종류인 Hexagonal Architecture 기반으로 개발되었습니다.

Hexagonal Architecture는 도메인의 핵심 로직과 외부 의존성을 분리하여 도메인 로직의 테스트와 유지보수를 쉽게 할 수 있도록 합니다.

프로젝트의 각 바운디드 컨텍스트(user, school, subscription)는 다음 구조로 헥사고널 아키텍처를 구현합니다.

<img width="1084" alt="image" src="https://github.com/eagle-25/classting-assignment/assets/110667795/64e612d5-98ae-476a-a397-3fa0ceef6089">


### Bounded Contexts

프로젝트는 DDD에 기반하여 다음과 같이 관심사를 Bounded Context로 나누었습니다.

**1. Users**
   
분리 이유: 사용자는 최상위 엔티티입니다. 다른 Bonded Context로부터 영향을 받으면 안되기 때문에 분리했습니다.

   - 사용자 생성, 조회, 수정, 삭제
   - 사용자 인증
   

**2. Schools**

분리 이유: 학교 관리에 집중하기 위해 분리합니다. 소식은 학교의 하위 개념이므로 학교에 포함합니다.

 - 학교 생성, 조회, 수정
 - 학교 소식 발행 


**3. Subscription**

분리 이유: 학교 구독과, 구독한 학교 소식을 조회하는 기능에 집중하기 위해 분리했습니다.

 - 학교 소식 구독
 - 구독한 학교 소식 조회

> 🤔 **고민 지점**
> <br>
> <br>
> 구독한 학교의 소식을 조회하는 기능은 별도의 Bounded Context로 분리해야 할지 고민되었습니다. 이 기능은 NewsFeed와 관련성이 더 크다고 생각했기 때문입니다.
> <br>
> <br>
> 그러나, 조회 기능 1개만을 위해 새로운 Bounded Context를 만드는 것은 비효율적이라 판단했습니다. 또한, `구독한 학교들의 소식 조회`는 Subscription의 하위 기능으로도 불 수 있다 판단해 Subscription Bounded Context에 포함시켰습니다.
> <br>
> <br>
> 만약 해당 기능이 복잡해지거나, NewsFeed 관련 기능이 더 많아진다면 NewsFeed Bounded Context로 분리할 수 있겠습니다. 

> 💡 **DDD 사용 이유**
> 1. 업무 분담
>     - 개발자들은 DDD를 통해 업무 분담을 쉽게 할 수 있습니다. 각 Bounded Context에 대해 독립적으로 개발할 수 있기 때문입니다.
> 2. 유지보수
>     - DDD를 사용하면 코드의 유지보수가 쉬워집니다. 코드의 변경이 한 Bounded Context에만 영향을 미치기 때문입니다.


## 개발 가이드

프로젝트의 개발 환경 구축 및 사용에 대해 소개합니다.

### 사전 요구사항

로컬 머신에 아래 의존성이 설치되어 있으면 개발을 시작할 수 있습니다.

- Docker
- Python (3.11 이상)
- Poetry (Python 패키지 매니저)

### 최초 설정
프로젝트의 루트 디렉터리에서 다음 커맨드를 실행합니다. poetry가 설치되지 않았다면 `pip install poetry`로 설치합니다.

아래 커맨드는 lint 실행을 위해 필요한 의존성을 설치합니다.

 ```bash
poetry install
 ```

### 개발 도구

프로젝트의 개발에 사용되는 도구는 다음과 같습니다.

1. test-watch
  
    코드가 변경되면 모든 테스트를 다시 실행합니다. 테스트 주도 개발에 유용합니다.
   ``` bash
   make test-watch
   ```

2. pre-commit

    코드 커밋 전에 린트를 실행합니다. pre-commit이 통과해야 코드를 커밋할 수 있습니다. 
    
   > 💡 make lint로 린트를 수동으로 실행한 후, 커밋하면 많은 시간을 절약할 수 있습니다.


3. 의존성 관리 (Poetry)

   이 프로젝트는 poetry를 통해 의존성을 관리하고 있습니다.

   ```bash
    poetry add <package-name> # 의존성 추가
    poetry remove <package-name> # 의존성 제거
    ```

