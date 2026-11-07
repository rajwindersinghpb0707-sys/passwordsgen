import flet as ft

CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"


def vault_view(passwords, navigate, on_delete):

    results = ft.Column(spacing=12)

    search = ft.TextField(
        label="Search your accounts",
        hint_text="Search website, username or category",
    )

    account_count = ft.Text(
        f"{len(passwords)} saved accounts",
        color=PURPLE,
    )

    def refresh():

        results.controls.clear()

        query = (search.value or "").lower().strip()

        filtered = [
            item for item in passwords
            if query in item.get("website", "").lower()
            or query in item.get("username", "").lower()
            or query in item.get("category", "").lower()
        ]

        if not filtered:

            results.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.LOCK_OUTLINE,
                                size=40,
                                color=PURPLE,
                            ),

                            ft.Text(
                                "Your vault is empty",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                "Add an account or try another search.",
                                color=MUTED,
                            ),
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=CARD,
                    padding=30,
                    border_radius=16,
                )
            )

        for item in filtered:

            password_field = ft.TextField(
                label="Password",
                value=item.get("password", ""),
                password=True,
                can_reveal_password=True,
                read_only=True,
            )

            def remove_account(e, selected=item):
                on_delete(selected)

            results.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            item.get("website", "?")[:1].upper(),
                                            color=PURPLE,
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        bgcolor="#29243D",
                                        padding=14,
                                        border_radius=12,
                                    ),

                                    ft.Column(
                                        [
                                            ft.Text(
                                                item.get(
                                                    "website",
                                                    "Unknown Account",
                                                ),
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),

                                            ft.Text(
                                                item.get("username", ""),
                                                color=MUTED,
                                                size=12,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),

                                    ft.Text(
                                        item.get("category", "Other"),
                                        color=PURPLE,
                                        size=11,
                                    ),
                                ]
                            ),

                            ft.Divider(color="#303145"),

                            password_field,

                            ft.Text(
                                item.get("notes", ""),
                                color=MUTED,
                                size=12,
                            ),

                            ft.Row(
                                [
                                    ft.Button(
                                        content=ft.Text("Delete Account"),
                                        on_click=remove_account,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor=CARD,
                    padding=18,
                    border_radius=16,
                    border=ft.Border.all(1, "#303145"),
                )
            )

    def handle_search(e):
        refresh()
        results.update()

    search.on_change = handle_search

    # Initial build: do not call update() here.
    refresh()

    return ft.Column(
        [
            ft.Text(
                "Password Vault",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "All your saved accounts in one place.",
                color=MUTED,
            ),

            search,

            ft.Row(
                [
                    account_count,
                    ft.Container(expand=True),

                    ft.Button(
                        content=ft.Text("+ Add Password"),
                        on_click=lambda e: navigate("add"),
                    ),
                ]
            ),

            results,
        ],
        spacing=18,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )