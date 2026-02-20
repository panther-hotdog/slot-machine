import tkinter as tk
import random

# アイテムリストと重み
items = ["りんご", "みかん", "ぶどう", "メロン", "スイカ"]
weights = [5, 5, 5, 1, 5]  # メロンだけ低確率

def weighted_choice():
    return random.choices(items, weights=weights, k=1)[0]

# スロット状態管理
state = {"step": 0, "A": None, "B": None, "running": False}

def spin():
    if state["running"]:
        return  # 回転中は無視
    state["running"] = True
    step = state["step"]

    # 回転回数と速度
    count = 0
    max_count = 30

    def update_slot():
        nonlocal count
        if count < max_count:
            if step == 0:  # A回転中
                label_A.config(text=random.choice(items))
            elif step == 1:  # B回転中
                label_B.config(text=random.choice(items))
            count += 1
            root.after(50, update_slot)
        else:
            # 最終確定
            if step == 0:
                state["A"] = weighted_choice()
                label_A.config(text=state["A"])
                state["step"] = 1  # 次はB
            elif step == 1:
                # BはAと被らないように
                B_final = state["A"]
                while B_final == state["A"]:
                    B_final = weighted_choice()
                state["B"] = B_final
                label_B.config(text=state["B"])
                state["step"] = 2  # 全て確定
            state["running"] = False

    update_slot()

# GUI設定
root = tk.Tk()
root.title("スロット風2ステップ表示")

# Aラベル
label_A = tk.Label(root, text="---", font=("Arial", 24), width=10, height=2, relief="solid")
label_A.pack(pady=10)

# Bラベル
label_B = tk.Label(root, text="---", font=("Arial", 24), width=10, height=2, relief="solid")
label_B.pack(pady=10)

# スピンボタン
button = tk.Button(root, text="スピン", font=("Arial", 16), command=spin)
button.pack(pady=20)

root.mainloop()