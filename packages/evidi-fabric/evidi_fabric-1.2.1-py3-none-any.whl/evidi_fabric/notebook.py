import ast
import base64
import json
import re
import sempy.fabric as fabric
import time
from uuid import UUID
from evidi_fabric.fs import get_table_path, resolve_workspace_id


def get_destination_matches(tree, notebook_content: str):
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call): #without type hints
            if isinstance(node.func, ast.Attribute) and node.func.attr == "forPath":
                try:
                    if isinstance(node.args[1], ast.Name):
                        # input is a variable. Look up its value!
                        matches.append(node.args[1].id)
                    elif isinstance(node.args[1], ast.Constant):
                        matches.append(f"'{node.args[1].s}'")
                except AttributeError:
                    pattern_forPath = r"DeltaTable\.forPath\(spark, (f\".*?\"|f'.*?'|\".*?\"|'.*?')"
                    matches.extend(re.findall(pattern_forPath, notebook_content))

            elif isinstance(node.func, ast.Attribute) and node.func.attr == "save":
                try:
                    keyword = node.func.value.args[0].s
                    value = node.func.value.args[1]
                    if keyword == "path":
                        if isinstance(value, ast.Name):
                            matches.append(value.id)
                        elif isinstance(value, ast.Constant):
                            matches.append(f"'{value.s}'")
                except AttributeError:
                    # Falling back to regex
                    # pattern_save = r"\.write\.save\((.*?)(?:,|\))"
                    pattern_save = r"\.write\.save\((f\".*?\"|f'.*?'|\".*?\"|'.*?')"
                    matches.extend(re.findall(pattern_save, notebook_content))

        if isinstance(node, ast.Expr): #with type hints
            if isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "forPath":
                try:
                    if isinstance(node.value.args[1], ast.Name):
                        # input is a variable. Look up its value!
                        matches.append(node.value.args[1].id)
                    elif isinstance(node.value.args[1], ast.Constant):
                        matches.append(f"'{node.value.args[1].s}'")
                except AttributeError:
                    pattern_forPath = r"DeltaTable\.forPath\(spark, (f\".*?\"|f'.*?'|\".*?\"|'.*?')"
                    matches.extend(re.findall(pattern_forPath, notebook_content))
            elif isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "save":
                try:
                    keyword = node.value.func.value.args[0].s
                    value = node.value.func.value.args[1]
                    if keyword == "path":
                        if isinstance(value, ast.Name):
                            matches.append(value.id)
                        elif isinstance(value, ast.Constant):
                            matches.append(f"'{value.s}'")
                except AttributeError:
                    # Falling back to regex
                    # pattern_save = r"\.write\.save\((.*?)(?:,|\))"
                    pattern_save = r"\.write\.save\((f\".*?\"|f'.*?'|\".*?\"|'.*?')"
                    matches.extend(re.findall(pattern_save, notebook_content))


    matches_unique = list(set(matches))
    return matches_unique


def find_destination_paths(notebook_content: str) -> list[str]:
    # Parse the code to get the AST
    tree = ast.parse(notebook_content)

    # Create a dictionary to store variable assignments
    variables = get_all_variable_assignments_in_notebook(notebook_content)

    matches = get_destination_matches(tree, notebook_content)

    destination_paths = []
    for match in matches:
        try:
            destination_path = _get_path_from_match(match, tree, variables)
            destination_paths.append(destination_path)
        except:
            pass

    if not destination_paths:
        print("No match found")

    return destination_paths


def _find_keyword_arguments_in_get_table_path(node, variables: dict[str, str]):
    """
    Find the keyword arguments in the get_table_path function call
    """
    table_name = None
    lakehouse = None

    for keyword in node.value.keywords:
        if keyword.arg == "table_name":
            if isinstance(keyword.value, ast.Constant):
                table_name = keyword.value.s
            elif isinstance(keyword.value, ast.Name):
                table_name = variables.get(keyword.value.id)
        elif keyword.arg == "lakehouse":
            if isinstance(keyword.value, ast.Constant):
                lakehouse = keyword.value.s
            elif isinstance(keyword.value, ast.Name):
                lakehouse = variables.get(keyword.value.id)
    return table_name, lakehouse


def _find_positional_arguments_in_get_table_path(
    node, variables: dict[str, str], lakehouse: str = None, table_name: str = None
) -> tuple[str, str]:
    """
    Find the positional arguments in the get_table_path function call
    """

    if not table_name:
        try:
            # Looking up variable values
            table_name = variables.get(node.value.args[0].id)
        except AttributeError:
            # No variables, assuming string values
            table_name = node.value.args[0].value
        except IndexError:
            raise IndexError("No table name found")

    if not lakehouse:
        try:
            # Looking up variable values
            lakehouse = variables.get(node.value.args[1].id)
        except AttributeError:
            # No variables, assuming string values
            lakehouse = node.value.args[1].value

    return table_name, lakehouse


def _extract_path_from_get_table_path(node, variables: dict[str, str]) -> str:
    """
    Evaluate the get_table_path function call and extract the table path
    """

    # Check for keyword arguments
    table_name, lakehouse = _find_keyword_arguments_in_get_table_path(node, variables)

    # Check for positional arguments if keyword arguments are not found
    if not table_name or not lakehouse:
        table_name, lakehouse = _find_positional_arguments_in_get_table_path(node, variables, lakehouse, table_name)

    path = get_table_path(table_name=table_name, lakehouse=lakehouse)

    return path


def _get_args_from_f_string(parameter_value: str) -> list[str]:
    """
    Get the arguments from an f-string
    """
    n_arguments = len(parameter_value.split("{")) - 1
    args = []
    for i in range(n_arguments):
        arg = parameter_value.split("{")[i + 1].split("}")[0]
        args.append(arg)
    return args


def _get_args_from_string(string: str) -> list[str]:
    """
    Get the arguments from a string
    """
    args = string.split(".")
    return args


def _get_path_from_string(string: str) -> str:
    """
    Get the source path from a string
    """
    is_path: str = "abfss" == string[:4]
    if is_path:
        path = string
    else:
        args = _get_args_from_string(string)
        lakehouse = args[0]
        table_name = args[1]
        path = get_table_path(table_name=table_name, lakehouse=lakehouse)
    return path


def _convert_f_string_to_lakehouse_table_format(fstring: str, variables: dict[str, str]) -> str:
    """
    The goal of this function is to convert any f-string path to a f"{lakehouse}.{table_name}" format
    """
    if "mssparkutils.lakehouse.get" in fstring:
        args = _get_args_from_f_string(fstring)
        lakehouse = args[0].split("(")[1].split(")")[0]
        if _is_string(lakehouse):
            lakehouse = lakehouse.strip("'\"")
        else:
            lakehouse = _get_variable_assignment(lakehouse, variables)

            # table_name must be a part of the string
        if len(args) == 1:
            table_name = fstring.split("Tables/")[-1]
        else:
            table_name = args[1]
            if _is_string(table_name):
                table_name = table_name.strip("'\"")
            else:
                table_name = _get_variable_assignment(table_name, variables)
        return f"{lakehouse}.{table_name}"

    args = _get_args_from_f_string(fstring)
    fstring = fstring[1:].strip("'\"").replace("'''", "").replace('"""', "")
    for arg in args:
        value = _get_variable_assignment(arg, variables)
        fstring = fstring.replace(f"{{{arg}}}", value)
    return fstring


def _get_path_from_f_string(parameter_value: str, variables: dict[str, str]) -> str:
    """
    Get the source path from an f-string
    """
    string = _convert_f_string_to_lakehouse_table_format(parameter_value, variables)
    path = _get_path_from_string(string)
    return path


def _get_variable_assignment(variable: str, variables: dict[str, str]) -> str:
    """
    Get variable assignment from a variable
    """
    try:
        return [value for key, value in variables.items() if key == variable][0]
    except IndexError:
        raise IndexError(f"Variable {variable} is not assigned")


def get_all_variable_assignments_in_notebook(notebook_content: str):
    """
    Get all variables in a notebook
    """
    tree = ast.parse(notebook_content)
    variables = {}

    # Find variable assignments
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                variable_name = node.targets[0].id
                if isinstance(node.value, ast.Constant):
                    variable_value = node.value.value
                    variables[variable_name] = variable_value
                elif isinstance(node.value, ast.Name):
                    variable_value = variables.get(node.value.id)
                    if variable_value:
                        variables[variable_name] = variable_value
                elif isinstance(node.value, ast.JoinedStr):
                    fstring = "f'"
                    for value in node.value.values:
                        if isinstance(value, ast.FormattedValue):
                            variable_value = value.value.id
                            fstring += f"{{{variable_value}}}"
                        elif isinstance(value, ast.Constant):
                            fstring += value.value
                    fstring += "'"
                    variables[variable_name] = fstring
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                variable_name = node.target.id
                if isinstance(node.value, ast.Constant):
                    variable_value = node.value.value
                    variables[variable_name] = variable_value
                elif isinstance(node.value, ast.Name):
                    variable_value = variables.get(node.value.id)
                    if variable_value:
                        variables[variable_name] = variable_value
                elif isinstance(node.value, ast.JoinedStr):
                    fstring = "f'"
                    for value in node.value.values:
                        if isinstance(value, ast.FormattedValue):
                            variable_value = value.value.id
                            fstring += f"{{{variable_value}}}"
                        elif isinstance(value, ast.Constant):
                            fstring += value.value
                    fstring += "'"
                    variables[variable_name] = fstring
            
                

    return variables


def _is_string(value: str) -> bool:
    """
    Check if a value is a string
    """
    return "'" in value or '"' in value


def _is_f_string(value: str) -> bool:
    """
    Check if a value is an f-string
    """
    return value[:2] == "f'" or value[:2] == 'f"'


def _get_path_from_match(match: str, tree: ast.AST, variables: dict[str, str]) -> str:
    """
    Get the source path from a match. Match can be a f-string, string or a variable,
    basically whatever the designated function was called with
    """
    parameter_value = match.strip()
    if _is_string(parameter_value):
        if _is_f_string(parameter_value):
            path = _get_path_from_f_string(parameter_value, variables)
        else:
            # If it's a string, then it must be a path!
            path = parameter_value.strip("'\"")
        return path
    try:
        # Check if the variable is assigned using an assignment
        value = _get_variable_assignment(variable=parameter_value, variables=variables)
        if _is_f_string(value):
            path = _get_path_from_f_string(value, variables)
        elif _is_string(value):
            path = _get_path_from_string(value)
        else:
            raise NotImplementedError("Not implemented yet")
        return path

    except IndexError:
        # Check if the variable is assigned using get_table_path or get_file_path
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == parameter_value
            ):
                # Check if the variable is assigned using get_table_path or get_file_path
                if (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id in ["get_table_path", "get_file_path"]
                ):
                    path = _extract_path_from_get_table_path(node, variables)
                    return path
            elif (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == parameter_value
            ):
                # Check if the variable is assigned using get_table_path or get_file_path
                if (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id in ["get_table_path", "get_file_path"]
                ):
                    path = _extract_path_from_get_table_path(node, variables)
                    return path
        raise IndexError(f"Variable {parameter_value} is not assigned")


def get_source_matches(tree, notebook_content: str):
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in ["load", "table"]:
                try:
                    if isinstance(node.args[0], ast.Name):
                        # input is a variable. Look up its value!
                        matches.append(node.args[0].id)
                    elif isinstance(node.args[0], ast.Constant):
                        matches.append(f"'{node.args[0].s}'")
                except AttributeError:
                    source_pattern = r"spark\.read(?:\.format\(.delta.\))?\.(?:load|table)\((.*)\)"
                    matches.extend(re.findall(source_pattern, notebook_content))

    matches_unique = list(set(matches))
    return matches_unique


def find_source_paths(notebook_content: str):
    # Parse the code to get the AST
    tree = ast.parse(notebook_content)

    # Create a dictionary to store variable assignments
    variables = get_all_variable_assignments_in_notebook(notebook_content)

    # Search for all occurrences of the source_pattern in the code
    matches = get_source_matches(tree, notebook_content)

    source_paths = []
    for match in matches:
        try:
            source_path = _get_path_from_match(match, tree, variables)
            source_paths.append(source_path)
        except:
            pass

    if not source_paths:
        print("No match found")

    return source_paths


def get_notebook_content(notebook_name: str, workspace: str | UUID | None = None):
    """
    Retrieving the content from a notebook from its id.
    Note: If workspace is not specified, the current workspace is used
    """
    client = fabric.FabricRestClient()
    df_notebooks = fabric.list_items("Notebook")
    workspace_id = resolve_workspace_id(workspace)

    # notebook_name=df_notebooks.loc[df_notebooks["Id"]==notebook_id, "Display Name"].iloc[0]
    notebook_id = df_notebooks.loc[
        ((df_notebooks["Display Name"] == notebook_name) & (df_notebooks["Workspace Id"] == workspace_id)), "Id"
    ].iloc[0]

    print(f"{str(notebook_id)}: {notebook_name}")

    response = client.post(f"/v1/workspaces/{workspace_id}/items/{notebook_id}/getDefinition")
    if response.status_code == 202:
        # Output is not ready yet. Waiting for the request to finish
        status = "Running"
        while status == "Running":
            wait_secs = int(response.headers["Retry-After"]) / 40  # End point suggest to wait REDICOUOUSLY long time
            time.sleep(wait_secs)
            response_status = client.get(response.headers["location"])
            status = json.loads(response_status._content.decode())["status"]
        response = client.get(response_status.headers["Location"])
    payload_encoded = json.loads(response.content)["definition"]["parts"][0]["payload"]
    notebook_content = base64.b64decode(payload_encoded).decode()
    return notebook_content


def get_cleaned_notebook_content(notebook_name: str, workspace: str | UUID | None = None):
    """
    Retrieving the cleaned content from a notebook from its id.
    Note: If workspace is not specified, the current workspace is used
    """
    notebook_content = get_notebook_content(notebook_name, workspace)
    notebook_content_cleaned = clean_notebook_content(notebook_content)
    return notebook_content_cleaned


def clean_notebook_content(notebook_content: str) -> str:
    """
    Clean the notebook content from the cell magic commands
    """
    lines = notebook_content.split("\n")
    # Filter out lines that start with '%'
    filtered_lines = [line for line in lines if not line.strip().startswith("%") and not line.strip().startswith("#")]

    # Replace !pip install with pass (if in try, except block) else remove
    filtered_lines = ["    pass" if line[:16] == "    !pip install" else line for line in filtered_lines]
    filtered_lines = ["\tpass" if line[:13] == "\t!pip install" else line for line in filtered_lines]
    filtered_lines = [line for line in filtered_lines if not line.strip()[:12] == "!pip install"]
    # Join the filtered lines back into a single string
    cleaned_notebook_content = "\n".join(filtered_lines)
    return cleaned_notebook_content


def get_notebook_names(workspace: str | UUID | None = None) -> list[str]:
    """
    Get the names of the notebooks in a workspace
    """
    df_notebooks = fabric.list_items("Notebook")
    workspace_id = resolve_workspace_id(workspace)
    notebook_names = df_notebooks.loc[df_notebooks["Workspace Id"] == workspace_id, "Display Name"].to_list()
    return notebook_names


if __name__ == "__main__":
    notebook_content = """lakehouse_silver="Sealing_System_Silver"
lakehouse_gold="Sealing_System_Gold"

org_table="CRM_opportunity"
new_table="dimUser"

from pyspark.sql import functions as F
from pyspark.sql.functions import when, col

lakehouse = "lakehouse_silver"

path=get_table_path(table_name=org_table, lakehouse=lakehouse_gold)

df = spark.read.load(path)

destination_table_path=get_table_path(table_name=new_table, lakehouse=lakehouse_gold)
#display(df)
try:
    #Delta loading
    delta_table = DeltaTable.forPath(spark, destination_table_path)
    delta_table.alias('target') \
    .merge(
        source=df.alias('source'),
        condition=["source.datetime_utc = target.datetime_utc"]
    ) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()
except:
    #Full loading
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .option("path", destination_table_path) \
        .save()
"""
    # 	notebook_content = """no_one_cares = "idiot"
    # lakehouse="silver"
    # table_name="customer"
    # table_path = f"{lakehouse}.customers"#= get_table_path("customers", lakehouse="lakehouse_silver")

    # spark.read.format('delta').load(table_path)
    # spark.read.load(table_path)

    # destination_table_path = get_table_path("customers", lakehouse="lakehouse_silver")

    # try:
    #     #Delta loading
    #     delta_table = DeltaTable.forPath(spark, destination_table_path)
    #     delta_table.alias('target') \
    #     .merge(
    #         source=df.alias('source'),
    #         condition=merge_conditions
    #     ) \
    #     .whenMatchedUpdateAll() \
    #     .whenNotMatchedInsertAll() \
    #     .execute()
    # except:
    #     #Full loading
    #     df.write \
    #         .format("delta") \
    #         .mode("overwrite") \
    #         .option("overwriteSchema", "true") \
    #         .option("path", destination_table_path) \
    #         .save()
    # """

    #     notebook_content = """# Loading the Project delta table from the connected Bronze lakehouse
    # bronze_df = spark.read.format("delta").load("Tables/Project")
    # # Loading the Project delta table from the ABFS path
    # bronze_df = spark.read.format("delta").load("abfss://XXXXXX@onelake.dfs.fabric.microsoft.com/XXXXXX/Tables/Project")
    # # Loading the project delta table from the ABFS path fetched automatically through the mssparkutils package (based on the workspace the notebook is in)
    # bronze_df = spark.read.format("delta").load(f"{mssparkutils.lakehouse.get('GK_Bronze').abfsPath}/Tables/Project")
    # # Writing the Project delta table back to the Bronze lakehouse (the lacehouse has to be connected to use this code)
    # bronze_df.write.format("delta").mode("overwrite").saveAsTable("Project")

    # # Writing the Project delta table using generic strings fethed through mssparkutils. If the table exists the code uses Upsert.
    # silver_table_name = "prosjekt"
    # if mssparkutils.fs.exists(f"{mssparkutils.lakehouse.get('GK_Silver').abfsPath}/Tables/{silver_table_name}"):
    #     print("upserting")
    #     from delta.tables import DeltaTable
    #     silver_table = DeltaTable.forPath(spark, f"{mssparkutils.lakehouse.get('GK_Silver').abfsPath}/Tables/{silver_table_name}")
    #     (silver_table.alias("silver")
    #         .merge(
    #         bronze_df.alias("bronze"),
    #             "silver.surrogateKey = bronze.surrogateKey"
    #         )
    #         .whenMatchedUpdateAll()  # Update existing rows
    #         .whenNotMatchedInsertAll()  # Insert new rows
    #         .execute()
    #     )
    # else:
    #     print("overwriting")
    #     bronze_df.write.save(f"{mssparkutils.lakehouse.get('GK_Silver').abfsPath}/Tables/{silver_table_name}", format="delta", mode="overwrite")
    # 	"""

    # notebook_content="""# Fabric notebook source\n\n\n# CELL ********************\n\nimport json\nimport pandas as pd\n\nfrom azure.data.tables import TableClient\nfrom json import JSONDecodeError\nfrom pyspark.sql.types import FloatType, StructType, StructField, StringType, ArrayType, BooleanType,TimestampType,DateType, MapType, IntegerType\nfrom pyspark.sql import functions as F\nfrom pyspark.sql.functions import col,when,lit,to_date,col,split,to_timestamp,from_json,explode,first,monotonically_increasing_id,substring,schema_of_json,regexp_extract\n\nfrom evidi_fabric.fs import get_table_path\n\n# CELL ********************\n\nlakehouse_bronze="Bronze"\nlakehouse_silver="Silver"\n\nsource_table="Configurations"\ndestination_table="Configurations"\n\n# CELL ********************\n\ntable_path = get_table_path(table_name=source_table,lakehouse=lakehouse_bronze)\ndf_source = spark.read.load(table_path)\n\n# CELL ********************\n\ndf_filtered = df_source.filter(col("ConfigurationData").isNotNull() &\n                      (col("ConfigurationData") != "") &\n                      (col("ConfigurationData") != "[]") &\n                      (col("ConfigurationData") != "configurationData"))\n\n# CELL ********************\n\n# #TODO: Why is ConfigurationData_value not exploded??\n# # MUST BE DELETED\n# df_filtered=df_filtered.filter(col("RowKey")==\'26cc9d9a-37ba-4016-bbe4-451d394369da\')\n# display(df_filtered)\n\n# MARKDOWN ********************\n\n# ### Unfold JSON columns\n# 1. **Convert spark dataframe to pandas**: unfortunately, spark currently do not support infer schema of a JSON column. Fortunately, pandas does\n# 2. Convert ```ConfigurationData``` to columns and explode the rows\n# 3. Filter ```value``` to the rows containing valid json and convert it to columns and explode the rows and union it on to the dataframe where ```value``` was not valid json\n# 4. iteratively, Filter the newly added columns from the above and convert it colums and explode the rows. Continue this to ALL json objects have been converted\n\n# CELL ********************\n\ndf_pd = df_filtered.toPandas()\n# json_pattern = r\'^\\s*\\{.*\\}\\s*$\'\n\njson_pattern = r\'^\\s*[\\{\\[].*[\\}\\]]\\s*$\'\n# Convert JSON strings to dictionaries\ncolumns=df_pd.columns\n\nwhile True:\n    newly_added_columns=[]\n    for col in columns:\n        print(col)\n        df_non_empty_rows = df_pd[~df_pd[col].isna()]\n        df_empty_rows = df_pd[df_pd[col].isna()]\n        try:\n            df_pd_json = df_non_empty_rows[df_non_empty_rows[col].astype(str).str.contains(json_pattern)]\n        except AttributeError:\n            continue\n\n        if df_pd_json.empty:\n            continue\n\n        df_pd_non_json=df_non_empty_rows[~df_non_empty_rows[col].astype(str).str.contains(json_pattern)]\n        try:\n            try:\n                df_pd_json[col] = df_pd_json[col].apply(json.loads)\n            except TypeError:\n                #Possibly already a json object!\n                pass\n\n            # Explode to more rows\n            df_exploded = df_pd_json.explode(col).reset_index() \n\n            # Extracting columns\n            df_normalize = pd.json_normalize(df_exploded[col]) \n\n            # Concatenating together\n            df_concatenated = pd.concat([df_exploded, df_normalize], axis=1)\n            \n            # remove_col=["index",col]\n            remove_col=["index"]\n            df_concatenated.drop(remove_col,axis=1,inplace=True)\n\n            # Union \n            df_pd = pd.concat([df_concatenated,df_pd_non_json,df_empty_rows], axis=0)\n\n            existing_cols=df_pd_non_json.columns\n            new_cols=df_concatenated.columns\n\n            newly_added_columns_temp = list(set(new_cols)-set(existing_cols))\n\n            rename_cols={f"{new_col}": f"{col}_{new_col}" for new_col in newly_added_columns_temp}\n\n            df_pd=df_pd.rename(columns=rename_cols)\n\n            new_col_names=list(rename_cols.values())\n            newly_added_columns.extend(new_col_names)\n            \n        except JSONDecodeError:\n            continue\n        except TypeError:\n            continue\n    columns=newly_added_columns\n    if not columns:\n        break\n\n\n# MARKDOWN ********************\n\n# ### Remove upstream columns\n# Removing all json columns, where data have been extracted and transformed into seperate columns. This is done by the following procedure:\n# 1. Identifying the downstream columns (e.g. columns that start with another column\'s name and a underscore)\n# 2. Removing all columns that has a downstream column\n\n# CELL ********************\n\n# downstream_columns = {}\n# for original_col in df_afterjson.columns:\n#     downstream_columns[original_col] = [col for col in df_afterjson.columns if col.startswith(original_col+"_") and col!=original_col]\n\n# cols_to_drop=[col for col in downstream_columns.keys() if downstream_columns[col] and col!="ConfigurationData"]\n# df_pd.drop(cols_to_drop, axis=1, inplace=True)\n\n# MARKDOWN ********************\n\n# ### Replace NaNs with Nulls\n# Otherwise, spark will intrepret the NaNs as string values\n\n# CELL ********************\n\ndf_pd_null=df_pd.where(pd.notnull(df_pd), None)\n\n# MARKDOWN ********************\n\n# ### Convert from pandas back to spark\n# while respecting the datatypes. Here we assume that all "unknown" columns are strings\n\n# CELL ********************\n\ntimestamp_cols=["ModifiedDate"]\nint_cols=[]\nfloat_cols=["ConfigurationData_value_codes_codeIndex"]\n\nsub_schema=[]\nfor col in df_pd_null.columns:\n    if col in float_cols:\n        sub_schema.append(StructField(col, FloatType(), True))\n    elif col in int_cols:\n        sub_schema.append(StructField(col, IntegerType(), True))\n    elif col in timestamp_cols:\n        sub_schema.append(StructField(col, TimestampType(), True))\n    else:\n        sub_schema.append(StructField(col, StringType(), True))\n\nschema = StructType(\n    sub_schema\n)\n\ndf_spark=spark.createDataFrame(df_pd_null,schema)\n\n# MARKDOWN ********************\n\n# ### Casting columns that cannot be initially understood by spark\n# In the below case, the float type includes "nan" value, which cannot be interpret as a integer. Hence, first it is kept as a float type in pandas, then a float type in spark and then casted to a integer, after all nans are being replaced with NULLS \n\n# CELL ********************\n\ndf_converted_datatypes=df_spark\ndf_converted_datatypes = df_converted_datatypes.replace(float(\'nan\'), None)\n\nconvert_to_int_cols=["ConfigurationData_value_codes_codeIndex"]\n\nfor col in convert_to_int_cols:\n    if col in df_converted_datatypes.columns:\n        df_converted_datatypes = df_converted_datatypes.withColumn(col, df_converted_datatypes[col].cast(IntegerType()))\n\n# MARKDOWN ********************\n\n# ## Split column\n# 1. Split of column (variableId) into multiple columns split by ```.```\n# 2. Take a maximum 20 in case more ```.``` are included\n# 3. In case no more than ```n<20``` ```.``` is included the code breaks\n# 4. Drop of column\n\n# CELL ********************\n\ndf_spark_split=df_spark.withColumn("split",split(df_spark[\'ConfigurationData_variableId\'], \'\\.\'))\n\ni=0\nwhile i<20:\n    df_spark_split = df_spark_split.withColumn(f\'level_{i}\',df_spark_split["split"].getItem(i))\n    number_of_not_null_rows = df_spark_split.filter(df_spark_split[f\'level_{i}\'].isNotNull()).count()\n    if number_of_not_null_rows == 0:\n        df_spark_split = df_spark_split.drop(f\'level_{i}\')\n        break\n    i+=1\n\n\ndf_spark_dropped = df_spark_split.drop("split")\n\n# MARKDOWN ********************\n\n# ## Creation of new field ```questionId```\n# 1. sort array of fields named level_* with desc\n# 2. use function ```coalesce``` to identify the highest level-field with values in it\n\n# CELL ********************\n\ncols=[f"{col}" for col in df_spark_dropped.columns if "level_" in col]\ncols.sort(reverse=True)\nquestionId=", ".join(cols)\n\nselect_statement = ["*",f"COALESCE({\', \'.join(cols)}) AS questionId"]\n\ndf = df_spark_dropped.selectExpr(*select_statement)\n\n# CELL ********************\n\ndestination_table_path = get_table_path(table_name=destination_table,lakehouse=lakehouse_silver)\n\ndf.write \\\n    .format("delta") \\\n    .mode("overwrite") \\\n    .option("overwriteSchema", "true") \\\n    .option("path", destination_table_path) \\\n    .save()\n"""
    # 	notebook_content="""table_name="silver.customer"
    # spark.read.load(table_name)"""
    # notebook_content="""silver_table_name = "prosjekt"\nbronze_df.write.save(f"{mssparkutils.lakehouse.get('GK_Silver').abfsPath}/Tables/{silver_table_name}", format="delta", mode="overwrite")"""
    # notebook_content="""silver_table_name = "prosjekt"\nspark.read.load(f"{mssparkutils.lakehouse.get('GK_Silver').abfsPath}/Tables/{silver_table_name}", format="delta", mode="overwrite")"""
    #     notebook_content = """from pyspark.sql.functions import col, concat_ws, row_number
    # from pyspark.sql import Window
    # from pyspark.sql.types import DateType, TimestampType
    # from delta.tables import DeltaTable

    # gk_bronz_path = mssparkutils.lakehouse.get("GK_Bronze").abfsPath
    # gk_silver_path = mssparkutils.lakehouse.get("GK_Silver").abfsPath

    # bronze_df = spark.read.format("delta").load(f"{gk_bronz_path}/Tables/Unit4_Customer")"""

    # notebook_content = '''\n\n\n\ntry:\n    import evidi_fabric\nexcept:\n    pass\n\nfrom evidi_fabric.fs import get_table_path\nfrom evidi_fabric.sql import get_table_name_and_alias, create_sql_views_from_sql\nfrom evidi_fabric.utils import get_config\n\nimport json\nfrom delta.tables import DeltaTable\nfrom pyspark.sql.functions import expr\nfrom typing import Dict, List\n\n\n\n\nlakehouse_silver="Silver"\nlakehouse_gold="Gold"\ndestination_table_name="FactSalesInvoiceTransactions" #DimCompany\n\n\nconfig = get_config(config_base, config_custom)[destination_table_name]\nprint(json.dumps(config, indent=2))\n\n\ncompanies=[key for key in config["companies"].keys()]\nfirst_iteration=True\n\nfor company in companies:\n    if "table" in config["companies"][company]["depends_on"][0]:\n        table, alias=get_table_name_and_alias(config["companies"][company]["depends_on"][0]["table"])\n        table_path=get_table_path(table_name=table, lakehouse=lakehouse_silver)\n        df_merged=spark.read.load(table_path).alias(alias)\n    elif "table_sql" in config["companies"][company]["depends_on"][0]:\n        table_sql=config["companies"][company]["depends_on"][0]["table_sql"]\n        create_sql_views_from_sql(sql=table_sql, lakehouse=lakehouse_silver)\n        alias=config["companies"][company]["depends_on"][0]["alias"]\n        df_merged=spark.sql(table_sql).alias(alias)\n    print(alias)\n\n    table_infos=config["companies"][company]["depends_on"][1:]\n    for table_info in table_infos:\n        if "table" in table_info.keys():\n            table, alias=get_table_name_and_alias(table_info["table"])\n            table_path=get_table_path(table_name=table, lakehouse=lakehouse_silver)\n            df2=spark.read.load(table_path).alias(alias)\n        elif "table_sql" in table_info.keys():\n            table_sql=table_info["table_sql"]\n            create_sql_views_from_sql(sql=table_sql, lakehouse=lakehouse_silver)\n            alias=table_info["alias"]\n            df2=spark.sql(table_sql).alias(alias)\n        else:\n            raise NotImplementedError("Neither \'table\' or \'table_sql\' was specified")\n            \n        print(alias)\n        join_clause=expr(table_info["join_clause"])\n        join_type=table_info["join_type"]\n        df_merged=df_merged.join(df2, join_clause, how=join_type)\n\n    df_selected_cols=df_merged.selectExpr(*config["companies"][company]["columns"])\n    df_where=df_selected_cols.where(config["companies"][company]["where_clause"])\n    \n    if first_iteration:\n        df = df_where\n        first_iteration=False\n    else:\n        df = df.union(df_where)\n\n\nkeys = config["primary_keys"]\npart_cols=[]\nzorder_cols=keys\ndf=df.sort(*keys)\n\n\ndestination_table_path:str=get_table_path(table_name=destination_table_name, lakehouse=lakehouse_gold)\n\n\nload_type=config["load_type"]\nif load_type=="FULL":\n    df.write \\\n        .format("delta") \\\n        .mode("overwrite") \\\n        .option("overwriteSchema", "true") \\\n        .option("path", destination_table_path) \\\n        .partitionBy(part_cols) \\\n        .option("zOrderBy", zorder_cols) \\\n        .save()\n        \nelif load_type=="DELTA":\n    try:\n        delta_table = DeltaTable.forPath(spark, destination_table_path)\n        delta_table.alias(\'target\') \\\n        .merge(\n            source=df.alias(\'source\'),\n            condition=merge_condition\n        ) \\\n        .whenMatchedUpdateAll() \\\n        .whenNotMatchedInsertAll() \\\n        .execute()\n    except:\n        df.write \\\n            .format("delta") \\\n            .mode("overwrite") \\\n            .option("overwriteSchema", "true") \\\n            .option("path", destination_table_path) \\\n            .partitionBy(part_cols) \\\n            .option("zOrderBy", zorder_cols) \\\n            .save()\n'''
    # print(notebook_content)

    notebook_content = """#!/usr/bin/env python
# coding: utf-8

# ## STD_InventTransOrigin
# 
# New notebook


lakehouse_src = "Bronze"
lakehouse_dst:str = "Silver"
table_name:str = "inventtransorigin" 


# ## Read

path_df = get_table_path(table_name = table_name, lakehouse=lakehouse_src)
df_raw = spark.read.load(path_df)


# ## Write

destination_table_path:str=get_table_path(table_name=table_name, lakehouse=lakehouse_dst)


df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", destination_table_path) \
    .save()

destination_table_path2=get_table_path(table_name=table_name, lakehouse=lakehouse_dst)


df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", destination_table_path2) \
    .save()

"""
    notebook_content_cleaned = clean_notebook_content(notebook_content)
    source_paths = find_source_paths(notebook_content_cleaned)
    destination_paths = find_destination_paths(notebook_content_cleaned)
    print(f"Source paths: {source_paths}")
    print("stop")
