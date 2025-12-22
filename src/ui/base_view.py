import flet as ft
from application.app import App
from data.table_classes import TableColumn
from typing import TypeAlias, Dict, Callable


FieldDict: TypeAlias = Dict[TableColumn, ft.TextField]


class BaseContextMenu(ft.Container):
    ...


class BaseItem(ft.Container):
    def __init__(
        self,
        values: dict[TableColumn, str | int | float],
        display_values: list[str],
        on_left_click: Callable[[ft.Container], None],
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
        self.on_click = lambda e: on_left_click(self)



class BaseView(ft.Container):
    def __init__(
        self,
        app: App,
        search_layout: ft.Container,
        lv_headers: tuple[str, ...],
        add_layout: ft.Container,
        update_layout: ft.Container,
    ):
        super().__init__()

        self.app = app

        self.lv = ft.ListView(
            expand=True,
            spacing=5,
        )
        self.clicked_item: BaseItem = None
        self.lv_context_menu: BaseContextMenu = None

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Adicionar",
                    icon=ft.Icons.ADD,
                    height=50,
                    content=add_layout,
                ),
                ft.Tab(
                    text="Atualizar",
                    icon=ft.Icons.UPDATE,
                    height=50,
                    content=update_layout,
                )
            ]
        )

        lv_header = ft.Row(
            controls=[
                ft.Text(
                    value=label,
                    size=16,
                    expand=1,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
                for label in lv_headers
            ]
        )
        lv_layout = ft.Container(
            content=ft.Column(
                controls=[
                    lv_header,
                    self.lv
                ],
                height=300,
            ),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=12,
            padding=10,
        )

        
        self.content=ft.Column(
            controls=[
                search_layout,
                lv_layout,
                self.tabs
            ]
        )

    # GENERIC METHODS

    def on_item_left_click(self, item: BaseItem | None, update=True):
        if self.clicked_item:
            self.clicked_item.bgcolor = None

        self.clicked_item = item if self.clicked_item != item else None

        if self.clicked_item:
            self.clicked_item.bgcolor = ft.Colors.BLUE_GREY_400
            self._item_left_clicked(True)
        else:
            self._item_left_clicked(False)

        if update: self.update()
        
    def db_action_error_handling(
        self,
        error_messages: dict,
        target_field_dict: FieldDict,
        snack_bar_message: str = "Sucesso"
    ):
        has_errors = False
        for field_key, msg in error_messages.items():
            target_field_dict[field_key].error_text = msg if msg else None
            if msg:
                has_errors = True

        if not has_errors:
            self.clear_fields(target_field_dict, update=False)
            self.update_lv(update=False)
            self.page.snack_bar.content.value = snack_bar_message
            self.page.snack_bar.bgcolor = ft.Colors.GREEN
            self.page.snack_bar.open = True
            self.page.overlay.append(self.page.snack_bar)

        self.page.update()

    def update_lv(self, update=True):

        self.lv.controls.clear()
        raw_base_items_list = self.get_raw_base_items_list()

        for raw_base_item in raw_base_items_list:
            self.lv.controls.append(
                BaseItem(**raw_base_item)
            )
        
        if update: self.update()

    def clear_fields(self, target: FieldDict | tuple[FieldDict, ...], update=True):
        def _clear_field_dict(fd: FieldDict):
            for field in fd.values():
                field.value = None
                field.error_text = None

        if isinstance(target, tuple):
            for fd in target:
                _clear_field_dict(fd)
        else:
            _clear_field_dict(target)

        if update: self.update()
        
    def clear_error_field(self, e: ft.ControlEvent):
        if e.control.error_text:
            e.control.error_text = None
            e.control.update()

    # ABSTRACT METHODS

    def _item_left_clicked(self, cliked: bool):
        raise NotImplementedError(
            "child class must implement '_item_left_clicked' method"
        )

    def add_action(self):
        """Try to add, get the errors and call BaseView's db action error handler"""
        raise NotImplementedError("child class must implement 'add' method")

    def update_action(self):
        """Try to update, get the errors and call BaseView's db action error handler"""
        raise NotImplementedError("child class must implement 'update' method")

    def get_raw_base_items_list(self) -> list[Dict]:
        """Dicts must contain the same key words as BaseItem's args"""
        raise NotImplementedError("child class must implement 'get_raw_base_items_list' method")
    
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
        on_change: Callable = None
    ):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            expand=expand,
            height=height,
            disabled=disabled,
            icon=icon,
            on_change=on_change
        )

    @staticmethod
    def _create_main_button(
        text: str,
        icon: ft.Icons,
        on_click=None
    ):
        return ft.ElevatedButton(
            text,
            width=300,
            icon=icon,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            on_click=on_click,
        )

    @staticmethod
    def _create_rubber_button(on_click=None):
        return ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Desfazer",
            on_click=on_click,
        )
    
    @staticmethod
    def _create_column_layout(*rows: ft.Row):
        return ft.Column(
            controls=rows,
        )
    
    @staticmethod
    def _create_container_display(content):
        return ft.Container(
            content=content,
            margin=ft.margin.only(top=5),
        )