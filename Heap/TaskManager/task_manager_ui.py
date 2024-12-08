import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from priority_task_manager import ProjectTaskManager, ProjectTask, TaskPriority, TaskStatus
import json
import io
import base64

# Configure page settings
st.set_page_config(
    page_title="Project Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
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
    """
    Handles all UI rendering and interaction for the task management system.
    Provides methods for displaying forms, lists, and visualizations.
    """
    def __init__(self):
        """Initialize the Task Manager UI and set up session state"""
        if 'task_manager' not in st.session_state:
            st.session_state.task_manager = ProjectTaskManager()
        if 'activity_log' not in st.session_state:
            st.session_state.activity_log = []
        if 'comments' not in st.session_state:
            st.session_state.comments = {}
        if 'time_tracking' not in st.session_state:
            st.session_state.time_tracking = {}
        
        # Display header
        st.markdown(
            """
            <div class="custom-header">
                <h1>📋 Project Task Manager</h1>
                <p>Organize, prioritize, and track your project tasks efficiently</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def log_activity(self, action: str, details: str):
        """Record user actions for audit and history tracking"""
        st.session_state.activity_log.append({
            'timestamp': datetime.now(),
            'action': action,
            'details': details
        })

    def render_add_task_form(self):
        """Display and handle the form for creating new tasks"""
        st.markdown("### 📝 Schedule New Task")
        
        with st.form("new_task_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                task_id = st.text_input(
                    "Task ID",
                    value=f"PROJ-{len(st.session_state.task_manager.heap) + 1}",
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
            
            if submitted and title:
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
                self.log_activity('task_created', f'Created task: {title}')
                st.success("✅ Task scheduled successfully!")

    def render_time_tracking(self, task_id: str):
        """Handle time tracking interface for individual tasks"""
        if task_id not in st.session_state.time_tracking:
            st.session_state.time_tracking[task_id] = {
                'logged_time': 0,
                'sessions': []
            }
        
        tracking = st.session_state.time_tracking[task_id]
        
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input(
                "Log Time (hours)",
                min_value=0.0,
                step=0.5,
                key=f"time_{task_id}"
            )
            if st.button("Log Time", key=f"log_{task_id}"):
                tracking['logged_time'] += hours
                tracking['sessions'].append({
                    'timestamp': datetime.now(),
                    'hours': hours
                })
                self.log_activity('time_logged', f'Logged {hours} hours for task {task_id}')
        
        with col2:
            st.metric("Total Time Logged", f"{tracking['logged_time']} hours")

    def render_comments_section(self, task_id: str):
        """Display and handle comments for individual tasks"""
        if task_id not in st.session_state.comments:
            st.session_state.comments[task_id] = []
        
        comment = st.text_area("Add Comment", key=f"comment_{task_id}")
        if st.button("Post Comment", key=f"post_{task_id}"):
            st.session_state.comments[task_id].append({
                'timestamp': datetime.now(),
                'text': comment,
                'user': 'Current User'
            })
            self.log_activity('comment_added', f'New comment on task {task_id}')
        
        for comment in reversed(st.session_state.comments[task_id]):
            st.markdown(f"""
                <div style='border-left: 3px solid #4CAF50; padding-left: 10px; margin: 10px 0;'>
                    <p><strong>{comment['user']}</strong> - {comment['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
                    <p>{comment['text']}</p>
                </div>
            """, unsafe_allow_html=True)

    def generate_gantt_chart(self):
        """Create a Gantt chart visualization of all tasks"""
        tasks = []
        for task in st.session_state.task_manager.heap:
            end_date = task.due_date
            start_date = end_date - timedelta(hours=task.estimated_hours)
            tasks.append({
                'Task': task.title,
                'Start': start_date,
                'Finish': end_date,
                'Priority': task.priority.name
            })
        
        if tasks:
            df = pd.DataFrame(tasks)
            fig = ff.create_gantt(df, colors={
                'HIGH': 'rgb(242, 132, 130)',
                'MEDIUM': 'rgb(255, 199, 132)',
                'LOW': 'rgb(144, 238, 144)'
            })
            st.plotly_chart(fig)
        else:
            st.info("Add tasks to see the project timeline visualization")

    def generate_metrics_dashboard(self):
        """Display project metrics and visualizations"""
        tasks = list(st.session_state.task_manager.heap)
        
        # Calculate metrics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
        overdue_tasks = sum(1 for task in tasks if task.due_date < datetime.now() and task.status != TaskStatus.COMPLETED)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", total_tasks)
        with col2:
            st.metric("Completed", completed_tasks)
        with col3:
            completion_rate = f"{(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "0%"
            st.metric("Completion Rate", completion_rate)
        with col4:
            st.metric("Overdue Tasks", overdue_tasks, delta=-overdue_tasks, delta_color="inverse")
        
        if tasks:
            # Priority distribution
            priority_counts = pd.DataFrame([{'Priority': task.priority.name} for task in tasks])
            fig_priority = px.pie(priority_counts, names='Priority', title='Task Priority Distribution')
            st.plotly_chart(fig_priority)
            
            # Status distribution
            status_counts = pd.DataFrame([{'Status': task.status.value} for task in tasks])
            fig_status = px.pie(status_counts, names='Status', title='Task Status Distribution')
            st.plotly_chart(fig_status)
            
            # Time tracking overview
            time_tracking_data = []
            for task in tasks:
                logged_time = st.session_state.time_tracking.get(task.task_id, {}).get('logged_time', 0)
                time_tracking_data.append({
                    'Task': task.title,
                    'Estimated Hours': task.estimated_hours,
                    'Actual Hours': logged_time
                })
            
            if time_tracking_data:
                df_time = pd.DataFrame(time_tracking_data)
                fig_time = px.bar(df_time, x='Task', y=['Estimated Hours', 'Actual Hours'],
                                title='Estimated vs Actual Hours',
                                barmode='group')
                st.plotly_chart(fig_time)
        else:
            st.info("""
                No tasks have been created yet. Start by adding some tasks using the 'Add Task' page!
                
                Quick tips:
                1. Click on 'Add Task' in the sidebar
                2. Fill in the task details
                3. Click 'Schedule Task' to create your first task
                
                Once you have tasks, this dashboard will show:
                - Task priority distribution
                - Status breakdown
                - Time tracking analysis
                - And more!
            """)

    def render_task_list(self):
        """Display and manage the list of all tasks"""
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
        # Instead of using insert, we'll create a new heap while preserving the original
        original_tasks = st.session_state.task_manager.heap.copy()
        sorted_tasks = []
        temp_heap = []
        
        # Push all tasks to temporary heap
        for task in original_tasks:
            heapq.heappush(temp_heap, task)
        
        # Extract tasks in priority order
        while temp_heap:
            task = heapq.heappop(temp_heap)
            # Apply filters
            if (not filter_priority or task.priority in filter_priority) and \
            (not filter_status or task.status in filter_status) and \
            (not search or search.lower() in task.title.lower() or search.lower() in task.description.lower()):
                sorted_tasks.append(task)
        
        # Restore original heap
        st.session_state.task_manager.heap = original_tasks
        
        # Display tasks
        for task in sorted_tasks:
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
                
                # Time tracking section
                st.markdown("#### ⏱️ Time Tracking")
                self.render_time_tracking(task.task_id)
                
                # Comments section
                st.markdown("#### 💬 Comments")
                self.render_comments_section(task.task_id)
                
                # Status update
                new_status = st.select_slider(
                    "Update Status",
                    options=[s for s in TaskStatus],
                    value=task.status,
                    format_func=lambda x: x.value,
                    key=f"status_{task.task_id}"
                )
                if new_status != task.status:
                    task.status = new_status
                    self.log_activity('status_updated', f'Updated status of task {task.task_id} to {new_status.value}')
                    st.success("✅ Status updated!")

    def export_data(self):
        """Handle data export in various formats"""
        st.markdown("### 📤 Export Project Data")
        export_format = st.selectbox(
            "Select Export Format",
            ["CSV", "JSON", "Excel"],
            help="Choose the format for your exported data"
        )
        
        if st.button("Export Data"):
            tasks_data = []
            for task in st.session_state.task_manager.heap:
                task_dict = {
                    'task_id': task.task_id,
                    'title': task.title,
                    'priority': task.priority.name,
                    'status': task.status.value,
                    'due_date': task.due_date.strftime('%Y-%m-%d %H:%M'),
                    'assigned_to': task.assigned_to,
                    'description': task.description,
                    'estimated_hours': task.estimated_hours,
                    'dependencies': list(task.dependencies),
                    'logged_time': st.session_state.time_tracking.get(task.task_id, {}).get('logged_time', 0)
                }
                tasks_data.append(task_dict)
            
            if export_format == "CSV":
                df = pd.DataFrame(tasks_data)
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="tasks_export.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            elif export_format == "JSON":
                json_str = json.dumps(tasks_data, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="tasks_export.json">Download JSON</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            elif export_format == "Excel":
                df = pd.DataFrame(tasks_data)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Tasks', index=False)
                b64 = base64.b64encode(output.getvalue()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="tasks_export.xlsx">Download Excel</a>'
                st.markdown(href, unsafe_allow_html=True)

    def main(self):
        """Main application interface and navigation"""
        st.sidebar.title("📊 Project Manager")
        
        # Store the current page in session state if it doesn't exist
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
        
        # Navigation
        page = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Add Task", "View Tasks", "Timeline", "Reports", "Export"],
            index=["Dashboard", "Add Task", "View Tasks", "Timeline", "Reports", "Export"].index(st.session_state.current_page)
        )
        
        # Update the current page
        st.session_state.current_page = page
        
        if page == "Dashboard":
            st.title("Project Dashboard")
            self.generate_metrics_dashboard()
            
            # Activity Log
            st.markdown("### Recent Activity")
            for activity in reversed(st.session_state.activity_log[-5:]):
                st.text(f"{activity['timestamp'].strftime('%Y-%m-%d %H:%M')} - {activity['action']}: {activity['details']}")
        
        elif page == "Add Task":
            self.render_add_task_form()
        
        elif page == "View Tasks":
            self.render_task_list()
        
        elif page == "Timeline":
            st.title("Project Timeline")
            self.generate_gantt_chart()
        
        elif page == "Reports":
            st.title("Project Reports")
            report_type = st.selectbox(
                "Report Type",
                ["Task Status Summary", "Time Tracking Analysis", "Priority Distribution"]
            )
            self.generate_metrics_dashboard()
        
        elif page == "Export":
            st.title("Export Data")
            self.export_data()

if __name__ == "__main__":
    app = TaskManagerUI()
    app.main()