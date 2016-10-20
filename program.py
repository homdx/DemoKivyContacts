#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# program.py
#

import os
import sys

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.properties import ObjectProperty

from libs.uix import customsettings
from libs.uix.dialogs import dialog
from libs.uix.startscreen import StartScreen
from libs import programdata as data
from libs import programclass as _class

from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import NavigationDrawer


class NavDrawer(NavigationDrawer):
    events_callback = ObjectProperty()


class Program(App, _class.Plugin, _class.About, _class.License,
              _class.ShowFormCreateContact, _class.ShowContacts,
              _class.ShowEmptyScreen, _class.CreateGroup):
    '''Функционал программы.'''

    settings_cls = customsettings.CustomSettings
    customsettings.TEXT_INPUT = data.string_lang_enter_value
    nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'BlueGrey'  # 'Teal'

    def __init__(self, **kvargs):
        super(Program, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)

        self.window = Window
        self.open_exit_dialog = None
        self.scren_add_groups = None  # kivy.lang.builder.AddContactAddGroups
        self.data = data
        self.current_tab = 'contacts'
        self.load_all_kv_files()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'Русский')
        config.setdefault('General', 'theme', 'default')

    def build_settings(self, settings):
        with open('{}/data/settings/general.json'.format(
                data.prog_path), 'r') as settings_json:
            settings.add_json_panel(data.string_lang_settings, self.config,
                data=settings_json.read().format(
                    language=data.string_lang_setting_language,
                    title=data.string_lang_setting_language_title,
                    desc=data.string_lang_setting_language_desc,
                    russian=data.string_lang_setting_language_russian,
                    english=data.string_lang_setting_language_english))

    def build(self):
        self.use_kivy_settings = False
        self.title = data.string_lang_title  # заголовок окна программы
        self.icon = 'data/images/logo.png'  # иконка окна программы

        self.config = ConfigParser()
        self.config.read('{}/program.ini'.format(data.prog_path))

        # Главный экран программы.
        self.screen = StartScreen(events_callback=self.events_program)
        self.nav_drawer = NavDrawer(title=data.string_lang_menu)

        self.manager_tab_contacts = self.screen.ids.screen_manager_tab_contacts
        self.manager_tab_groups = self.screen.ids.screen_manager_tab_groups

        # Проверяем, присутствует ли файлы контактов.
        self._check_existence_contacts()
        self.info_contacts, self.info_groups = self._read_data()
        self.old_info_groups = self.info_groups

        if self.info_contacts.__len__():  # Activity со списком контактов
            self.show_contacts(self.info_contacts)

        return self.screen

    def events_program(self, *args):
        '''Вызывается при выборе одного из пунктов меню программы.'''

        if len(args) == 2:  # нажата ссылка
            event = args[1]
        else:  # нажата кнопка программы
            try:
                _args = args[0]
                event = _args if isinstance(_args, str) else _args.id
            except AttributeError:  # нажата кнопка девайса
                event = args[1]

        if data.PY2:
            if isinstance(event, unicode):
                event = event.encode('utf-8')

        if event == data.string_lang_settings:
            self.open_settings()
        elif event == data.string_lang_exit_key:
            self.exit_program()
        elif event == data.string_lang_license:
            self.show_license()
        elif event == data.string_lang_plugin:
            self.show_plugins()
        elif event in (1001, 27):
            self.back_screen(event)
        elif event == 'About':
            self.show_about()

        return True

    def back_screen(self, event):
        '''Менеджер экранов.'''

        # Нажата BackKey на главном экране.
        if event in (1001, 27):
            if self.current_tab == 'contacts':
                if self.manager_tab_contacts.current == 'create_contact':
                    if self.manager_tab_contacts.has_screen('contact_list'):
                        self.manager_tab_contacts.current = 'contact_list'
                        self._clear_form_create_contact()
                    else:
                        self.manager_tab_contacts.current = 'empty_contacts_list'
                else:
                    self.exit_program()
                    return

    def exit_program(self, *args):
        def close_dialog():
            self.open_exit_dialog.dismiss()
            self.open_exit_dialog = None

        if self.open_exit_dialog:
            return

        self.open_exit_dialog = dialog(
            text=data.string_lang_exit, title=self.title, dismiss=False,
            buttons=[
                [data.string_lang_yes, lambda *x: sys.exit(0)],
                [data.string_lang_no, lambda *x: close_dialog()]
            ]
        )

    def load_all_kv_files(self):
        directory_kv_files = '{}/libs/uix/kv'.format(self.directory)

        for kv_files in os.listdir(directory_kv_files):
            if kv_files == 'bugreporter.kv':
                continue
            Builder.load_file('{}/{}'.format(directory_kv_files, kv_files))

    def add_screens(self, name_screen, screen_manager, new_screen):
        screen = Screen(name=name_screen)
        screen.add_widget(new_screen)
        screen_manager.add_widget(screen)
        screen_manager.current = name_screen

    def on_tab_press(self, name_tab_press):
        '''Вызывается при переключении TabbedPanel.'''

        self.current_tab = name_tab_press
        self.screen.ids.action_bar.title = self.data.title_bar[name_tab_press]

        if name_tab_press == 'groups':
            self._check_existence_contacts()
            self.info_contacts, self.info_groups = self._read_data()

            if not self.info_groups.__len__():
                if self.manager_tab_groups.current == 'empty_groups_list':
                    self.empty_screen_groups = \
                        self.manager_tab_groups.current_screen.children[0]

                    if not self.info_contacts.__len__():
                        self.empty_screen_groups.ids.float_act_btn.disabled = \
                            True
                    else:
                        self.empty_screen_groups.ids.float_act_btn.disabled = \
                            False
            else:
                self._show_group(self.info_groups)
            if self.info_contacts.__len__() and not self.info_groups.__len__():
                self.empty_screen_groups.ids.label.text = \
                    data.string_lang_not_groups
                self.empty_screen_groups.ids.float_act_btn.disabled = False

    def on_config_change(self, config, section, key, value):
        '''Вызывается при выборе одного из пункта настроек программы.'''

        if key == 'language':
            if not os.path.exists('{}/data/language/{}.txt'.format(
                    self.directory, data.select_locale[value])):
                dialog(
                    text=data.string_lang_not_locale.format(
                        data.select_locale[value]
                    ),
                    title=self.title
                )
                config.set(section, key, data.old_language)

                config.write()
                self.close_settings()

    def on_pause(self):
        '''Ставит приложение на 'паузу' при выхоже из него.
        В противном случае запускает программу по заново'''

        return True

