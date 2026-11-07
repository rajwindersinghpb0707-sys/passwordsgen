import flet as ft

CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"


def dashboard_view(passwords, navigate):

    total = len(passwords)

    favorites = len([
        item for item in passwords
        if item.get("favorite", False)
    ])

    categories = len(set(
        item.get("category", "Other")
        for item in passwords
    ))

    def stat_card(title, value, description, icon):

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, color=PURPLE, size=25),
                            ft.Container(expand=True),
                            ft.Text(
                                str(value),
                                size=27,
                                weight=ft.FontWeight.BOLD,
                                color=PURPLE,
                            ),
                        ]
                    ),

                    ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        description,
                        size=11,
                        color=MUTED,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=CARD,
            padding=20,
            border_radius=16,
            border=ft.Border.all(1, "#303145"),
            col={"xs": 12, "sm": 6, "md": 4},
        )

    recent_accounts = []

    for item in passwords[-5:][::-1]:

        recent_accounts.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                item.get("website", "?")[:1].upper(),
                                color=PURPLE,
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                            bgcolor="#29243D",
                            padding=12,
                            border_radius=10,
                        ),

                        ft.Column(
                            [
                                ft.Text(
                                    item.get("website", "Unknown"),
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    item.get("username", ""),
                                    color=MUTED,
                                    size=11,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),

                        ft.Text(
                            item.get("category", "Other"),
                            color=PURPLE,
                            size=11,
                        ),
                    ]
                ),
                bgcolor=CARD,
                padding=14,
                border_radius=12,
            )
        )

    if not recent_accounts:

        recent_accounts.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.LOCK_OUTLINE,
                            color=PURPLE,
                            size=35,
                        ),

                        ft.Text(
                            "No accounts saved yet",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Start by adding your first account.",
                            color=MUTED,
                        ),

                        ft.Button(
                            content=ft.Text("Add Password"),
                            on_click=lambda e: navigate("add"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                bgcolor=CARD,
                padding=25,
                border_radius=16,
            )
        )

    return ft.Column(
        [
            ft.Text(
                "Dashboard",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Welcome to your secure password manager.",
                color=MUTED,
            ),

            ft.ResponsiveRow(
                [
                    stat_card(
                        "Total Accounts",
                        total,
                        "Saved passwords",
                        ft.Icons.LOCK,
                    ),

                    stat_card(
                        "Favorites",
                        favorites,
                        "Favorite accounts",
                        ft.Icons.STAR,
                    ),

                    stat_card(
                        "Categories",
                        categories,
                        "Account categories",
                        ft.Icons.CATEGORY,
                    ),
                ],
                spacing=12,
                run_spacing=12,
            ),

            ft.Row(
                [
                    ft.Text(
                        "Recent Accounts",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Container(expand=True),

                    ft.Button(
                        content=ft.Text("View Vault"),
                        on_click=lambda e: navigate("vault"),
                    ),
                ]
            ),

            ft.Column(
                recent_accounts,
                spacing=10,
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "SECURITY INFORMATION",
                            color=PURPLE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Your account records are stored in your local "
                            "CloudPass database using your configured "
                            "encryption system.",
                            color=MUTED,
                            size=12,
                        ),

                        ft.Text(
                            "Cloud synchronization is not connected.",
                            color=MUTED,
                            size=11,
                        ),
                    ],
                    spacing=8,
                ),
                bgcolor=CARD,
                padding=18,
                border_radius=14,
            ),
        ],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )