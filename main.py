from tkinter import *
from tkinter import messagebox
from crawl import *

root = Tk()
root.geometry("450x500")
root.title("アドレスキャッチャー")
root.configure(bg="#edf2f4")

label = Label(root, text="指定したイベント名を持つ全てのアドレスを取得します\n注：空白（スペース）は入れないでください", fg="#2b2d42", bg="#edf2f4")
label.pack()

label = Label(root, text="１．取得するメールの種類を選びます", fg="#2b2d42", bg="#edf2f4")
label.pack()

selectedRadio = IntVar()
selectedRadio.set(1)
Radiobutton(root, text="イベント参加", variable=selectedRadio, value=1, fg="#2b2d42", bg="#edf2f4").pack()
Radiobutton(root, text="イベント出店", variable=selectedRadio, value=2, fg="#2b2d42", bg="#edf2f4").pack()
Radiobutton(root, text="商品出品", variable=selectedRadio, value=3, fg="#2b2d42", bg="#edf2f4").pack()

label = Label(root, text="２．イベント名を入れます", fg="#2b2d42", bg="#edf2f4")
label.pack()

entry = Entry(root, fg="#2b2d42", bg="#edf2b4", insertbackground="black")
entry.pack()

def onFetchButtonClick():
    resultLabel.config(text="")

    enteredEventName = entry.get()

    if enteredEventName.strip() == "":
        resultLabel.config(text="イベント名を入力して下さい")
    elif len(enteredEventName.strip()) <= 4:
        resultLabel.config(text="５文字以上でないと検索できません")
    else:
        label = ''
        if selectedRadio.get() == 1: 
            label = 'EventParticipantRequest' 
        elif selectedRadio.get() == 2: 
            label = 'EventOrganizerRequest'
        elif selectedRadio.get() == 3:
            label = 'ItemForSalesRequest'

        resultMap = crawl(enteredEventName, label)

        if len(resultMap) == 0:
            messagebox.showinfo("結果なし", "結果０件．一件も一致しませんでした")
            resultLabel.config(text="")
            return
        
        messagebox.showinfo("成功！", "完了しました．OKをクリックすると結果がクリップボードにコピーされます")

        resultString = ''
        hitEventTitle = ''
        for key, values in resultMap.items():
            resultString += key + ":\n"
            hitEventTitle += key + "\n"
            for value in values:
                resultString += value + "\n"

        root.clipboard_clear()
        root.clipboard_append(resultString)
        root.update()

        resultLabel.config(text="ヒットしたイベント名：\n\n" + hitEventTitle)

button = Button(root, text="３．クリックします", command=onFetchButtonClick, fg="#2b2d42", bg="#2b2d42", highlightbackground="#edf2f4")
button.pack()

spacer = Label(root, text="", bg="#edf2f4", pady=20)
spacer.pack()

resultLabel = Label(root, text="", fg="#2b2d42", bg="#edf2f4")
resultLabel.pack()

root.mainloop()