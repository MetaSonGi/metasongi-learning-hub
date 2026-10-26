# MetaSonGi Learning Hub

한국폴리텍대학의 웹 이러닝을 참고해 나만의 스타일로 직접 만드는 개인 무료 학습 서비스입니다.

## 현재 상태

강좌·차시·완료·퀴즈·관심 태그 필터·SQLite 저장·xAPI 형식 JSON 내보내기를 구현했습니다. 개인 로컬 서비스이며 로그인·다중 사용자·공식 LRS는 후속 범위입니다. 자동 테스트 3개와 HTTP 검사를 통과했습니다.

## 빠른 실행

```bash
python app.py
```

실행 절차·제한: [RUN.md](RUN.md) · 검증 기록: [VALIDATION.md](VALIDATION.md)

## 전체 개발 로드맵 (최종 목표)
- [ ] 강좌·차시·동영상·문서·퀴즈와 진도 관리
- [ ] LMS 기능: 수강·과제·평가·수료 기준
- [ ] LXP 기능: 관심 주제와 목표별 학습 경로
- [ ] xAPI 이벤트 설계와 LRS 연동
- [ ] 개인 대시보드와 무료 기본 학습 기능

## 개발 순서
1단계: 예제 강좌와 로컬 학습 화면 → 2단계: 로그인·진도·퀴즈 → 3단계: 학습 경로 → 4단계: LRS와 외부 VR 실습 연동.

## 설계와 프로젝트 경계
LMS는 학습 관리 플랫폼, LXP는 학습 탐색·경험 플랫폼, xAPI는 학습 경험 기록 표준입니다. xAPI는 LMS의 대체 플랫폼이 아니며 기록은 LRS에 저장합니다. 무료 기본 서비스와 로컬 개발을 목표로 하되 호스팅·저장공간·AI 사용 비용은 별도 검토합니다. 폴리텍 공식 서비스가 아니며 학교 코드·상표·강의 콘텐츠를 복제하지 않습니다. 학습자 개인정보와 접근 권한은 서버에서 관리합니다.

## 비교 및 참고 사이트
- 폴리텍 PLISM: https://e-poly.kopo.ac.kr/
- LMS — Moodle: https://docs.moodle.org/502/en/Features_tour
- LMS — Canvas: https://www.instructure.com/canvas
- LXP — Degreed: https://degreed.com/experience/lxp/
- xAPI 명세: https://github.com/adlnet/xAPI-Spec
- LRS 구현 참고: https://github.com/adlnet/ADL_LRS

제품별 제공 기능과 이용 조건은 도입 시 공식 문서에서 다시 확인합니다.
