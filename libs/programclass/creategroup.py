# -*- coding: utf-8 -*-
#
# creategroup.py
#
# Создает новую группу контактов и выводит ее на экран.
#

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

from libs.uix.dialogs import input_dialog
from libs.uix.contactslist import ContactsList
from libs.uix.lists import Lists

from kivymd.accordion import MDAccordionItem
from kivymd.label import MDLabel
import kivymd.snackbar as Snackbar


class NewGroup(FloatLayout):
    pass


class CreateGroup(object):
    _new_group = None
    _contacts_list_in_group = None

    def create_group(self):
        def callback(group_name):
            dialog_group.dismiss()
            if group_name:
                if group_name in self.info_groups:
                    Snackbar.make(
                        self.data.string_lang_group_exists.format(group_name)
                )
                    return
                self.info_groups[group_name] = []
                self._save_data('groups.ini', self.info_groups)
                self._show_group(group_name)

        dialog_group = input_dialog(
            title=self.title, hint_text=self.data.string_lang_name_group,
            text_button_ok='OK', events_callback=callback
        )

    def _show_group(self, groups_data):
        if self.manager_tab_groups.has_screen('groups') and \
                not isinstance(groups_data, str):
            if self.old_info_groups != groups_data:
                self._check_new_add_contact_in_groups(groups_data)
                return
            else:
                # Выводим на экран список групп, если он был ранее создан.
                self.manager_tab_groups.current = 'groups'
                return

        if not self._new_group:
            self._new_group = NewGroup()
        if isinstance(groups_data, str):
            groups_data = {groups_data: []}

        for group_name in groups_data.keys():
            self._create_accordion_item(group_name, groups_data)

        if not self.manager_tab_groups.current or \
                self.manager_tab_groups.current == 'empty_groups_list':
            self.add_screens(
                'groups', self.manager_tab_groups, self._new_group
            )

    def _create_accordion_item(self, group_name, groups_data):
        group_item = MDAccordionItem(
            id=group_name, title=group_name, icon='accounts',
            background_color=self.data.alpha, title_theme_color='Primary'
        )
        scroll = ScrollView(id=group_name)
        contacts_group = self._get_contacts_group(groups_data[group_name])
        scroll.add_widget(contacts_group)
        group_item.add_widget(scroll)
        self._new_group.ids.group.add_widget(group_item)

    def _add_contact_in_group(self, name_contact, group_name):
       '''Добавляет контакт в группу.'''

       if name_contact not in self.info_groups[group_name]:
           self.info_groups[group_name].append(name_contact)
           self._save_data('groups.ini', self.info_groups)
           self.info_contacts, self.info_groups = self._read_data()
           Snackbar.make(
               self.data.string_lang_add_contact_in_group.format(
                   name_contact, group_name
               )
            )

    def _get_contacts_group(self, contacts_group):
        '''Возвращает объект MDLabel - "Контактов нет",
        если контакты в группе отсутствуют или объект со списком
        добавленных в группу контактов.'''

        if not contacts_group.__len__():
            return MDLabel(
                text=self.data.string_lang_not_contacts,
                font_style='Headline', halign='center',
                theme_text_color='Custom',
                text_color=self.data.text_color
            )
        else:
            for contact_name in contacts_group:
                info_contacts = {contact_name: self.info_contacts[contact_name]}
                if not self._contacts_list_in_group:
                    contacts_list = ContactsList()
                    self._contacts_list_in_group = Lists(
                        dict_items=info_contacts, flag='three_list_custom_icon',
                        right_icons=self.data.right_icons[:1],
                        events_callback=self._event_contact_item
                    )
                    contacts_list.add_widget(self._contacts_list_in_group)
                else:
                    self._contacts_list_in_group.three_list_custom_icon(
                        info_contacts
                    )
            self._contacts_list_in_group = None

            return contacts_list

    def _check_new_add_contact_in_groups(self, groups_data):
        '''Проверяет и добавляет в группу новые контакты, если таковые
        были включены в какую-лиюо группу во вкладке "Контакты".'''

        def add_contact_list_in_groups():
            scroll_in_accordion_item = accordion_item.ids.container.children[0]
            label_not_contacts = scroll_in_accordion_item.children[0]
            scroll_in_accordion_item.remove_widget(label_not_contacts)
            contacts_group = self._get_contacts_group(groups_data[group_name])
            scroll_in_accordion_item.add_widget(contacts_group)

        for accordion_item in self._new_group.ids.group.children:
            for group_name in groups_data.keys():
                contacts_name_in_group = groups_data[group_name]
                if group_name == accordion_item.id:
                    for contact_name in contacts_name_in_group:
                        if group_name in self.old_info_groups:
                            if contact_name not in self.old_info_groups[group_name]:
                                accordion_content = \
                                    accordion_item.ids.container.children[0].children[0]
                                if type(accordion_content) == ContactsList:
                                    contacts_list_in_group = \
                                        accordion_content.children[0]
                                    info_contacts = \
                                        {contact_name: self.info_contacts[contact_name]}
                                    contacts_list_in_group.three_list_custom_icon(
                                        info_contacts
                                    )
                                else:
                                    add_contact_list_in_groups()
                        else:
                            add_contact_list_in_groups()

        self.old_info_groups = groups_data

