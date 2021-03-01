import rumps

class PomodoroApp(object):
    def __init__(self):
        self.config = {
            "app_name": "Pomodoro",
            "start": "Bắt Đầu 🏁",
            "pause": "Tạm Dừng ⏸",
            "continue": "Tiếp Tục ▶️",
            "stop": "Dừng Lại 🛑",
            "break_message": "25 phút đã trôi qua! +1 🍅",
            "interval": 1500,
            "reset_round": "Đặt Lại Số Lượt 🍅",
            "work_mode": "Tập Trung 💪",
            "rest_mode": "Giải Lao 💤"
        }
        self.round = 0
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.timer.count = 0
        self.interval = self.config["interval"]
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=None)
        self.set_up_menu()
        self.is_in_mode = self.config["work_mode"]
        self.reset_round_button = rumps.MenuItem(title=self.config["reset_round"], callback=self.reset_round)
        self.mode_button = rumps.MenuItem(title=self.config["rest_mode"], callback= self.rest)
        self.app.menu = [self.start_pause_button, self.stop_button, self.reset_round_button, self.mode_button]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.start_pause_button.title = self.config["start"]
        self.app.title = "Số lượt đã tập trung 🍅: {}".format(self.round)
        self.stop_button.set_callback(None)

    def on_tick(self, sender):
        if self.is_in_mode == self.config["work_mode"]:
            self.stop_button.set_callback(self.stop_timer)
            self.time_left = sender.end - sender.count
            self.mins = self.time_left // 60 if self.time_left >= 0 else (-1 * self.time_left) // 60
            self.secs = self.time_left % 60 if self.time_left >= 0 else (-1 * self.time_left) % 60
            #count up one round and send message at every interval
            if (-1*self.time_left % self.config["interval"]) == 0 and self.time_left <= 0:
                self.round += 1
                rumps.notification(title=self.config["app_name"], subtitle=self.config["break_message"], message='')
            #display seconds
            if self.time_left >=0:
                self.app.title = 'Tập trung 💪 | ▶️ {:2d}:{:02d} | Lượt 🍅: {}'.format(self.mins, self.secs, self.round)
            else:
                self.app.title = 'Tập trung 💪 | ▶️ -{:2d}:{:02d} | Lượt 🍅: {}'.format(self.mins, self.secs, self.round)
        elif self.is_in_mode == self.config["rest_mode"]:
            self.mins = sender.count // 60
            self.secs = sender.count % 60
            self.app.title = 'Giải lao 💤 | {:2d}:{:02d}'.format(self.mins, self.secs, self.round)
        sender.count += 1

    def start_timer(self, sender):
        if sender.title.lower().startswith(("bắt", "tiếp")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()
            if self.time_left >=0:
                self.app.title = 'Tập trung 💪 | ⏸️ {:2d}:{:02d} | Lượt 🍅: {}'.format(self.mins, self.secs, self.round)
            else:
                self.app.title = 'Tập trung 💪 | ⏸️ -{:2d}:{:02d} | Lượt 🍅: {}'.format(self.mins, self.secs, self.round)

    def stop_timer(self, sender):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.set_callback(self.start_timer)
        self.start_pause_button.title = self.config["start"]

    def run(self):
        self.app.run()

    def reset_round(self, sender):
        self.round = 0
        self.set_up_menu()

    def rest(self, sender):
        sender.title = self.config["work_mode"]
        self.mode_button.set_callback(self.work)
        self.is_in_mode = self.config["rest_mode"]
        self.set_up_menu()
        self.reset_round_button.set_callback(None)
        self.stop_button.set_callback(None)
        self.start_pause_button.set_callback(None)
        self.start_timer(self.start_pause_button)
        self.on_tick(self.timer)

    def work(self, sender):
        sender.title = self.config["rest_mode"]
        self.mode_button.set_callback(self.rest)
        self.is_in_mode = self.config["work_mode"]
        self.stop_timer("")
        self.start_pause_button.set_callback(self.start_timer)
        self.reset_round_button.set_callback(self.reset_round)

if __name__ == '__main__':
    app = PomodoroApp()
    app.run()