
import MessageClient from message_client

class MessageClient:
    def __init__(self, root, server_url, poll_seconds=3):
        self.root = root
        self.server_url = server_url.rstrip('/')
        self.poll_seconds = max(2, int(poll_seconds))
        self.last_id = 0
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        if not self.server_url.startswith('https://'):
            raise ValueError('메시지 서버 주소는 https:// 로 시작해야 합니다.')
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _poll_loop(self):
        while self.running:
            try:
                query = urllib.parse.urlencode({'after': self.last_id})
                req = urllib.request.Request(
                    f'{self.server_url}/messages?{query}',
                    headers={'User-Agent': 'ScreenAutomation-MessageClient'}
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = json.loads(response.read().decode('utf-8'))
                for item in data.get('messages', []):
                    msg_id = int(item.get('id', 0))
                    text = str(item.get('message', ''))[:300]
                    if msg_id > self.last_id:
                        self.last_id = msg_id
                        self.root.after(0, self._show_message, text)
            except Exception:
                # 네트워크 오류는 매크로에 영향을 주지 않도록 조용히 재시도
                pass
            for _ in range(self.poll_seconds * 10):
                if not self.running:
                    break
                threading.Event().wait(0.1)

    def _show_message(self, text):
        if not self.running or not self.root.winfo_exists():
            return
        win = tk.Toplevel(self.root)
        win.title('관리자 공지')
        win.geometry('360x170')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        tk.Label(win, text='관리자 공지', font=('맑은 고딕', 13, 'bold')).pack(pady=(18, 8))
        tk.Label(win, text=text, font=('맑은 고딕', 10), wraplength=320, justify='center').pack(padx=16, pady=8, expand=True)
        tk.Button(win, text='확인', command=win.destroy, width=12).pack(pady=(0, 14))
