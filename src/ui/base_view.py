import flet as ft
from application.app import App
from data.table_classes import TableColumn
from typing import TypeAlias, Dict, Callable


FieldDict: TypeAlias = Dict[TableColumn, ft.TextField]


class BaseItem(ft.Container):
    def __init__(
        self,
        values: dict[TableColumn, str | int | float],
        display_values: list[str],
        on_click_function: Callable[[ft.Container], None],
    ):
        super().__init__()

        self.values = values

        self.content = ft.Row(
            [
                ft.Text(value, size=16, expand=1, text_align=ft.TextAlign.CENTER)
                for value in display_values
            ]
        )
        self.padding = 10
        self.border_radius = 8
        self.ink = True
        self.on_click = lambda e: on_click_function(self)


class BaseView(ft.Column):
    def __init__(
        self,
        app: App,
        search_bar_label: str,
        lv_header_labels: tuple[str, ...],
        add_fields: FieldDict,
        add_column_layout: ft.Column,
        update_fields: FieldDict,
        update_column_layout: ft.Column,
        db_table_columns: tuple[TableColumn, ...],
    ):
        """Base view for Product and Client"""
        super().__init__()

        self.app = app

        # --- SEARCH BAR ---
        self.search_bar = ft.TextField(
            label=search_bar_label,
            icon=ft.Icons.SEARCH,
            on_change=lambda e: self.update_list_view(),
        )
        self.search_bar_display = ft.Container(
            content=self.search_bar,
            margin=ft.margin.only(top=10),
        )

        # --- LIST VIEW ---
        self.lv_header = ft.Row(
            controls=[
                ft.Text(
                    label,
                    size=16,
                    expand=1,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
                for label in lv_header_labels
            ],
        )
        self.lv = ft.ListView(
            expand=True,
            spacing=5,
        )
        self.lv_column = ft.Column([self.lv_header, self.lv], height=300)
        self.lv_display = ft.Container(
            content=self.lv_column,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=12,
            padding=10,
        )
        self.clicked_item: BaseItem = None

        # --- ADD ---
        for field in add_fields.values():
            field.on_change = self.clear_error_field
            field.on_submit = lambda e: self.add_action()
        self.add_fields = add_fields
        add_column_layout.controls.append(
            ft.Row(
                [
                    self._create_main_button(
                        "Adicionar", on_click=lambda e: self.add_action()
                    ),
                    self._create_rubber_button(
                        add_fields,
                        on_click=lambda e: self.clear_fields(self.add_fields),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.add_display = ft.Container(
            content=add_column_layout,
            margin=ft.margin.only(top=5),
        )

        # UPDATE - SECTION -
        for field in update_fields.values():
            field.on_change = self.clear_error_field
            field.on_submit = lambda e: self.update_action()
        self.update_fields = update_fields

        update_column_layout.controls.append(
            ft.Row(
                [
                    self._create_main_button(
                        "Atualizar", on_click=lambda e: self.update_action()
                    ),
                    self._create_rubber_button(
                        update_fields,
                        on_click=lambda e: self.on_item_click(self.clicked_item),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.update_display = ft.Container(
            content=update_column_layout,
            margin=ft.margin.only(top=5),
        )

        self._check_field_dicts_keys(
            (self.add_fields, self.update_fields), db_table_columns
        )

        # TABS - SECTION -
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    "Adicionar",
                    icon=ft.Icons.ADD,
                    height=50,
                    content=self.add_display,
                ),
                ft.Tab(
                    text="Atualizar",
                    icon=ft.Icons.UPDATE,
                    height=50,
                    content=self.update_display,
                ),
            ],
        )

        # DISPLAY - SECTION -
        self.controls = [self.search_bar_display, self.lv_display, self.tabs]

    # GENERIC METHODS

    def on_item_click(self, item: BaseItem | None, update=True):
        if self.clicked_item:
            self.clicked_item.bgcolor = None

        self.clicked_item = item if self.clicked_item != item else None

        if self.clicked_item:
            self.clicked_item.bgcolor = ft.Colors.BLUE_GREY_400
            self.tabs.selected_index = 1

            for key, value in self.clicked_item.values.items():
                if key in self.update_fields:
                    self.update_fields[key].value = value
        else:
            self.clear_fields(self.update_fields, update=False)

        if update:
            self.update()

    def clear_fields(self, target_fields: FieldDict, update=True):
        for field in target_fields.values():
            field.value = None
            field.error_text = None

        if update:
            self.update()

    def clear_error_field(self, e: ft.ControlEvent):
        if e.control.error_text:
            e.control.error_text = None
            e.control.update()

    # ABSTRACT METHODS

    def update_list_view(self, update=True):
        raise NotImplementedError(
            "child class must implement 'update_list_view' method"
        )

    def add_action(self):
        raise NotImplementedError("child class must implement 'add' method")

    def update_action(self):
        raise NotImplementedError("child class must implement 'update' method")

    # HELPERS

    def get_field_data(self, target_fields: FieldDict):
        """Extract values from FieldDicts"""
        data = {}

        for key, field in target_fields.items():
            value = field.value

            data[key] = value

        return data

    @classmethod
    def create_text_field(
        cls,
        label="",
        hint_text="",
        expand=True,
        disabled=False,
        height=40,
        icon: ft.Icons = None,
    ):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            expand=expand,
            height=height,
            disabled=disabled,
            icon=icon,
        )

    def _create_main_button(self, text: str, on_click=None):
        return ft.ElevatedButton(
            text,
            width=300,
            icon=ft.Icons.ADD,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            on_click=on_click,
        )

    def _create_rubber_button(self, target_fields: FieldDict, on_click=None):
        return ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Desfazer",
            on_click=on_click,
        )

    # CHECKERS

    @classmethod
    def _check_field_dicts_keys(
        cls, field_dicts: tuple[FieldDict, FieldDict], table_columns: list[TableColumn]
    ):
        for fd in field_dicts:
            for key in fd.keys():
                if key not in table_columns:
                    raise KeyError(f"Key '{key}' not in {table_columns}")
