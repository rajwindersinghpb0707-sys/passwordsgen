import flet as ft

CARD = "#1B1C2B"
PURPLE = "#A58AFF"
MUTED = "#A5A5B5"


def add_password_view(on_save, navigate):

    website = ft.TextField(
        label="Website or App Name",
        hint_text="Example: Google",
    )

    username = ft.TextField(
        label="Username or Email",
        hint_text="Enter your account username",
    )

    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
    )

    category = ft.Dropdown(
        label="Account Category",
        options=[
            ft.dropdown.Option("Social Media"),
            ft.dropdown.Option("Banking"),
            ft.dropdown.Option("Work"),
            ft.dropdown.Option("Shopping"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Other"),
        ],
        value="Other",
    )

    notes = ft.TextField(
        label="Notes",
        hint_text="Optional information about this account",
        multiline=True,
        min_lines=2,
        max_lines=4,
    )

    message = ft.Text("", color="#FF7777")

    def save(e):

        if (
            not website.value
            or not username.value
            or not password.value
        ):
            message.value = "Please complete all required fields."
            message.update()
            return

        data = {
            "website": website.value.strip(),
            "username": username.value.strip(),
            "password": password.value,
            "category": category.value or "Other",
            "notes": notes.value or "",
            "favorite": False,
        }

        on_save(data)

    return ft.Column(
        [
            ft.Text(
                "Add New Password",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Securely organize your account details.",
                color=MUTED,
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "ACCOUNT INFORMATION",
                            size=12,
                            color=PURPLE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        website,
                        username,
                        password,
                        category,
                        notes,
                        message,

                        ft.Row(
                            [
                                ft.Button(
                                    content=ft.Text("Save Account"),
                                    on_click=save,
                                ),

                                ft.Button(
                                    content=ft.Text("Cancel"),
                                    on_click=lambda e: navigate("vault"),
                                ),
                            ],
                            wrap=True,
                            spacing=10,
                        ),
                    ],
                    spacing=16,
                ),
                bgcolor=CARD,
                padding=22,
                border_radius=18,
            ),

            ft.Text(
                "Required fields: Website, Username and Password.",
                color=MUTED,
                size=11,
            ),
        ],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
    )