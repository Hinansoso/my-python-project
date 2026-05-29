from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel # 이 도구가 꼭 import 되어 있어야 합니다!
import uvicorn

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>RETRO PROFILE 199X</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DungGeunMo&display=swap" rel="stylesheet">
    <style>
        /* [디자인 영역] 전체를 고전 게임기처럼 꾸밉니다 */
        body {
            background-color: #111; color: #39ff14; /* 검은 배경에 네온 그린 글씨 */
            font-family: 'DungGeunMo', 'Press Start 2P', monospace;
            text-align: center; margin: 0; padding: 20px;
            overflow-x: hidden;
        }
        
        .arcade-screen {
            border: 4px solid #39ff14; padding: 30px;
            max-width: 600px; margin: 0 auto;
            box-shadow: 0 0 20px #39ff14, inset 0 0 20px #39ff14; /* 빛나는 효과 */
            background-color: #0a0a0a; position: relative;
        }

        h1 { font-size: 2.5rem; text-shadow: 2px 2px #ff0055; margin-bottom: 10px; }
        .blink-text { animation: blink 1s step-end infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* 프로필 정보 박스 */
        .info-box {
            border: 2px dashed #ff0055; padding: 15px; margin: 20px 0;
            text-align: left; font-size: 1.2rem; line-height: 1.8;
            background: rgba(255, 0, 85, 0.1);
        }
        .highlight { color: #00ffff; }

        /* 방명록(TMI) 영역 */
        .tmi-container { border-top: 2px solid #39ff14; padding-top: 20px; margin-top: 30px; }
        .tmi-list { text-align: left; list-style-type: "> "; padding-left: 20px; font-size: 1.1rem; }
        .tmi-list li { margin-bottom: 10px; color: #fff; }

        /* 레트로 입력창과 버튼 */
        .input-group { margin-top: 20px; display: flex; gap: 10px; }
        input[type="text"] {
            flex: 1; padding: 10px; font-family: 'DungGeunMo';
            background: black; color: #39ff14; border: 2px solid #39ff14; font-size: 1.1rem;
        }
        input[type="text"]:focus { outline: none; background: #222; }
        button.retro-btn {
            padding: 10px 20px; font-family: 'DungGeunMo'; font-size: 1.1rem;
            background: #39ff14; color: black; border: none; cursor: pointer; font-weight: bold;
        }
        button.retro-btn:hover { background: #fff; color: black; }

        /* 장난감 버튼 (파티클 발생기) */
        .danger-btn {
            margin-top: 30px; padding: 10px 15px;
            background: red; color: white; border: 4px solid darkred;
            font-family: 'DungGeunMo'; cursor: pointer; font-size: 1rem;
            box-shadow: 3px 3px 0px darkred; transition: transform 0.1s;
        }
        .danger-btn:active { transform: translate(3px, 3px); box-shadow: none; }

        /* 파티클 애니메이션 요소 */
        .particle {
            position: absolute; width: 10px; height: 10px;
            pointer-events: none; border-radius: 50%;
        }
    </style>
</head>
<body>

    <div class="arcade-screen" id="screen">
        <h1>PLAYER 1</h1>
        <p class="blink-text">INSERT COIN TO START...</p>

        <div class="info-box">
            <div>NAME: <span id="val-title" class="highlight">LOADING...</span></div>
            <div>AGE: <span id="val-age" class="highlight">??</span></div>
            <div>CLASS: <span id="val-tier" class="highlight">LOADING...</span></div>
        </div>

        <div class="tmi-container">
            <h3>[ MESSAGE LOGS ]</h3>
            <ul class="tmi-list" id="tmi-list">
                <li>SYSTEM: 대기 중...</li>
            </ul>
            
            <div class="input-group">
                <input type="text" id="tmi-input" placeholder="여기에 텍스트 입력..." autocomplete="off">
                <button class="retro-btn" onclick="sendTMI()">ENTER</button>
            </div>
        </div>

        <button class="danger-btn" onclick="explodeParticles(event)">버튼을 누르지 마시오</button>
    </div>

    <script>
        // [1] 페이지 로딩 시 내 정보(GET) 가져오기
        async function fetchProfile() {
            try {
                // 주의: 백엔드에 이 주소가 구현되어 있어야 합니다!
                const res = await fetch('/api/my_profile');
                const data = await res.json();
                
                document.getElementById('val-title').innerText = data.title;
                document.getElementById('val-age').innerText = data.age;
                document.getElementById('val-tier').innerText = data.algorithm_tier;
                
                // TMI 리스트 그리기
                renderTMI(data.tmis);
            } catch (e) {
                console.log("백엔드 서버와 아직 연결되지 않았습니다.");
            }
        }

        // TMI 목록을 HTML로 그려주는 헬퍼 함수
        function renderTMI(tmiArray) {
            const listObj = document.getElementById('tmi-list');
            listObj.innerHTML = '';
            if(!tmiArray || tmiArray.length === 0) {
                listObj.innerHTML = '<li>아직 등록된 로그가 없습니다.</li>';
                return;
            }
            tmiArray.forEach(tmi => {
                listObj.innerHTML += `<li>${tmi}</li>`;
            });
        }

        // [2] 방문자가 쓴 글 보내기 (POST)
        async function sendTMI() {
            const inputBox = document.getElementById('tmi-input');
            const text = inputBox.value;
            if (!text) return;

            // 주의: 백엔드에 이 주소와 POST 처리가 구현되어 있어야 합니다!
            await fetch('/api/tmi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: text })
            });

            inputBox.value = '';
            
            // 글을 새로 썼으니, 업데이트된 정보를 다시 불러와서 화면을 고칩니다.
            fetchProfile(); 
        }

        // 페이지 켜지면 실행
        window.onload = fetchProfile;

        // [3] 의미 없는 장난감 기능: 파티클 폭발!
        function explodeParticles(e) {
            const screen = document.getElementById('screen');
            const colors = ['#ff0055', '#39ff14', '#00ffff', '#ffff00'];
            
            for(let i=0; i<30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                particle.style.left = e.clientX + 'px';
                particle.style.top = e.clientY + 'px';
                document.body.appendChild(particle);

                const angle = Math.random() * Math.PI * 2;
                const velocity = 50 + Math.random() * 100;
                const tx = Math.cos(angle) * velocity;
                const ty = Math.sin(angle) * velocity;

                particle.animate([
                    { transform: `translate(0,0) scale(1)`, opacity: 1 },
                    { transform: `translate(${tx}px, ${ty}px) scale(0)`, opacity: 0 }
                ], { duration: 600 + Math.random() * 400, easing: 'ease-out' });

                setTimeout(() => particle.remove(), 1000);
            }
        }
    </script>
</body>
</html>
"""

# 1. 데이터 검증을 위한 가방(클래스) 만들기
class TMICreate(BaseModel):
    content: str

# 2. 내 프로필 데이터 창고
profile = {
    "title": "저를 소개합니다!",
    "age": "22",
    "algorithm_tier": "Gold V",
    "tmis": [] # 리스트가 꼭 있어야 합니다.
}

# 3. 라우터 설정
@app.get("/")
async def main():
    return HTMLResponse(content=html_content)

@app.get("/api/my_profile")
async def get_profile():
    return profile # 프로필 딕셔너리를 그대로 뱉어냅니다.

@app.post("/api/tmi")
async def tmi(tmi: TMICreate):
    # 가방(tmi) 안의 내용물(.content)을 꺼내서 리스트에 추가합니다.
    profile["tmis"].append(tmi.content)
    return {"message": "성공"}

# (터미널 대신 실행 버튼으로 켜기 위한 코드)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.1", port=8000, reload=True)