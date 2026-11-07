import flet as ft

CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"


def settings_view():

    return ft.Column(
        [
            ft.Text(
                "Settings",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Manage your CloudPass application information.",
                color=MUTED,
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "APPLICATION",
                            color=PURPLE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.LOCK,
                                color=PURPLE,
                            ),
                            title=ft.Text("Application Name"),
                            subtitle=ft.Text("CloudPass"),
                        ),

                        ft.Divider(color="#303145"),

                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.SECURITY,
                                color=PURPLE,
                            ),
                            title=ft.Text("Security"),
                            subtitle=ft.Text(
                                "Master-password authentication enabled"
                            ),
                        ),

                        ft.Divider(color="#303145"),

                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.STORAGE,
                                color=PURPLE,
                            ),
                            title=ft.Text("Storage"),
                            subtitle=ft.Text(
                                "Local SQLite database"
                            ),
                        ),

                        ft.Divider(color="#303145"),

                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.CLOUD_OUTLINED,
                                color=PURPLE,
                            ),
                            title=ft.Text("Cloud Sync"),
                            subtitle=ft.Text(
                                "Not connected"
                            ),
                        ),
                    ],
                    spacing=8,
                ),
                bgcolor=CARD,
                padding=20,
                border_radius=16,
                border=ft.Border.all(1, "#303145"),
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "ABOUT CLOUDPASS",
                            color=PURPLE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "CloudPass is a password manager designed "
                            "to organize account credentials in one place.",
                            color=MUTED,
                            size=12,
                        ),

                        ft.Text(
                            "Version 1.0",
                            color=MUTED,
                            size=11,
                        ),
                    ],
                    spacing=10,
                ),
                bgcolor=CARD,
                padding=20,
                border_radius=16,
            ),
        ],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )