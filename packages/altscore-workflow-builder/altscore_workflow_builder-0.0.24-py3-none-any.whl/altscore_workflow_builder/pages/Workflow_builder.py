import streamlit as st
from altscore_workflow_builder.utils import list_workflows, load_workflow_definition, load_task_definitions, \
    save_task_definitions, save_workflow_definition
from altscore_workflow_builder.custom_tasks_utils import determine_levels, add_item, update_edges, create_task, \
    delete_task
from altscore_workflow_builder.input_override_utils import add_input_override
from altscore_workflow_builder.flow_definition_utils import add_workflow_args, remove_workflow_args
from altscore_workflow_builder.native_tasks_utils import add_native_task, remove_native_task
from altscore_workflow_builder.utils import hide_deploy_button
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide")
hide_deploy_button()
st.sidebar.header("Graph Configuration")
workflow = st.sidebar.selectbox("Select Workflow", list_workflows())
flow_definition = load_workflow_definition(workflow['alias'], workflow['version'])
native_task_definitions, custom_task_definitions = load_task_definitions()
task_definitions = {**native_task_definitions, **custom_task_definitions}

# Create columns for the buttons
col1, col2, col3, col4 = st.columns(4)

# UI for creating custom task
if 'create_task' not in st.session_state:
    st.session_state['create_task'] = False
with col1:
    if st.button('Create Custom Task'):
        st.session_state.create_task = not st.session_state.create_task
if st.session_state.create_task:
    with st.form("create_task_form"):
        new_task_name = st.text_input("Task Name")
        new_task_inputs = st.text_area("Inputs (comma-separated)")
        new_task_outputs = st.text_area("Outputs (comma-separated)")
        submitted = st.form_submit_button("Submit Task")
        if submitted:
            if new_task_name and new_task_name not in custom_task_definitions:
                create_task(new_task_name, custom_task_definitions, new_task_inputs, new_task_outputs,
                            workflow['alias'],
                            workflow['version'], flow_definition)
                st.session_state.create_task = False
                st.rerun()
            else:
                st.error("Task name is required or already exists.")

# UI for adding native task
if 'add_native_task' not in st.session_state:
    st.session_state['add_native_task'] = None
with col2:
    if st.button('Create Native Task'):
        st.session_state.add_native_task = not st.session_state.add_native_task

if st.session_state.add_native_task:
    with st.form("create_native_task_form"):
        new_task_name = st.text_input("Task Name")
        native_task = st.selectbox("Native Task", list(native_task_definitions.keys()))
        if st.form_submit_button("Submit Task"):
            if new_task_name and new_task_name not in custom_task_definitions:
                add_native_task(new_task_name, native_task, workflow['alias'], workflow['version'], flow_definition)
                st.session_state.add_native_task = False
                st.rerun()
            else:
                st.error("Task name is required or already exists.")

# UI for workflow arguments
st.sidebar.title("Workflow Arguments")
st.sidebar.json(flow_definition.get("workflow_args", []))
alias_name = st.sidebar.text_input("Alias for Workflow Argument", key="workflow_arg_alias")
if st.sidebar.button("Add new Workflow Argument"):
    add_workflow_args(alias_name, workflow['alias'], workflow['version'], flow_definition)
    st.sidebar.success(f"New workflow argument added successfully!")
    st.rerun()
if st.sidebar.button("Remove selected Workflow Argument"):
    remove_workflow_args(alias_name, workflow['alias'], workflow['version'], flow_definition)
    st.sidebar.success("Workflow argument removed successfully!")
    st.rerun()

# UI for the graph
nodes = []
edges = []
task_nodes = flow_definition["task_instances"]
levels, level_spacing = determine_levels(task_nodes)
all_task_names = list(task_nodes.keys())

for task_name, task_info in flow_definition["task_instances"].items():
    inputs = ", ".join([inp['alias'] for inp in task_definitions.get(task_info['type'], {}).get('inputs', [])])
    outputs = ", ".join([out['alias'] for out in task_definitions.get(task_info['type'], {}).get('outputs', [])])
    input_overrides = ", ".join(
        [inp for inp in flow_definition['task_instances'][task_name].get('input_overrides', {})])
    label = f"{task_name}"
    tooltip = f"Inputs: {inputs}\nOutputs: {outputs}\nInput Overrides: {input_overrides}"
    level = levels[task_name]
    task_category = "Custom" if task_name in custom_task_definitions else "Native"
    shape = "dot" if task_category == "Custom" else "diamond"
    color = "lightblue" if task_category == "Custom" else "lightgreen"
    nodes.append(
        Node(id=task_name, label=label, shape=shape, color=color, size=50, x=level_spacing[level].pop(0),
             y=level * 150,
             title=tooltip))

    for next_task in task_info.get("to", []):
        edges.append(Edge(source=task_name, target=next_task, type="STRAIGHT"))

# Configuration for agraph
config = Config(
    height=900,
    width='100%',
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor='#88c999',
    collapsible=True,
    node={'labelProperty': 'label', 'font_size': 20},
    link={'labelProperty': 'label', 'renderLabel': True},
    staticGraph=True,
    physics={
        "solver": 'barnesHut',
        "hierarchical": False
    }
)

# Display the graph
selection = agraph(nodes=nodes, edges=edges, config=config)

if selection:
    task_info = task_nodes[selection]
    selected_task = st.sidebar.selectbox("Select Task", all_task_names, index=all_task_names.index(selection))
    if selected_task:
        task_info = task_nodes[selected_task]
        task_details = task_definitions.get(task_info['type'], {})

        # UI for add/remove Inputs, Outputs
        for detail_key in ['inputs', 'outputs']:
            st.sidebar.title(f"{detail_key.capitalize()} Management")
            st.sidebar.json(task_details.get(detail_key, []))

            alias_name = st.sidebar.text_input(f"Alias for {detail_key[:-1]}", key=f"{detail_key}_alias")
            item_details = {"alias": alias_name}
            button_label = f"Add new {detail_key[:-1]}"
            if st.sidebar.button(button_label):
                if selected_task in list(native_task_definitions.keys()):
                    st.sidebar.error(f"Cannot add {detail_key} to a native task.")
                else:
                    add_item(task_details, detail_key, item_details, custom_task_definitions, selected_task)

            aliases = [item['alias'] if 'alias' in item else f"{item['key']}:{item['value']}" for item in
                       task_details.get(detail_key, [])]
            item_to_remove = st.sidebar.selectbox(f"Select {detail_key[:-1]} to remove", aliases,
                                                  key=f"{detail_key}_remove")
            if st.sidebar.button(f"Add borrower_package to {detail_key[:-1]}"):
                add_input_override(selected_task, workflow['alias'], workflow['version'], flow_definition)

            if st.sidebar.button(f"Remove selected {detail_key[:-1]}"):
                if selected_task in list(native_task_definitions.keys()):
                    st.sidebar.error(f"Cannot remove {detail_key} from a native task.")
                else:
                    task_details[detail_key] = [item for item in task_details[detail_key] if
                                                item['alias'] != item_to_remove]
                    task_definitions[selected_task] = task_details
                    save_task_definitions(custom_task_definitions)
                    st.sidebar.success(f"{detail_key[:-1].capitalize()} removed successfully!")
                    st.rerun()

        # UI for Delete Task
        if 'confirm_delete' not in st.session_state:
            st.session_state['confirm_delete'] = None
        with col4:
            if st.button('Delete Task', key="delete_task", type="primary"):
                if st.session_state.confirm_delete == selected_task:
                    if selected_task in custom_task_definitions:
                        delete_task(selected_task, custom_task_definitions, flow_definition, workflow)
                        st.session_state.confirm_delete = None  # Reset the confirmation state
                        st.rerun()
                    else:
                        remove_native_task(selected_task, workflow['alias'], workflow['version'], flow_definition)
                        st.session_state.confirm_delete = None
                        st.rerun()
                else:
                    st.session_state.confirm_delete = selected_task
                    st.warning(
                        f"Are you sure you want to delete '{selected_task}'? Click 'Delete Task' again to confirm.")

    # UI for edge management
    st.sidebar.title("Manage Edges")
    source_task = st.sidebar.selectbox("Source Task", all_task_names, index=all_task_names.index(selection))
    target_task = st.sidebar.selectbox("Target Task", all_task_names, index=all_task_names.index(selection))
    if st.sidebar.button("Add Edge"):
        update_edges('add', source_task, target_task, workflow['alias'], workflow['version'], flow_definition)
        st.rerun()
    if st.sidebar.button("Remove Edge"):
        update_edges('remove', source_task, target_task, workflow['alias'], workflow['version'], flow_definition)
        st.rerun()
