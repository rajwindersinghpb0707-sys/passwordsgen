import flet as ft

from pages.dashboard import dashboard_view
from pages.vault import vault_view
from pages.add_password import add_password_view
from pages.settings import settings_view

from storage.secure_storage import SecureStorage


def main(page: ft.Page):

    page.title = "CloudPass - Password Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#10111B"
    page.padding = 20

    PURPLE = "#A58AFF"
    MUTED = "#A5A5B5"

    storage = SecureStorage()

    passwords = []
    master_password = None
    current_page = "dashboard"

    # NAVIGATION

    def navigate(destination):
        nonlocal current_page

        current_page = destination
        render()

    # SAVE PASSWORD

    def save_password(data):

        if master_password is None:
            show_authentication()
            return

        try:
            storage.save_password(data, master_password)

            passwords.clear()
            passwords.extend(
                storage.get_passwords(master_password)
            )

            navigate("vault")

        except Exception as error:
            print("Save error:", error)

    # DELETE PASSWORD

    def delete_password(item):

        if master_password is None:
            show_authentication()
            return

        try:
            record_id = item.get("id")

            if record_id is not None:
                storage.delete_password(
                    record_id,
                    master_password
                )

            passwords.clear()
            passwords.extend(
                storage.get_passwords(master_password)
            )

            render()

        except Exception as error:
            print("Delete error:", error)

    # LOCK VAULT

    def lock_app(e=None):
        nonlocal master_password, current_page

        master_password = None
        passwords.clear()
        current_page = "dashboard"

        show_authentication()

    # AUTHENTICATION

    def show_authentication():

        page.clean()

        is_first_setup = not storage.has_master_password()

        title = (
            "Create Your Master Password"
            if is_first_setup
            else "Welcome Back"
        )

        description = (
            "Create a strong master password to protect your vault."
            if is_first_setup
            else "Unlock CloudPass to access your saved accounts."
        )

        password_field = ft.TextField(
            label="Master Password",
            password=True,
            can_reveal_password=True,
            autofocus=True,
        )

        confirm_field = None

        controls = [
            ft.Text(
                "CLOUDPASS",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=PURPLE,
            ),

            ft.Text(
                title,
                size=23,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(description, color=MUTED),

            password_field,
        ]

        if is_first_setup:

            confirm_field = ft.TextField(
                label="Confirm Master Password",
                password=True,
                can_reveal_password=True,
            )

            controls.append(confirm_field)

        message = ft.Text("", color="#FF7777")

        def authenticate(e):

            nonlocal master_password

            entered_password = password_field.value or ""

            if not entered_password:
                message.value = "Enter your master password."
                page.update()
                return

            try:

                if is_first_setup:

                    if entered_password != (confirm_field.value or ""):
                        message.value = "Passwords do not match."
                        page.update()
                        return

                    storage.create_master_password(entered_password)

                else:

                    if not storage.verify_master_password(entered_password):
                        message.value = "Incorrect master password."
                        page.update()
                        return

                master_password = entered_password

                passwords.clear()
                passwords.extend(
                    storage.get_passwords(master_password)
                )

                render()

            except Exception as error:

                message.value = str(error)
                page.update()

        controls.extend([
            message,

            ft.Button(
                content=ft.Text(
                    "Create Secure Vault"
                    if is_first_setup
                    else "Unlock CloudPass"
                ),
                on_click=authenticate,
            ),

            ft.Text(
                "Your master password is not stored as plaintext.",
                size=11,
                color=MUTED,
            ),
        ])

        page.add(
            ft.Container(
                content=ft.Column(
                    controls,
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                width=460,
                padding=30,
                bgcolor="#1B1C2B",
                border_radius=20,
            )
        )

        page.update()

    # NAVIGATION BUTTON

    def navigation_button(label, destination):

        return ft.Button(
            content=ft.Text(label),
            on_click=lambda e: navigate(destination),
        )

    # MAIN APPLICATION

    def render():

        if master_password is None:
            show_authentication()
            return

        page.clean()

        header = ft.Row([
            ft.Column([
                ft.Text(
                    "CLOUDPASS",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=PURPLE,
                ),

                ft.Text(
                    "ENCRYPTED PASSWORD MANAGER",
                    size=9,
                    color=MUTED,
                ),
            ], spacing=2),

            ft.Container(expand=True),

            ft.Button(
                content=ft.Text("Lock Vault"),
                on_click=lock_app,
            ),
        ])

        navigation = ft.Row(
            [
                navigation_button("Dashboard", "dashboard"),
                navigation_button("Vault", "vault"),
                navigation_button("+ Add Password", "add"),
                navigation_button("Settings", "settings"),
            ],
            wrap=True,
            spacing=8,
        )

        if current_page == "dashboard":

            page_content = dashboard_view(
                passwords,
                navigate,
            )

        elif current_page == "vault":

            page_content = vault_view(
                passwords,
                navigate,
                delete_password,
            )

        elif current_page == "add":

            page_content = add_password_view(
                save_password,
                navigate,
            )

        elif current_page == "settings":

            page_content = settings_view()

        else:
            page_content = ft.Text("Page not found")

        layout = ft.Column(
            [
                header,
                ft.Divider(color="#303145"),
                navigation,
                ft.Divider(color="#303145"),

                ft.Container(
                    content=page_content,
                    expand=True,
                ),
            ],
            spacing=12,
            expand=True,
        )

        page.add(layout)
        page.update()

    show_authentication()


ft.run(main)
app = ft.run(main, export_asgi_app=True)
