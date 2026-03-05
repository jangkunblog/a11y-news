---
title: 'WCAG 2.2 주요 변경 사항 정리'
description: 'WCAG 2.2에서 새롭게 추가된 접근성 기준과 변경 사항을 알아봅니다'
pubDate: 'Mar 04 2026'
heroImage: '../../assets/wcag-updates-hero.png'
---

## WCAG 2.2 개요

2023년 10월 5일, W3C가 WCAG(Web Content Accessibility Guidelines) 2.2를 정식 권고안(Recommendation)으로 발표했습니다. WCAG 2.2는 WCAG 2.1을 확장한 버전으로, 9개의 새로운 성공 기준이 추가되었습니다.

## 새로 추가된 성공 기준

### Level A

#### 2.4.11 Focus Not Obscured (Minimum)
- 키보드 포커스가 다른 요소에 의해 완전히 가려지지 않도록 해야 합니다
- 최소한 포커스된 요소의 일부는 보이도록 보장해야 합니다

#### 2.4.12 Focus Not Obscured (Enhanced) 
- Level AAA 기준으로, 포커스된 요소가 전혀 가려지지 않아야 합니다

#### 2.5.7 Dragging Movements
- 드래그 동작으로만 수행 가능한 기능에 대해 대체 수단을 제공해야 합니다
- 클릭, 탭 등 간단한 포인터 동작으로도 동일한 작업을 수행할 수 있어야 합니다

#### 2.5.8 Target Size (Minimum)
- 터치 타겟의 최소 크기를 24x24 CSS 픽셀로 규정합니다
- WCAG 2.1의 2.5.5(44x44픽셀)보다 완화된 기준입니다

### Level AA

#### 3.2.6 Consistent Help
- 도움말 메커니즘이 여러 페이지에 걸쳐 일관된 순서로 표시되어야 합니다

#### 3.3.7 Redundant Entry
- 사용자가 이미 입력한 정보를 다시 입력하도록 요구하지 않아야 합니다
- 자동 완성이나 선택 옵션을 제공해야 합니다

#### 3.3.8 Accessible Authentication (Minimum)
- 인증 과정에서 인지 기능 테스트(예: 비밀번호 암기)를 요구할 경우 대체 방법을 제공해야 합니다

### Level AAA

#### 3.3.9 Accessible Authentication (Enhanced)
- 더 엄격한 기준으로, 인지 기능 테스트를 전혀 요구하지 않아야 합니다

## 실무 적용 시 고려사항

### 1. 포커스 관리 개선
```css
/* 포커스 스타일을 명확하게 표시 */
:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* 고정 헤더로 인해 포커스가 가려지지 않도록 */
:focus {
  scroll-margin-top: 80px;
}
```

### 2. 드래그 대체 수단 제공
드래그 앤 드롭 인터페이스의 경우:
- 키보드로도 같은 작업을 수행할 수 있도록 구현
- 터치 디바이스에서 탭으로도 선택/이동 가능하도록 설계

### 3. 터치 타겟 크기 조정
```css
/* 최소 터치 타겟 크기 보장 */
button, a {
  min-height: 24px;
  min-width: 24px;
  padding: 8px 12px;
}
```

## 마이그레이션 가이드

WCAG 2.1에서 2.2로 전환 시 고려사항:

1. **기존 기준 유지**: WCAG 2.2는 2.1을 대체하는 것이 아니라 확장합니다
2. **점진적 적용**: 새로운 기준을 단계적으로 적용할 수 있습니다
3. **테스트 도구 업데이트**: 접근성 검사 도구가 WCAG 2.2를 지원하는지 확인

## 참고 자료

- [W3C WCAG 2.2 공식 문서](https://www.w3.org/TR/WCAG22/)
- [What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)

---

*WCAG 2.2 준수를 통해 더 많은 사용자에게 접근 가능한 웹을 만들어갑시다.*
