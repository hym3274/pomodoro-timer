import flet as ft
import time
import threading
import pygame

current_seconds = 1500
current_break_seconds = 0
lap = 0
bgm = "study1.mp3"
pygame.mixer.init()
pygame.mixer.music.load(bgm) 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
tips_list = [
    "「ポモドーロ」とは、トマトを意味し、トマト型のタイマーで測られていたことが由来です",
    "ポモドーロテクニックとは25分集中、5分休憩を繰り返すサイクルです。(Tipsは五分ごとに更新されます)",
    "52分集中し、17分休憩をとる52-17テクニックも存在するようです",
    "4週ほどしたら長めの休憩をとることをお勧めします"
    ]
def main(page: ft.Page):
    page.title = "ポモドーロタイマー"
    timer_text = ft.Text(value=0, size=70, weight=ft.FontWeight.BOLD)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    global current_seconds
    global current_break_seconds
    global tip_text_control
    global visiblebbutton
    global long_break
    global laptext
    laptext = ft.Text("1週目", size=50)
    long_break = ft.ElevatedButton(text="長休憩をとる",visible=False)
    visiblebbutton = False
    tip_text_control = ft.Text(value=f"Tips:{tips_list[0]}",size=20)
    


    

    def break_timer():
        global current_break_seconds
        global current_seconds
        global visiblebbutton
        global long_break
        current_break_seconds = 300
        
        visiblebbutton = True
        long_break.on_click = break_timerf
        long_break.visible = True
        while True:
            current_break_seconds -= 1
            mtime = current_break_seconds % 3600 // 60
            stime = current_break_seconds % 60

            timer_text.value = f"休憩時間 {mtime}:{stime:02d}"
            page.update()
            time.sleep(1)
            if current_break_seconds <= 0:
                current_seconds = 1500
                threading.Thread(target=update_timer, daemon=True).start()
                long_break.visible =False
                break

    
    def update_timer():
        global current_seconds
        global current_break_seconds
        global lap
        global laptext
        lap += 1
        laptext.value = f"{lap}週目"
        page.update()
        while True:
            current_seconds -= 1
            htime = current_seconds // 3600
            mtime = current_seconds % 3600 // 60
            stime = current_seconds % 60
            if htime > 0:
                timer_text.value = f"{htime}:{mtime:02d}:{stime:02d}"
            else:
                timer_text.value = f"{mtime}:{stime:02d}"
            page.update()
            time.sleep(1)
            if current_seconds == 11:
                pygame.mixer.music.load("timer1.mp3")
                pygame.mixer.music.play(1)
            elif current_seconds == 4:
                pygame.mixer.music.load("pii.mp3")
                pygame.mixer.music.play(1)
            if current_seconds <=0 :
                pygame.mixer.music.load(bgm)
                pygame.mixer.music.play(-1)
                current_break_seconds = 300
                threading.Thread(target=break_timer, daemon=True).start()
                break
    
    def timer_test(e): #動作確認用
        global current_seconds
        set_seconds = -1488
        current_seconds += set_seconds
        page.update()
    def timer_test2(e):
        global current_break_seconds
        set_seconds = -290
        current_break_seconds += set_seconds
    def break_timerf(e):
        global current_break_seconds
        set_seconds = 1500
        current_break_seconds = set_seconds
        page.update()
        long_break.visible = False
    def tips_updater():
        i = 0
        while True:
            i += 1
            tip_text_control.value = f"Tips: {tips_list[i % len(tips_list)]}"
            page.update()
            time.sleep(300) # 5分ごとに更新

    page.add(
        ft.Column(
        controls=[
            laptext,
            # 1. Row コントロールを Column の子要素として配置
            ft.Row(
                [
                    ft.Icon(ft.Icons.TIMER, size=70),
                    timer_text,
                    long_break,
                    ft.ElevatedButton(text="テスト用", on_click=timer_test),
                    #ft.ElevatedButton(text="テスト用2", on_click=timer_test2),
                    
                ],
                # Row 内の要素を水平方向に中央に配置
                alignment=ft.MainAxisAlignment.CENTER 
            ),

            tip_text_control,
        ],
        
        # Column 内の要素を垂直方向に中央に配置（page.vertical_alignmentと合わせて全体の制御に使用）
        alignment=ft.MainAxisAlignment.CENTER, 
        
        # Column 内の要素を水平方向に中央に配置
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
        spacing=30 # Column の子要素間のスペース
    )
    )

    
    if current_seconds > 0:
        threading.Thread(target=update_timer, daemon=True).start()
    if current_break_seconds > 0:
        threading.Thread(target=break_timer, daemon=True).start()
    threading.Thread(target=timer_test, daemon=True).start()
    threading.Thread(target=timer_test2, daemon=True).start()
    threading.Thread(target=break_timerf, daemon=True).start()
    threading.Thread(target=tips_updater, daemon=True).start()

# ASGI アプリをエクスポート（これを Uvicorn で起動します）
app = ft.app(target=main, export_asgi_app=True)

# ローカルで手動実行したいとき（開発用）
if __name__ == "__main__":
    # 開発時はブラウザで確認できるように起動（ポートは任意）
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)