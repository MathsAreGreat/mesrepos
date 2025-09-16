import flet as ft


def main(page: ft.Page):
    page.title = "Task Manager"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Define a list to store tasks
    tasks = ft.Column()

    # Function to handle adding tasks
    def add_task(e):
        task_text = task_input.value.strip()
        if task_text:
            # Create a new row with the task and a delete button
            task_row = ft.Row(
                controls=[
                    ft.Text(task_text),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,  # Updated here
                        on_click=lambda e: tasks.controls.remove(
                            task_row) or page.update()
                    ),
                ],
            )
            tasks.controls.append(task_row)
            task_input.value = ""  # Clear input
            page.update()

    # Input field and button for adding tasks
    task_input = ft.TextField(
        hint_text="Enter a task",
        expand=True,
        on_submit=add_task,
    )
    add_button = ft.FilledButton("Add Task", on_click=add_task)

    # Add all UI elements to the page
    page.add(
        ft.Row([task_input, add_button], spacing=10),
        tasks,
    )


# Run the app
ft.app(target=main)
