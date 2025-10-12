# Backend

## API

| 기능         | Endpoint                          | Method   |
| ---------- | --------------------------------- | -------- |
| 로그인        | `/api/users/login`                | `POST`   |
| 핀 생성하기     | `/api/pins`                       | `POST`   |
| 전체 핀 조회    | `/api/pins`                       | `GET`    |
| 핀 상세보기     | `/api/pins/:pinId`                | `POST`   |
| 핀 검색하기(제목) | `/api/pins/search?search=keyword` | `POST`   |
| 핀 수정하기     | `/api/pins/:pinId`                | `PUT`    |
| 핀 삭제하기     | `/api/pins/:pinId`                | `DELETE` |
| 핀 즐겨찾기     | `/api/pins/:pinId/likes`          | `PUT`    |
| 댓글 등록      | `/api/pins/:pinId/comments`       | `POST`   |
| 댓글 불러오기    | `/api/pins/:pinId/comments`       | `GET`    |
| 댓글 수정      | `/api/pins/comments/:commentId`   | `PUT`    |
| 댓글 삭제      | `/api/pins/comments/:commentId`   | `DELETE` |
| 프로필 Page   | `/api/user/:userId`               | `GET`    |
| 작성한 핀      | `/api/user/:userId/pins`          | `GET`    |
| 즐겨찾기한 핀    | `/api/users/:userId/likes`        | `GET`    |
| 프로필 수정     | `/api/users/:userId`              | `PUT`    |

## Git Commit Message 7가지 규칙

1. 제목과 본문을 **빈 행으로 구분**한다.
2. 제목은 **50글자** 이내로 제한한다.
3. 제목의 **첫 글자는 대문자**로 작성한다.
4. 제목 끝에는 **마침표를 넣지 않는다**.
5. 제목은 **명령문**으로 사용하며 **과거형을 사용하지 않는다**.
6. 본문의 **각 행은 72글자 내**로 제한한다.
7. 어떻게 보다는 **무엇과 왜를 설명**한다.

### 커밋 메시지 구조

```text
// Header, Body, Footer는 빈 행으로 구분한다.
타입: 주제(제목) // Header(헤더)

본문 // Body(바디)

바닥글 // Footer
```

* **Header**: **필수**
* **타입**: 해당 커밋의 성격

| 타입 이름    | 내용                               |
| -------- | -------------------------------- |
| feat     | 새로운 기능에 대한 커밋                    |
| fix      | 버그 수정에 대한 커밋                     |
| build    | 빌드 관련 파일 수정 / 모듈 설치 또는 삭제에 대한 커밋 |
| chore    | 그 외 자잘한 수정에 대한 커밋                |
| ci       | ci 관련 설정 수정에 대한 커밋               |
| docs     | 문서 수정에 대한 커밋                     |
| style    | 코드 스타일 혹은 포맷 등에 관한 커밋            |
| refactor | 코드 리팩토링에 대한 커밋                   |
| test     | 테스트 코드 수정에 대한 커밋                 |
| perf     | 성능 개선에 대한 커밋                     |

- **Body**: **상세 내용**, **생략 가능**
- **Footer**: **참조 정보 추가**, **생략 가능**
