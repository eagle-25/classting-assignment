# API Specs
이 문서는 Classting 서버의 API 명세를 기술합니다.

## 목차
- [/users](##/users)
- [/schools](##/schools)
- [/subscriptions](##/subscriptions)

# 사용자 관리 API

## /users

### 회원가입 API

**API 기본 정보**

| 메서드   | URL            | 출력 포맷 | 설명             |
|-------|----------------|-------|----------------|
| POST | /users/sign-up | json  | 사용자 등록시 사용합니다. |

**Request Body**
```json
{
  "email": "",
  "password": ""
}
```
| 변수명      | 타입     | 필수 여부 | 설명       |
|----------|--------|-------|----------|
| email    | string | Y     | 사용자 이메일  |
| password | string | Y     | 사용자 비밀번호 |

**Response Results**

1. 정상
* 상태 코드: `201`
* Response Body: `null`


2. 중복된 이메일
* 상태 코드: `400`
* Response Body
    ```json
    {
        "code": 2001,
        "msg": "User create failed",
        "detail": "User already exists"
    }
    ```
3. 잘못된 이메일 형식