ScreenAutomation 메시지 시스템 (공지 텍스트 전용)

구성
- server.py: Render에 배포할 Flask 서버
- Admin.py: 관리자 전송 GUI
- message_client.py: 기존 ScreenAutomation에 넣을 수신 모듈

1) 서버 배포
- GitHub 새 저장소에 server.py, requirements.txt, render.yaml을 올립니다.
- Render에서 New > Blueprint로 저장소를 연결합니다.
- 환경변수 ADMIN_TOKEN을 길고 임의의 값으로 설정합니다. 이 값은 관리자 PC에서만 사용합니다.
- 배포 후 https://...onrender.com 주소를 확인합니다.

2) 관리자 프로그램
- Admin.py의 GUI에서 서버 주소와 ADMIN_TOKEN을 입력해 메시지를 보냅니다.
- 빌드: python -m PyInstaller --noconfirm --clean --onefile --windowed --name Admin Admin.py
- 관리자 토큰을 친구에게 배포하는 파일이나 코드에 넣지 마세요.

3) 친구용 프로그램 연결
- message_client.py를 기존 auto_macro_fuck_RE.py와 같은 폴더에 둡니다.
- 아래 통합 안내를 따라 MessageClient를 생성하고 시작합니다.
- SERVER_URL에는 배포한 HTTPS 주소를 넣습니다. 수신자는 관리자 인증 토큰이 필요 없습니다.

4) 보안/동작 범위
- 이 시스템은 공지 텍스트만 전달합니다. 원격 명령, 파일 실행, 키보드/마우스 입력, 화면 감시 기능은 없습니다.
- 메시지는 서버에 임시 메모리로 저장되며 서버가 재시작되면 초기화됩니다.
- 서버는 마지막 200개 메시지만 유지합니다. 새로 설치한 클라이언트는 실행 시점 이후 메시지를 받아오도록 last_id를 초기화하는 기능을 추가할 수 있습니다.
- 공개 수신 엔드포인트이므로 서버 주소를 아는 사용자는 공지를 읽을 수 있습니다. 민감한 내용은 보내지 마세요.
