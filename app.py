from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import os


# ---------- LOAD DUMP ----------

def load_dump():

    path = "/storage/emulated/0/Download/dump.txt"
    skins = []

    if not os.path.exists(path):
        return skins

    with open(path, encoding="utf-8") as f:
        for line in f:
            p = [x.strip() for x in line.split("|")]
            if len(p) >= 3:
                skins.append((p[1], p[2]))

    return skins


# ---------- APP ----------

class SkinApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.skins = load_dump()
        self.cache = [(h, n, n.lower()) for h, n in self.skins]

        self.target = None
        self.ihave = None
        self.pairs = []

        screen = MDScreen()

        main = MDBoxLayout(
            orientation="vertical",
            spacing=10
        )

        # -------- TOP BAR --------

        top = MDTopAppBar(
            title="BGMI Skin Builder",
            elevation=4
        )

        main.add_widget(top)

        # -------- TARGET CARD --------

        target_card = MDCard(
            padding=15,
            radius=[25, 25, 25, 25],
            size_hint_y=None,
            height=120
        )

        self.target_field = MDTextField(
            hint_text="Search TARGET Skin"
        )

        self.target_field.bind(text=self.filter_target)

        target_card.add_widget(self.target_field)

        main.add_widget(target_card)

        # -------- TARGET LIST --------

        self.target_list = MDList()
        ts = MDScrollView()
        ts.add_widget(self.target_list)
        main.add_widget(ts)

        # -------- IHAVE CARD --------

        ihave_card = MDCard(
            padding=15,
            radius=[25, 25, 25, 25],
            size_hint_y=None,
            height=120
        )

        self.ihave_field = MDTextField(
            hint_text="Search I HAVE Skin"
        )

        self.ihave_field.bind(text=self.filter_ihave)

        ihave_card.add_widget(self.ihave_field)

        main.add_widget(ihave_card)

        # -------- IHAVE LIST --------

        self.ihave_list = MDList()
        isv = MDScrollView()
        isv.add_widget(self.ihave_list)
        main.add_widget(isv)

        # -------- RESULT CARD --------

        result_card = MDCard(
            padding=15,
            radius=[30, 30, 30, 30],
            size_hint_y=0.4
        )

        result_card.add_widget(
            MDLabel(text="Selected Skins", bold=True)
        )

        self.result_list = MDList()
        rscroll = MDScrollView()
        rscroll.add_widget(self.result_list)

        result_card.add_widget(rscroll)

        main.add_widget(result_card)

        # -------- FLOAT ADD BUTTON --------

        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": .9, "center_y": .1}
        )

        fab.bind(on_release=self.add_pair)

        screen.add_widget(main)
        screen.add_widget(fab)

        return screen

    # ---------- TARGET SEARCH ----------

    def filter_target(self, instance, value):

        if hasattr(self, "target_event"):
            self.target_event.cancel()

        self.target_event = Clock.schedule_once(
            lambda dt: self.perform_target(value), 0.3
        )

    def perform_target(self, text):

        self.target_list.clear_widgets()

        if not text:
            return

        text = text.lower()

        for h, n, nl in self.cache:

            if text in nl:

                self.target_list.add_widget(
                    OneLineListItem(
                        text=n,
                        on_release=lambda x, a=h, b=n: self.select_target(a, b)
                    )
                )

    # ---------- IHAVE SEARCH ----------

    def filter_ihave(self, instance, value):

        if hasattr(self, "ihave_event"):
            self.ihave_event.cancel()

        self.ihave_event = Clock.schedule_once(
            lambda dt: self.perform_ihave(value), 0.3
        )

    def perform_ihave(self, text):

        self.ihave_list.clear_widgets()

        if not text:
            return

        text = text.lower()

        for h, n, nl in self.cache:

            if text in nl:

                self.ihave_list.add_widget(
                    OneLineListItem(
                        text=n,
                        on_release=lambda x, a=h, b=n: self.select_ihave(a, b)
                    )
                )

    # ---------- SELECT ----------

    def select_target(self, h, n):
        self.target = (h, n)

    def select_ihave(self, h, n):
        self.ihave = (h, n)

    # ---------- ADD PAIR ----------

    def add_pair(self, *args):

        if not self.target or not self.ihave:
            return

        t_hex, t_name = self.target
        h_hex, h_name = self.ihave

        self.pairs.append((t_hex, h_hex))

        self.result_list.add_widget(
            OneLineListItem(
                text=f"[color=ff5555]{h_name}[/color] >> [color=55ff55]{t_name}[/color]",
                markup=True
            )
        )

        self.target = None
        self.ihave = None


SkinApp().run()
