# -*- coding: utf-8 -*-
#
# showformcreatecontact.py
#
# Выводит экран с формой и реализует функции для создания нового контакта.
#

import os
import pickle

from libs.createpreviousportrait import create_previous_portrait
from libs.uix.dialogs import dialog, file_dialog, card

import kivymd.snackbar as Snackbar


class ShowFormCreateContact(object):
    _path_to_avatar = False

    def show_form_create_contact(self, *args):
        '''Выводит на экран форму для создания нового контакта.'''

        self.manager_tab_contacts.current = 'create_contact'
        # <class 'libs.uix.createcontact.CreateContact'>
        self._form_create_contact = \
            self.manager_tab_contacts.current_screen.children[0]

    def choice_avatar_contact(self):
        '''Выводит файловый менеджер для выбора аватара
        и устанавливает его для создаваемого контакта. '''

        def on_select(path_to_avatar):
            dialog_manager.dismiss()
            if os.path.splitext(path_to_avatar)[1] in [
                    '.png', '.jpg',  '.jpeg', '.gif']:

                path_to_dir_image, name_image = os.path.split(path_to_avatar)
                name_image = '{}{}'.format(
                    os.path.splitext(name_image)[0], '.png'
                )
                new_path_to_avatar = '{}/data/contacts/previous/{}'.format(
                    self.directory, name_image
                )
                create_previous_portrait(path_to_avatar, new_path_to_avatar)
                self._path_to_avatar = new_path_to_avatar
                self._form_create_contact.ids.avatar.source = new_path_to_avatar
            else:
                dialog(title=self.title, text=self.data.string_avatar_wrong)

        dialog_manager, file_manager = file_dialog(
            title=self.data.string_lang_select_avatar, path='.',
            filter='files', events_callback=on_select
        )

    def save_info_contact(self):
        '''Сохраняет информацию о новом контакте.'''

        info_contacts = self._read_data()[0]

        name_contact = self._form_create_contact.ids.name_field.text
        number_contact = self._form_create_contact.ids.number_field.text
        mail_contact = self._form_create_contact.ids.email_field.text

        if not self._path_to_avatar:
            self._path_to_avatar = 'data/images/avatar_empty.png'
        if name_contact == '':
            Snackbar.make(self.data.string_lang_input_name_contact)
            return
        if number_contact == '':
            Snackbar.make(self.data.string_lang_input_number_contact)
            return
        if name_contact in self.info_contacts:
            Snackbar.make(
                self.data.string_lang_name_contact_exists.format(name_contact)
            )
            return

        info_contacts[name_contact] = [
            '{}\n{}'.format(number_contact, mail_contact), self._path_to_avatar
        ]
        self._save_data(data=info_contacts)
        self.info_contacts, self.info_groups = self._read_data()
        contact_data = \
            ['{}\n{}'.format(number_contact, mail_contact), self._path_to_avatar]
        self.show_contacts({name_contact: contact_data})
        self._clear_form_create_contact()

    def _clear_form_create_contact(self):
        self._form_create_contact.ids.name_field.text = ''
        self._form_create_contact.ids.number_field.text = ''
        self._form_create_contact.ids.email_field.text = ''
        self._form_create_contact.ids.avatar.source = 'data/images/avatar_empty.png'
        self._path_to_avatar = False

    def _save_data(self, file='contacts.ini', data=None):
        if not data:
            data = {}

        with open('{}/data/contacts/{}'.format(
                self.directory, file), 'wb') as file_contacts:
            pickle.dump(data, file_contacts)

    def _read_data(self):
        with open('{}/data/contacts/contacts.ini'.format(
                self.directory), 'rb') as file_contacts:
            contacts_data = pickle.load(file_contacts)
        with open('{}/data/contacts/groups.ini'.format(
                self.directory), 'rb') as file_contacts:
            groups_data = pickle.load(file_contacts)

        return contacts_data, groups_data

    def _check_existence_contacts(self):
        if not os.path.exists('{}/data/contacts'.format(self.directory)):
            os.mkdir('{}/data/contacts'.format(self.directory))
        if not os.path.exists('{}/data/contacts/previous'.format(self.directory)):
            os.mkdir('{}/data/contacts/previous'.format(self.directory))
        if not os.path.exists('{}/data/contacts/contacts.ini'.format(
                self.directory)):
            self._save_data()
        if not os.path.exists('{}/data/contacts/groups.ini'.format(
                self.directory)):
            self._save_data(file='groups.ini')


