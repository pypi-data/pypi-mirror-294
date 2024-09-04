import streamlit as st
import datetime

def generate_repeating_field_group(keys, group_id, default_values=None):
    """
    Generate a repeating field group in Streamlit.

    Args:
        keys (dict): A dictionary defining the fields and their properties.
        group_id (str): A unique identifier for the field group.
        default_values (list, optional): Default values for the fields.

    Returns:
        list: A list of dictionaries containing the field values for each row.
    """
    # Initialize session state for rows if not already present
    if f"rows_{group_id}" not in st.session_state or not st.session_state[f"rows_{group_id}"]:
        if default_values:
            st.session_state[f"rows_{group_id}"] = [str(i) for i in range(len(default_values))]
        else:
            st.session_state[f"rows_{group_id}"] = []

    rows_collection = []

    def add_row():
        """Add a new row to the field group."""
        new_index = str(len(st.session_state[f"rows_{group_id}"]))
        st.session_state[f"rows_{group_id}"].append(new_index)

    def remove_row(row_id):
        """Remove a row from the field group."""
        st.session_state[f"rows_{group_id}"].remove(str(row_id))

    def generate_row(row_id, defaults=None):
        """Generate a single row of fields."""
        row_container = st.container()
        row_columns = row_container.columns((3, 1))
        field_group = {}

        def update_field(key):
            """Mark a field as changed in the session state."""
            st.session_state[f"{key}_{row_id}_{group_id}_changed"] = True

        for key, value in keys.items():
            field_type = value["type"]
            default_value = defaults.get(key, value["default"]) if defaults else value["default"]
            only_show_if = value.get("only_show_if", None)

            # Check if the field should be displayed
            if only_show_if:
                kwargs = only_show_if["kwargs"].copy()
                func = only_show_if["func"]
                for arg_key, arg_value in kwargs.items():
                    if isinstance(arg_value, str) and arg_value in field_group:
                        kwargs[arg_key] = field_group[arg_value]
                if not func(**kwargs):
                    continue  # Skip this field if the function returns False

            try:
                # Generate the appropriate Streamlit input widget based on the field type
                if field_type in [int, "int"]:
                    int_value = int(default_value) if default_value is not None else 0
                    field_group[key] = row_columns[0].number_input(key, value=int_value, step=1, 
                                                                   key=f"{key}_{row_id}_{group_id}",
                                                                   on_change=update_field, args=(key,))
                elif field_type in [float, "float"]:
                    float_value = float(default_value) if default_value is not None else 0.0
                    field_group[key] = row_columns[0].number_input(key, value=float_value, format="%.2f", 
                                                                   key=f"{key}_{row_id}_{group_id}",
                                                                   on_change=update_field, args=(key,))
                elif field_type in [str, "str"]:
                    field_group[key] = row_columns[0].text_input(key, value=str(default_value) if default_value is not None else "", 
                                                                 key=f"{key}_{row_id}_{group_id}",
                                                                 on_change=update_field, args=(key,))
                elif field_type == "choice":
                    choices = value["choices"]
                    field_group[key] = row_columns[0].selectbox(key, options=choices, 
                                                                index=choices.index(default_value), 
                                                                key=f"{key}_{row_id}_{group_id}",
                                                                on_change=update_field, args=(key,))
                elif field_type == "date":
                    if isinstance(default_value, str):
                        date_value = datetime.date.fromisoformat(default_value)
                    elif isinstance(default_value, datetime.date):
                        date_value = default_value
                    else:
                        date_value = datetime.date.today()
                    field_group[key] = row_columns[0].date_input(key, value=date_value, 
                                                                 key=f"{key}_{row_id}_{group_id}",
                                                                 on_change=update_field, args=(key,))
                elif field_type == "toggle_switch":
                    field_group[key] = row_columns[0].toggle(key, value=bool(default_value),
                                                             key=f"{key}_{row_id}_{group_id}",
                                                             on_change=update_field, args=(key,))
                elif field_type == "checkbox":
                    field_group[key] = row_columns[0].checkbox(key, value=bool(default_value),
                                                               key=f"{key}_{row_id}_{group_id}",
                                                               on_change=update_field, args=(key,))
                elif field_type == "slider":
                    min_value = float(value.get("min", 0))
                    max_value = float(value.get("max", 100))
                    step = value.get("step", 1)
                    field_group[key] = row_columns[0].slider(key, min_value=min_value, max_value=max_value, 
                                                             value=float(default_value), step=step,
                                                             key=f"{key}_{row_id}_{group_id}",
                                                             on_change=update_field, args=(key,))
                elif field_type == "range_slider":
                    min_value = float(value.get("min", 0))
                    max_value = float(value.get("max", 100))
                    step = value.get("step", 1)
                    if isinstance(default_value, (list, tuple)) and len(default_value) == 2:
                        default_range = (float(default_value[0]), float(default_value[1]))
                    else:
                        default_range = (min_value, max_value)
                    field_group[key] = row_columns[0].slider(key, min_value=min_value, max_value=max_value,
                                                             value=default_range, step=step,
                                                             key=f"{key}_{row_id}_{group_id}",
                                                             on_change=update_field, args=(key,))
                else:
                    raise ValueError(f"Invalid field type '{field_type}' for field '{key}'")
            except ValueError as e:
                st.error(f"Error in field '{key}': {str(e)}. Please check the field configuration and ensure the default value matches the specified type.")
            except TypeError as e:
                st.error(f"Type error in field '{key}': {str(e)}. Make sure the default value is compatible with the field type.")
            except Exception as e:
                st.error(f"Unexpected error in field '{key}': {str(e)}. Please review the field configuration and data.")

        # Add a delete button for each row
        row_columns[1].button("🗑️", key=f"del_{row_id}_{group_id}", on_click=remove_row, args=[row_id])
        return field_group

    # Add a button to add new rows
    menu = st.columns(2)
    with menu[0]:
        st.button("Add Item", on_click=add_row, key=f"add_item_{group_id}")

    # Generate rows based on the session state
    for row_index in st.session_state[f"rows_{group_id}"]:
        defaults = default_values[int(row_index)] if default_values and int(row_index) < len(default_values) else None
        row_data = generate_row(row_index, defaults)
        rows_collection.append(row_data)

    return rows_collection