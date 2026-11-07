
import flet as ft


CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"


def password_card(
    item,
    on_delete=None,
    on_favorite=None,
    on_edit=None,
    on_copy=None
):

    website = item.get("website", "Unknown Account")
    username = item.get("username", "")
    password = item.get("password", "")
    category = item.get("category", "Other")
    favorite = item.get("favorite", False)

    password_field = ft.TextField(
        label="Password",
        value=password,
        password=True,
        can_reveal_password=True,
        read_only=True,
        dense=True
    )

    def action_button(label, callback):
        return ft.Button(
            content=ft.Text(label),
            on_click=(
                lambda e: callback(item)
                if callback else None
            ),
            disabled=callback is None
        )

    return ft.Container(
        content=ft.Column(
            [
                # Account heading
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                website[:1].upper(),
                                size=21,
                                weight=ft.FontWeight.BOLD,
                                color=PURPLE
                            ),
                            bgcolor="#30264B",
                            padding=14,
                            border_radius=12
                        ),

                        ft.Column(
                            [
                                ft.Text(
                                    website,
                                    size=17,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    username,
                                    size=12,
                                    color=MUTED
                                )
                            ],
                            spacing=4,
                            expand=True
                        ),

                        ft.IconButton(
                            icon=(
                                ft.Icons.STAR
                                if favorite
                                else ft.Icons.STAR_OUTLINE
                            ),
                            icon_color="#F2C66D" if favorite else MUTED,
                            tooltip="Toggle favorite",
                            on_click=(
                                lambda e: on_favorite(item)
                                if on_favorite else None
                            )
                        )
                    ],
                    spacing=12
                ),

                ft.Divider(color="#303145"),

                # Category
                ft.Row(
                    [
                        ft.Text("CATEGORY", size=10, color=MUTED),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                category,
                                size=11,
                                color=PURPLE
                            ),
                            bgcolor="#30264B",
                            padding=8,
                            border_radius=8
                        )
                    ]
                ),

                # Password field
                password_field,

                # Notes
                ft.Text(
                    item.get("notes", ""),
                    color=MUTED,
                    size=11
                ),

                # Actions
                ft.Row(
                    [
                        action_button("Copy", on_copy),
                        action_button("Edit", on_edit),
                        action_button("Delete", on_delete)
                    ],
                    wrap=True,
                    spacing=8
                )
            ],
            spacing=12
        ),
        bgcolor=CARD,
        padding=17,
        border_radius=16,
        border=ft.Border.all(1, "#303145"),
        width=360
    )
