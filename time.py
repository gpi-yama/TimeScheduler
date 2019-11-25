import tkinter as Tk
import time
# import winsound
import os
import datetime
WID = 10


class Timer(Tk.Frame):
    def __init__(self, master=None):
        self.times = {}
        self.ids = 0
        self.minid = 1
        self.end_time = None

        Tk.Frame.__init__(self, master)
        self.master.title('Time scheduler')

        self.tokei = Tk.Label(self, text=u'00:00', font='Arial, 25')
        self.text = Tk.Label(self, text=u'内容', font='Arial, 12')

        b1 = Tk.Button(self, text='Start', command=self.start)
        b2 = Tk.Button(self, text='Reset', command=self.stop)

        b1.grid(row=0, column=0, columnspan=4,
                padx=5, pady=2, sticky=Tk.W+Tk.E)
        b2.grid(row=0, column=4, columnspan=4,
                padx=5, pady=2, sticky=Tk.W + Tk.E)

        self.tokei.grid(row=1, column=2, columnspan=4,
                        padx=5, pady=2, sticky=Tk.W + Tk.E)
        self.text.grid(row=1, column=0, columnspan=2,
                       padx=5, pady=2, sticky=Tk.W + Tk.E)

        add_b = Tk.Button(self, text='Add schedule', command=self.add_schedule)
        add_b.grid(row=2, column=0, columnspan=4,
                   padx=5, pady=2, sticky=Tk.W + Tk.E)

        self.row = 2
        self.add_schedule()

    def add_schedule(self):
        self.row += 1
        self.ids += 1
        self.times[self.ids] = {}
        #frame = Tk.LabelFrame(self, text=u"内容", width=20)
        self.times[self.ids]["label"] = Tk.Label(self, text=u"内容:")
        self.times[self.ids]["text"] = Tk.Entry(self, width=WID)
        self.times[self.ids]["starth"] = Tk.Label(
            self, text=u'時', font='Arial, 12')
        self.times[self.ids]["startm"] = Tk.Label(
            self, text=u'分', font='Arial, 12')
        self.times[self.ids]["endh"] = Tk.Label(
            self, text=u'時', font='Arial, 12')
        self.times[self.ids]["endm"] = Tk.Label(
            self, text=u'分', font='Arial, 12')
        self.times[self.ids]["fromto"] = Tk.Label(
            self, text=u'〜', font='Arial, 12')

        self.times[self.ids]["sh"] = Tk.Spinbox(
            self, from_=0, to=23, increment=1, width=WID)
        self.times[self.ids]["sm"] = Tk.Spinbox(
            self, from_=0, to=59, increment=1, width=WID)
        self.times[self.ids]["eh"] = Tk.Spinbox(
            self, from_=0, to=23, increment=1, width=WID)
        self.times[self.ids]["em"] = Tk.Spinbox(
            self, from_=0, to=59, increment=1, width=WID)

        self.times[self.ids]["label"].grid(
            row=self.row, column=0, padx=5, pady=2, sticky=Tk.W
        )
        self.times[self.ids]["text"].grid(
            row=self.row, column=1, padx=5, pady=2, sticky=Tk.W
        )

        self.times[self.ids]["starth"].grid(
            row=self.row, column=3, padx=5, pady=2, sticky=Tk.W)
        self.times[self.ids]["sh"].grid(
            row=self.row, column=2, padx=5, pady=2)

        self.times[self.ids]["startm"].grid(
            row=self.row, column=5, padx=5, pady=2, sticky=Tk.W)
        self.times[self.ids]["sm"].grid(
            row=self.row, column=4, padx=5, pady=2)

        self.times[self.ids]["fromto"].grid(
            row=self.row, column=6, padx=5, pady=2, sticky=Tk.W)

        self.times[self.ids]["endh"].grid(
            row=self.row, column=8, padx=5, pady=2, sticky=Tk.W)
        self.times[self.ids]["eh"].grid(
            row=self.row, column=7, padx=5, pady=2)

        self.times[self.ids]["endm"].grid(
            row=self.row, column=10, padx=5, pady=2, sticky=Tk.W)
        self.times[self.ids]["em"].grid(
            row=self.row, column=9, padx=5, pady=2)

    def start(self):  # Startを押したときの動作
        self.started = True
        self.set_time()
        self.count()
        self.after(1000, self.start)
        print(self.end_time)

    def count(self):
        if self.started and self.end_time is not None:
            print("count fin")
            now = datetime.datetime.now()
            h = int(self.end_time.hour) - int(now.hour)
            m = int(self.end_time.minute) - int(now.minute)
            t = h * 3600 + m * 60 + (60 - now.second)
            # winsound.PlaySound("SystemAsterisk",winsound.SND_ALIAS) #時間になったらwindowsのみ音で知らせる
            if self.end_time < now:
                self.tokei.config(text="Finish!")
                os.system("afplay /System/Library/Sounds/Ping.aiff -v 10")
                self.after(1000, self.start)
            else:
                print("count", t)
                self.tokei.config(text='%02d:%02d' %
                                  (t / 60, t % 60))  # 表示時間を1秒毎に書き換え
                self.after(1000, self.count)

    def stop(self):  # 停止処理
        self.started = False
        self.tokei.config(text='00:00')

    def get_time(self, id_):
        times = self.times[id_]
        sh = times["sh"].get()
        sm = times["sm"].get()
        eh = times["eh"].get()
        em = times["em"].get()
        txt = times["text"].get()
        return sh, sm, eh, em, txt

    def set_time(self):
        print("set time")
        self.interval = 0
        now = datetime.datetime.now()
        et = None

        for i in range(self.minid, self.ids + 1):
            sh, sm, eh, em, txt = self.get_time(i)
            print(sh, sm, eh, em, txt)
            start_time = datetime.datetime(year=now.year, month=now.month,
                                           day=now.day,
                                           hour=int(sh), minute=int(sm),
                                           second=0, microsecond=0)
            end_time = datetime.datetime(year=now.year, month=now.month,
                                         day=now.day,
                                         hour=int(eh), minute=int(em),
                                         second=0, microsecond=0)
            print("OKOK", end_time, start_time, now)
            if start_time <= now and end_time >= now:
                h = int(eh) - int(sh)
                m = int(em) - int(sm)
                self.now_id = i
                self.end_time = end_time
                self.text.config(text=u"内容:"+txt)
                break
            elif et is not None:
                if et <= now and start_time >= now:
                    h = int(sh) - int(et.hour)
                    m = int(sm) - int(et.minute)
                    self.now_id = i
                    self.interval = h * 3600 + m * 60
                    self.end_time = start_time
                    self.text.config(text=u"内容:休憩 after"+txt)
                    break
            elif start_time >= now:
                self.now_id = i
                self.end_time = start_time
                self.text.config(text=u"内容:休憩, after" + txt)
                break

            et = end_time


if __name__ == '__main__':  # スクリプトファイルとして実行されたとき用
    f = Timer()
    f.pack()
    f.mainloop()
