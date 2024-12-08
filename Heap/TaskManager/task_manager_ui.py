import streamlit as st
from datetime import datetime, timedelta
from priority_task_manager import ProjectTaskManager, ProjectTask, TaskPriority, TaskStatus

class TaskManagerUI:
    def __init__(self):
        """Initialize the Task Manager UI"""
        # Initialize session state to persist data between reruns
        if 'task_manager' not in st.session_state:
            st.session_state.task_manager = ProjectTaskManager()

    def render_add_task_form(self):
        """Render the form for adding new tasks"""
        st.subheader("Schedule New Task")
        
        with st.form("new_task_form"):
            # Required fields
            task_id = st.text_input("Task ID", value="PROJ-" + str(len(st.session_state.task_manager.heap) + 1))
            title = st.text_input("Task Title")
            priority = st.selectbox(
                "Priority",
                options=[p for p in TaskPriority],
                format_func=lambda x: x.name
            )
            due_date = st.date_input("Due Date")
            due_time = st.time_input("Due Time")
            
            # Optional fields
            assigned_to = st.text_input("Assigned To")
            description = st.text_area("Description")
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=0.5)
            
            # Dependencies (multi-select from existing tasks)
            existing_tasks = [task.task_id for task in st.session_state.task_manager.heap]
            dependencies = st.multiselect("Dependencies", options=existing_tasks)
            
            submitted = st.form_submit_button("Schedule Task")
            
            if submitted:
                # Combine date and time
                due_datetime = datetime.combine(due_date, due_time)
                
                # Schedule the task
                st.session_state.task_manager.schedule_task(
                    task_id=task_id,
                    title=title,
                    priority=priority,
                    due_date=due_datetime,
                    assigned_to=assigned_to,
                    description=description,
                    estimated_hours=estimated_hours,
                    dependencies=set(dependencies)
                )
                st.success(f"Task {task_id} scheduled successfully!")

    def render_task_list(self):
        """Render the list of all tasks"""
        st.subheader("Task List")
        
        # Create a temporary list of all tasks sorted by priority
        tasks = []
        temp_manager = ProjectTaskManager()
        
        # Clone current task manager to avoid modifying original
        for task in st.session_state.task_manager.heap:
            temp_manager.insert(task)
        
        # Extract tasks in priority order
        while not temp_manager.is_empty():
            tasks.append(temp_manager.get_highest_priority_task())
        
        # Display tasks in a more visual format
        for task in tasks:
            with st.expander(f"{task.priority.name}: {task.title} ({task.task_id})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Status:**", task.status.value)
                    st.write("**Assigned To:**", task.assigned_to or "Unassigned")
                    st.write("**Due Date:**", task.due_date.strftime('%Y-%m-%d %I:%M %p'))
                
                with col2:
                    st.write("**Estimated Hours:**", task.estimated_hours)
                    st.write("**Dependencies:**", ', '.join(task.dependencies) if task.dependencies else "None")
                
                st.write("**Description:**", task.description)
                
                # Add status update button
                new_status = st.selectbox(
                    "Update Status",
                    options=[s for s in TaskStatus],
                    format_func=lambda x: x.value,
                    key=f"status_{task.task_id}"
                )
                if new_status != task.status:
                    task.status = new_status
                    st.success(f"Status updated for task {task.task_id}")

def main():
    st.title("Project Task Manager")
    
    # Initialize UI
    ui = TaskManagerUI()
    
    # Sidebar for navigation
    page = st.sidebar.radio("Navigation", ["Add Task", "View Tasks"])
    
    if page == "Add Task":
        ui.render_add_task_form()
    else:
        ui.render_task_list()
    
    # Add some useful statistics in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    
    total_tasks = len(st.session_state.task_manager.heap)
    st.sidebar.write(f"Total Tasks: {total_tasks}")
    
    if total_tasks > 0:
        next_task = st.session_state.task_manager.peek_next_task()
        st.sidebar.write("Next Priority Task:")
        st.sidebar.write(f"- {next_task.title}")
        st.sidebar.write(f"- Priority: {next_task.priority.name}")

if __name__ == "__main__":
    main()