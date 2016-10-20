# -*- coding: utf-8 -*-
#
# showemptycontacts.py
#
# Выводит пустой экран 'Добавить контакты'.
#

from kivy.lang import Builder


class ShowEmptyScreen(object):
    def show_empty_screen(self, text='', name_screen='add_contact',
                          screen_manager=None, disabled=False, callback=None):
        if not screen_manager:
            screen_manager = self.screen.ids.screen_manager_tab_contacts

        empty_screen = Builder.template(
            'EmptyScreen', image='data/images/contacts.png', text=text
        )
        button_add = Builder.template(
            'ButtonAdd', events_callback=callback, disabled=disabled
        )
        empty_screen.add_widget(button_add)
        self.add_screens(name_screen, screen_manager, empty_screen)

        return empty_screen, button_add

