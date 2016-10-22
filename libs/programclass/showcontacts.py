# -*- coding: utf-8 -*-
#
# contacts.py
#
# Выводит список и кнопку для добавления нового контакта.
#

from kivy.lang import Builder

from libs.uix.contactslist import ContactsList
from libs.uix.callcontact import CallContact
from libs.uix.lists import Lists, RightButton
from libs.uix.dialogs import dialog, card

import kivymd.snackbar as Snackbar


class ShowContacts(object):
    _contacts_items = None

    def show_contacts(self, info_contacts):
        '''
        :type info_contacts: dict;
        :param info_contacts: {
            'Name contact': ['Number contact\nMail contact', 'path/to/avatar']
        };

        '''
        if not self._contacts_items:
            # Создаем список контактов.
            self._contacts_list = ContactsList()
            self._contacts_items = Lists(
                dict_items=info_contacts, flag='three_list_custom_icon',
                right_icons=self.data.right_icons,
                events_callback=self._event_contact_item
            )

            button_add_contact = Builder.template(
                'ButtonAdd', disabled=False,
                events_callback=self.show_form_create_contact
            )
            self._contacts_list.add_widget(self._contacts_items)
            self._contacts_list.add_widget(button_add_contact)
            self.add_screens(
                'contact_list', self.manager_tab_contacts, self._contacts_list
            ) 
        else:
            # Добавляет контакт к существующему списку
            # и выводит список на экран.
            self._add_contact_item(info_contacts)
            self.manager_tab_contacts.current = 'contact_list'

    def _event_contact_item(self, *args):
        '''События пункта списка контактов.'''

        def end_call():
            self.screen.current = 'root_screen'

        instanse_button = args[0]
        if type(instanse_button) == RightButton:
            name_contact, name_event = instanse_button.id.split(', ')
            if name_event == 'call':
                self.screen.current = 'call_contact'
                data_contact = self.info_contacts[name_contact]
                call_screen = self.screen.current_screen.children[0]
                call_screen.name_contact = name_contact
                call_screen.number_contact = data_contact[0].split('\n')[0]
                call_screen.avatar = data_contact[1]
                call_screen.callback = end_call
            elif name_event == 'groups':
                self._show_names_groups(name_contact)
        else:
            name_contact, name_event = args

    def _show_names_groups(self, name_contact):
        '''Выводит на экран окно со списком групп.'''

        def get_choice_group(name_group):
            groups_list.dismiss()
            self._add_contact_in_group(name_contact, name_group)

        if not self.info_groups.__len__():
            Snackbar.make(self.data.string_lang_list_groups_empty)
            return
        groups_list = \
            [[name_group, 'accounts'] for name_group in self.info_groups.keys()]
        groups_list = Lists(
            list_items=groups_list, events_callback=get_choice_group,
            flag='single_list_icon'
        )
        groups_list = card(groups_list, self.data.string_lang_add_in_group)

    def _add_contact_item(self, info_contacts):
        self._contacts_items.three_list_custom_icon(info_contacts)
