
import flet as ft


BG = "#10111B"
CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"
ACTIVE = "#30264B"


def sidebar(active_page="dashboard", on_navigate=None):

    def nav_item(label, icon, destination):
        is_active = active_page == destination

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        icon,
                        size=19,
                        color=PURPLE if is_active else MUTED
                    ),
                    ft.Text(
                        label,
                        size=14,
                        weight=(
                            ft.FontWeight.BOLD
                            if is_active
                            else ft.FontWeight.NORMAL
                        ),
                        color="#FFFFFF" if is_active else MUTED
                    )
                ],
                spacing=13
            ),
            padding=13,
            border_radius=11,
            bgcolor=ACTIVE if is_active else None,
            on_click=(
                lambda e: on_navigate(destination)
                if on_navigate else None
            )
        )

    return ft.Container(
        width=245,
        bgcolor=CARD,
        padding=18,
        border_radius=18,
        content=ft.Column(
            [
                # Brand
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.SHIELD,
                                color=PURPLE,
                                size=26
                            ),
                            bgcolor="#30264B",
                            padding=11,
                            border_radius=12
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "CLOUDPASS",
                                    size=19,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF"
                                ),
                                ft.Text(
                                    "PASSWORD MANAGER",
                                    size=9,
                                    color=MUTED
                                )
                            ],
                            spacing=2
                        )
                    ],
                    spacing=10
                ),

                ft.Divider(color="#303145"),

                ft.Text(
                    "WORKSPACE",
                    size=10,
                    color=MUTED,
                    weight=ft.FontWeight.BOLD
                ),

                nav_item(
                    "Dashboard",
                    ft.Icons.DASHBOARD_OUTLINED,
                    "dashboard"
                ),

                nav_item(
                    "Password Vault",
                    ft.Icons.LOCK_OUTLINE,
                    "vault"
                ),

                nav_item(
                    "Add Password",
                    ft.Icons.ADD_CIRCLE_OUTLINE,
                    "add"
                ),

                nav_item(
                    "Password Generator",
                    ft.Icons.AUTO_AWESOME,
                    "generator"
                ),

                ft.Divider(color="#303145"),

                ft.Text(
                    "PREFERENCES",
                    size=10,
                    color=MUTED,
                    weight=ft.FontWeight.BOLD
                ),

                nav_item(
                    "Settings",
                    ft.Icons.SETTINGS_OUTLINED,
                    "settings"
                ),

                ft.Container(expand=True),

                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.SHIELD_OUTLINED,
                                color=PURPLE,
                                size=25
                            ),
                            ft.Text(
                                "Your security matters",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "CloudPass security setup is in progress.",
                                size=10,
                                color=MUTED
                            )
                        ],
                        spacing=9
                    ),
                    bgcolor="#29213F",
                    padding=14,
                    border_radius=13
                ),

                ft.Text(
                    "CloudPass v1.0",
                    color=MUTED,
                    size=10
                )
            ],
            spacing=12,
            expand=True
        )
    )
