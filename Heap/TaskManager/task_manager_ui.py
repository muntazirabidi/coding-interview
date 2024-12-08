import streamlit as st
from datetime import datetime, timedelta
from priority_task_manager import ProjectTaskManager, ProjectTask, TaskPriority, TaskStatus
import streamlit.components.v1 as components

# Configure the default Streamlit theme
st.set_page_config(
    page_title="Project Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the UI
st.markdown("""
    <style>
        /* Main container styling */
        .main .block-container {
            padding: 2rem 3rem;
        }
        
        /* Card-like styling for task items */
        .stExpander {
            background-color: white;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Custom header styling */
        .custom-header {
            background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
            padding: 1.5rem;
            border-radius: 0.5rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Form styling */
        .stForm {
            background-color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa;
        }
        
        /* Stats card styling */
        .stats-card {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
            margin-top: 1rem;
        }
        
        /* Priority badges */
        .priority-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        .priority-HIGH { background-color: #ffebee; color: #c62828; }
        .priority-MEDIUM { background-color: #fff3e0; color: #ef6c00; }
        .priority-LOW { background-color: #e8f5e9; color: #2e7d32; }
    </style>
""", unsafe_allow_html=True)

class TaskManagerUI:
    def __init__(self):
        """Initialize the Task Manager UI with enhanced styling"""
        if 'task_manager' not in st.session_state:
            st.session_state.task_manager = ProjectTaskManager()
        
        # Custom header
        st.markdown(
            """
            <div class="custom-header">
                <h1>📋 Project Task Manager</h1>
                <p>Organize, prioritize, and track your project tasks efficiently</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render_add_task_form(self):
        """Render an enhanced form for adding new tasks"""
        st.markdown("### 📝 Schedule New Task")
        
        with st.form("new_task_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                task_id = st.text_input(
                    "Task ID",
                    value="PROJ-" + str(len(st.session_state.task_manager.heap) + 1),
                    help="Unique identifier for the task"
                )
                title = st.text_input("Task Title", placeholder="Enter a descriptive title")
                priority = st.selectbox(
                    "Priority",
                    options=[p for p in TaskPriority],
                    format_func=lambda x: f"{'🔴' if x == TaskPriority.HIGH else '🟡' if x == TaskPriority.MEDIUM else '🟢'} {x.name}"
                )
            
            with col2:
                due_date = st.date_input("Due Date")
                due_time = st.time_input("Due Time")
                assigned_to = st.text_input("Assigned To", placeholder="Team member name")
            
            # Full width fields
            description = st.text_area(
                "Description",
                placeholder="Provide detailed task description...",
                height=100
            )
            
            col3, col4 = st.columns(2)
            with col3:
                estimated_hours = st.number_input(
                    "Estimated Hours",
                    min_value=0.0,
                    step=0.5,
                    help="Expected time to complete the task"
                )
            
            with col4:
                existing_tasks = [task.task_id for task in st.session_state.task_manager.heap]
                dependencies = st.multiselect(
                    "Dependencies",
                    options=existing_tasks,
                    help="Select tasks that must be completed before this one"
                )
            
            submitted = st.form_submit_button("Schedule Task", use_container_width=True)
            
            if submitted and title:  # Basic validation
                due_datetime = datetime.combine(due_date, due_time)
                
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
                st.success("✅ Task scheduled successfully!")

    def render_task_list(self):
        """Render an enhanced list of all tasks"""
        st.markdown("### 📋 Task List")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_priority = st.multiselect(
                "Filter by Priority",
                options=[p for p in TaskPriority],
                format_func=lambda x: x.name
            )
        with col2:
            filter_status = st.multiselect(
                "Filter by Status",
                options=[s for s in TaskStatus],
                format_func=lambda x: x.value
            )
        with col3:
            search = st.text_input("Search tasks", placeholder="Enter keywords...")
        
        # Get and sort tasks
        tasks = []
        temp_manager = ProjectTaskManager()
        for task in st.session_state.task_manager.heap:
            temp_manager.insert(task)
        
        while not temp_manager.is_empty():
            task = temp_manager.get_highest_priority_task()
            # Apply filters
            if (not filter_priority or task.priority in filter_priority) and \
               (not filter_status or task.status in filter_status) and \
               (not search or search.lower() in task.title.lower() or search.lower() in task.description.lower()):
                tasks.append(task)
        
        # Display tasks
        for task in tasks:
            with st.expander(f"{task.title} ({task.task_id})"):
                cols = st.columns([2, 1, 1])
                
                with cols[0]:
                    st.markdown(f"""
                        <div class="priority-badge priority-{task.priority.name}">
                            {task.priority.name}
                        </div>
                    """, unsafe_allow_html=True)
                    st.write("**Description:**", task.description)
                
                with cols[1]:
                    st.write("**Status:**", task.status.value)
                    st.write("**Due Date:**", task.due_date.strftime('%Y-%m-%d %I:%M %p'))
                    st.write("**Estimated Hours:**", task.estimated_hours)
                
                with cols[2]:
                    st.write("**Assigned To:**", task.assigned_to or "Unassigned")
                    st.write("**Dependencies:**", ', '.join(task.dependencies) if task.dependencies else "None")
                
                # Status update with visual feedback
                new_status = st.select_slider(
                    "Update Status",
                    options=[s for s in TaskStatus],
                    value=task.status,
                    format_func=lambda x: x.value,
                    key=f"status_{task.task_id}"
                )
                if new_status != task.status:
                    task.status = new_status
                    st.success("✅ Status updated!")

def main():
    # Initialize UI
    ui = TaskManagerUI()
    
    # Enhanced sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150", caption="Project Task Manager")
        page = st.radio("📚 Navigation", ["Add Task", "View Tasks"])
        
        # Enhanced statistics
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        total_tasks = len(st.session_state.task_manager.heap)
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Tasks", total_tasks)
        
        with col2:
            completed_tasks = sum(1 for task in st.session_state.task_manager.heap 
                                if task.status == TaskStatus.COMPLETED)
            st.metric("Completed", completed_tasks)
        
        if total_tasks > 0:
            st.markdown("### 🎯 Next Priority Task")
            next_task = st.session_state.task_manager.peek_next_task()
            st.markdown(f"""
                <div class="stats-card">
                    <h4>{next_task.title}</h4>
                    <p>Priority: {next_task.priority.name}</p>
                    <p>Due: {next_task.due_date.strftime('%Y-%m-%d')}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Main content
    if page == "Add Task":
        ui.render_add_task_form()
    else:
        ui.render_task_list()

if __name__ == "__main__":
    main()