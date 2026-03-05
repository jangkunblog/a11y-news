---
title: '스크린 리더 사용자를 위한 웹 개발 가이드'
description: '시각 장애인이 사용하는 스크린 리더를 고려한 웹 개발 모범 사례를 소개합니다'
pubDate: 'Mar 03 2026'
heroImage: '../../assets/blog-placeholder-3.jpg'
---

## 스크린 리더란?

스크린 리더(Screen Reader)는 시각 장애인이 컴퓨터와 웹 콘텐츠를 사용할 수 있도록 화면의 텍스트를 음성으로 읽어주거나 점자로 출력하는 보조 기술입니다.

### 주요 스크린 리더

- **NVDA** (Windows, 무료 오픈소스)
- **JAWS** (Windows, 상용)
- **VoiceOver** (macOS/iOS, 내장)
- **TalkBack** (Android, 내장)
- **Narrator** (Windows, 내장)

## 스크린 리더 친화적인 개발 원칙

### 1. 시맨틱 HTML 사용

의미 있는 HTML 요소를 사용하면 스크린 리더가 콘텐츠를 올바르게 해석할 수 있습니다.

```html
<!-- 좋은 예 -->
<header>
  <nav>
    <ul>
      <li><a href="/">홈</a></li>
      <li><a href="/about">소개</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>제목</h1>
    <p>내용...</p>
  </article>
</main>

<footer>
  <p>&copy; 2026 회사명</p>
</footer>
```

```html
<!-- 나쁜 예 -->
<div class="header">
  <div class="nav">
    <div class="link">홈</div>
    <div class="link">소개</div>
  </div>
</div>
```

### 2. 적절한 헤딩 구조

헤딩은 문서의 구조를 나타내며, 스크린 리더 사용자의 주요 탐색 수단입니다.

```html
<h1>페이지 제목</h1>
  <h2>주요 섹션 1</h2>
    <h3>하위 섹션 1-1</h3>
    <h3>하위 섹션 1-2</h3>
  <h2>주요 섹션 2</h2>
    <h3>하위 섹션 2-1</h3>
```

**주의사항:**
- h1은 페이지당 하나만 사용
- 헤딩 레벨을 건너뛰지 말 것 (h2 다음에 h4 사용 금지)
- 스타일링을 위해 헤딩 레벨을 선택하지 말 것

### 3. 대체 텍스트 제공

모든 이미지에는 적절한 대체 텍스트를 제공해야 합니다.

```html
<!-- 정보를 담은 이미지 -->
<img src="chart.png" alt="2026년 1분기 매출 증가 그래프, 전년 대비 15% 상승">

<!-- 장식용 이미지 -->
<img src="decoration.png" alt="">

<!-- 링크 내 이미지 -->
<a href="/home">
  <img src="logo.png" alt="회사명 홈페이지로 이동">
</a>
```

### 4. ARIA 속성 활용

ARIA(Accessible Rich Internet Applications)를 사용하여 추가적인 접근성 정보를 제공할 수 있습니다.

```html
<!-- 랜드마크 역할 -->
<div role="search">
  <label for="search-input">검색</label>
  <input id="search-input" type="text" aria-label="사이트 검색">
</div>

<!-- 상태 표시 -->
<button aria-pressed="true">활성화됨</button>
<button aria-expanded="false">메뉴 펼치기</button>

<!-- 라이브 영역 -->
<div role="alert" aria-live="assertive">
  오류: 비밀번호를 입력해주세요
</div>
```

### 5. 포커스 관리

키보드 사용자와 스크린 리더 사용자는 포커스를 통해 웹을 탐색합니다.

```javascript
// 모달 열릴 때 포커스 이동
function openModal() {
  const modal = document.getElementById('modal');
  modal.style.display = 'block';
  modal.querySelector('h2').focus();
  
  // 이전 포커스 저장
  previousFocus = document.activeElement;
}

// 모달 닫힐 때 포커스 복원
function closeModal() {
  const modal = document.getElementById('modal');
  modal.style.display = 'none';
  
  // 포커스 복원
  if (previousFocus) {
    previousFocus.focus();
  }
}
```

### 6. 링크와 버튼의 명확한 텍스트

```html
<!-- 좋은 예 -->
<a href="/report.pdf">2026년 연간 보고서 다운로드 (PDF, 2.5MB)</a>

<!-- 나쁜 예 -->
<a href="/report.pdf">여기를 클릭하세요</a>
<a href="/more">더 보기</a>
```

### 7. 폼 접근성

```html
<form>
  <label for="email">이메일 주소</label>
  <input 
    type="email" 
    id="email" 
    name="email"
    required
    aria-describedby="email-help"
  >
  <span id="email-help">
    예: user@example.com
  </span>
  
  <div role="alert" aria-live="polite" id="email-error">
    <!-- 오류 메시지가 여기에 동적으로 표시됨 -->
  </div>
</form>
```

## 스크린 리더 테스트 방법

### Windows + NVDA
1. [NVDA 다운로드](https://www.nvaccess.org/)
2. 설치 후 자동 실행
3. 웹사이트 탐색 테스트

### macOS + VoiceOver
1. `Cmd + F5`로 VoiceOver 실행
2. 웹사이트 탐색 테스트
3. `Cmd + F5`로 종료

### 주요 테스트 포인트

- [ ] 모든 콘텐츠가 읽히는가?
- [ ] 헤딩으로 탐색이 가능한가?
- [ ] 이미지 대체 텍스트가 적절한가?
- [ ] 링크/버튼의 목적이 명확한가?
- [ ] 폼 필드에 레이블이 있는가?
- [ ] 오류 메시지가 읽히는가?
- [ ] 모달/다이얼로그에 포커스가 트랩되는가?

## 자주 하는 실수

1. **`<div>`와 `<span>`의 과도한 사용**: 시맨틱 요소 사용
2. **시각적으로만 정보 제공**: 색상만으로 정보 전달 금지
3. **자동 재생되는 오디오**: 사용자 제어 불가능한 소리
4. **건너뛰기 링크 부재**: 반복되는 내비게이션 건너뛰기
5. **키보드 트랩**: 키보드로 빠져나올 수 없는 영역

## 참고 자료

- [WebAIM: Screen Reader User Survey](https://webaim.org/projects/screenreadersurvey9/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [Inclusive Components](https://inclusive-components.design/)

---

*스크린 리더를 고려한 개발은 모든 사용자에게 더 나은 경험을 제공합니다.*
