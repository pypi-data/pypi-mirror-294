from colorama import Fore, Style
from sqlalchemy import Column, create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
import importlib.util
import os
import inspect

class MigrationSystem:
	def __init__(self, db_connection_path: str, model_paths: list) -> None:
		self.db_connection_path = db_connection_path
		self.model_paths = model_paths

	def _extract_db_url_from_connection(self, file_path: str) -> None:
		# Load the module from the file path
		module_name = os.path.splitext(os.path.basename(file_path))[0]
		spec = importlib.util.spec_from_file_location(module_name, file_path)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		
		# Extract the database URL from the `Connection` object
		if hasattr(module, 'Connection'):
			connection = module.Connection
			# Extracting the database URL from the connection object
			# This depends on the actual implementation of `connection` in `libmercury.db`
			if hasattr(connection, 'Engine'):
				db_url = connection.Engine.url
				return str(db_url)
			else:
				raise AttributeError("The 'Connection' object does not have an 'engine' or 'url' attribute.")
		else:
			raise AttributeError("The module does not have a 'Connection' object.")


	def _generate_file(self, autogenerate_table, message) -> None:
		python_files = []
	
		for file in os.listdir("src/cargo/migrations"):
			if file.endswith('.py') and os.path.isfile(os.path.join("src/cargo/migrations", file)):
				try:
					python_files.append(int(file[:-3]))
				except ValueError:
					pass
	
		name = max(python_files) + 1 if python_files else 1
	
		upgrade_commands = []
		downgrade_commands = []
	
		# Separate tables with and without foreign key dependencies
		fk_tables = []
		no_fk_tables = []
	
		for new_table in autogenerate_table.get("new_tables", []):
			if any(col_info.get("foreign_keys") for col_info in new_table["columns"].values()):
				fk_tables.append(new_table)
			else:
				no_fk_tables.append(new_table)
	
		# First stage: Handle tables without foreign keys
		for new_table in no_fk_tables:
			table_name = new_table["name"]
			columns = []
	
			for col_name, col_info in new_table["columns"].items():
				col_type = col_info["type"]
				col_nullable = col_info["nullable"]
				col_primary_key = col_info["primary_key"]
	
				column_def = f"Column('{col_name}', {col_type}"
				if col_primary_key:
					column_def += f", primary_key={col_primary_key}"
				column_def += f", nullable={col_nullable}"
				column_def += ")"
	
				columns.append(column_def)
	
			columns_str = ", \n\t\t".join(columns)
			upgrade_commands.append(f"wrapper.create_table('{table_name}', [\n\t\t{columns_str}\n\t])")
			downgrade_commands.append(f"wrapper.delete_table('{table_name}')")
	
		# Second stage: Handle tables with foreign keys
		for new_table in fk_tables:
			table_name = new_table["name"]
			columns = []
	
			for col_name, col_info in new_table["columns"].items():
				col_type = col_info["type"]
				col_nullable = col_info["nullable"]
				col_primary_key = col_info["primary_key"]
				col_foreign_keys = col_info.get("foreign_keys")
	
				column_def = f"Column('{col_name}', {col_type}"
				if col_primary_key:
					column_def += f", primary_key={col_primary_key}"
				if col_foreign_keys:
					column_def += f", {col_foreign_keys[0]}"
				column_def += f", nullable={col_nullable}"
				column_def += ")"
	
				columns.append(column_def)
	
			columns_str = ", \n\t\t".join(columns)
			upgrade_commands.append(f"wrapper.create_table('{table_name}', [\n\t\t{columns_str}\n\t])")
			downgrade_commands.append(f"wrapper.delete_table('{table_name}')")
	
		# Handle removed columns (drop columns first)
		for removed_column in autogenerate_table.get("removed_columns", []):
			table_name = removed_column["table"]
			column_name = removed_column["name"]
	
			upgrade_commands.append(f"wrapper.drop_column('{table_name}', '{column_name}')")
			downgrade_commands.append(f"wrapper.add_column('{table_name}', {column_name})")  # Assuming re-adding logic
	
		# Handle new columns (add columns after dropping)
		for new_column in autogenerate_table.get("new_columns", []):
			table_name = new_column["table"]
			column_name = new_column["name"]
			column_type = new_column["type"]
			nullable = new_column["nullable"]
			primary_key = new_column["primary_key"]
			foreign_keys = new_column.get("foreign_keys")
	
			col_def = f"Column('{column_name}', {column_type}"
			if primary_key:
				col_def += f", primary_key={primary_key}"
			if foreign_keys:
				col_def += f", ForeignKey('{foreign_keys[0]}')"
			col_def += f", nullable={nullable}"
			col_def += ")"
	
			upgrade_commands.append(f"wrapper.add_column('{table_name}', {col_def})")
			downgrade_commands.append(f"wrapper.drop_column('{table_name}', '{column_name}')")
	
		# Write to file
		with open(f"src/cargo/migrations/{name}.py", "w") as f:
			f.write("from libmercury.db import MigrationWrapper, Column, INTEGER, VARCHAR, ForeignKey\n\n")
			f.write(f"_version = '{name}'\n")
			f.write(f"_prev_version = '{int(name) - 1}'\n\n")
			f.write(f"_commit_message = '{message}'\n\n")
			f.write("def upgrade(url):\n")
			f.write("\twrapper = MigrationWrapper(url)\n")
			for cmd in upgrade_commands:
				f.write(f"\t{cmd}\n")
	
			f.write("\n\ndef downgrade(url):\n")
			f.write("\twrapper = MigrationWrapper(url)\n")
			for cmd in downgrade_commands:
				f.write(f"\t{cmd}\n")
	
		print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Generated file: src/cargo/migrations/{name}.py")

	def _create_migration(self, message) -> None:
		# Step 0: Load ORM models
		print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Loading ORM models")
		orm_models = self.load_orm_models(self.model_paths)
		
		# Step 2: Get the database schema
		print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Loading database schema")
		db_metadata = self.get_database_schema(self._extract_db_url_from_connection(self.db_connection_path))
		
		# Step 3: Compare schemas
		print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Finding discrepancies...")
		migration_response = self.compare_schemas(orm_models, db_metadata)
		discrepancies = migration_response[0]
		autogenerate_table = migration_response[1]
		
		# Output discrepancies
		print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Loading discrepancies")
		if discrepancies:
			for discrepancy in discrepancies:
				print(discrepancy)
			self._generate_file(autogenerate_table, message)
		else:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} ORM models perfectly match the database schema, no migrations are required")

	def load_orm_models(self, model_paths: list) -> list:
		models = []
		for path in model_paths:
			module_name = os.path.splitext(os.path.basename(path))[0]
			spec = importlib.util.spec_from_file_location(module_name, path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			for name, obj in inspect.getmembers(module, inspect.isclass):
				if hasattr(obj, '__table__'):
					models.append(obj)
		return models

	def get_database_schema(self, engine_url: str) -> MetaData:
		engine = create_engine(engine_url)
		metadata = MetaData()
		metadata.reflect(bind=engine)
		return metadata

	def compare_schemas(self, orm_models: list, db_metadata: MetaData) -> tuple:
		discrepancies = []
		autogenerate_table = {"new_columns": [], "new_tables": [], "removed_columns": []}
		orm_tables = {}
	
		for model in orm_models:
			table = model.__table__
			orm_tables[table.name] = {
				col.name: {
					"type": col.type,
					"nullable": col.nullable,
					"primary_key": col.primary_key,
					"foreign_keys": list(col.foreign_keys)	# Store foreign key information
				}
				for col in table.columns
			}
	
		db_tables = {
			table.name: {
				col.name: {
					"type": col.type,
					"nullable": col.nullable,
					"primary_key": col.primary_key,
					"foreign_keys": list(col.foreign_keys)	# Store foreign key information
				}
				for col in table.columns
			}
			for table in db_metadata.sorted_tables
		}
	
		for table_name, orm_columns in orm_tables.items():
			if table_name not in db_tables:
				discrepancies.append(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Table '{table_name}' is missing in the database.")
				autogenerate_table["new_tables"].append({
					"name": table_name,
					"columns": orm_columns
				})
				continue
	
			db_columns = db_tables[table_name]
	
			for col_name, orm_col_data in orm_columns.items():
				if col_name not in db_columns:
					discrepancies.append(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{col_name}' in table '{table_name}' is missing in the database.")
					autogenerate_table["new_columns"].append({
						"name": col_name,
						"type": orm_col_data["type"],
						"table": table_name,
						"nullable": orm_col_data["nullable"],
						"primary_key": orm_col_data["primary_key"],
						"foreign_keys": [fk.target_fullname for fk in orm_col_data["foreign_keys"]]
					})
				else:
					db_col_data = db_columns[col_name]
					if (str(orm_col_data["type"]) != str(db_col_data["type"]) or
						orm_col_data["nullable"] != db_col_data["nullable"] or
						orm_col_data["primary_key"] != db_col_data["primary_key"]):
						discrepancies.append(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{col_name}' in table '{table_name}' has type or attribute mismatch.")
						autogenerate_table["removed_columns"].append({
							"table": table_name,
							"name": col_name
						})
						autogenerate_table["new_columns"].append({
							"name": col_name,
							"type": orm_col_data["type"],
							"table": table_name,
							"nullable": orm_col_data["nullable"],
							"primary_key": orm_col_data["primary_key"],
							"foreign_keys": [fk.target_fullname for fk in orm_col_data["foreign_keys"]]
						})
	
			for col_name in db_columns:
				if col_name not in orm_columns:
					discrepancies.append(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{col_name}' in table '{table_name}' is extra in the database.")
					autogenerate_table["removed_columns"].append({
						"table": table_name,
						"name": col_name
					})
	
		return discrepancies, autogenerate_table

class MigrationWrapper:
	def __init__(self, connection_string: str) -> None:
		self.engine = create_engine(connection_string)
		self.metadata = MetaData(bind=self.engine)

	def create_table(self, table_name: str, columns: list) -> None:
		"""
		Create a new table with specified columns.
		
		:param table_name: Name of the table to create
		:param columns: List of Column definitions
		"""
		self.metadata.reflect(bind=self.engine)
		try:
			table = Table(table_name, self.metadata, *columns)
			table.create(self.engine)
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Table '{table_name}' created successfully.")
		except SQLAlchemyError as e:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Error creating table: {e}")

	def delete_table(self, table_name: str) -> None:
		"""
		Delete an existing table.
		
		:param table_name: Name of the table to delete
		"""
		try:
			table = Table(table_name, self.metadata, autoload_with=self.engine)
			table.drop(self.engine)
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Table '{table_name}' deleted successfully.")
		except SQLAlchemyError as e:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Error deleting table: {e}")

	def add_column(self, table_name: str, column: Column) -> None:
		"""
		Add a new column to an existing table.
	
		:param table_name: Name of the table
		:param column: Column definition
		"""
		try:
			table = Table(table_name, self.metadata, autoload_with=self.engine)
			with self.engine.connect() as conn:
				# Manually construct the column definition with type, nullable, and default value
				column_sql = f"{column.name} {column.type.compile(self.engine.dialect)}"
			
				if not column.nullable:
					column_sql += " NOT NULL"
				else:
					column_sql += " NULL"
			
				if column.default is not None:
					# Extract the default value, accounting for SQL expressions or callable defaults
					if callable(column.default.arg):
						default_value = column.default.arg()
					else:
						default_value = column.default.arg
					column_sql += f" DEFAULT {default_value}"
			
				conn.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_sql}')
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{column.name}' added to table '{table_name}'.")
		except SQLAlchemyError as e:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Error adding column: {e}")

	def drop_column(self, table_name: str, column_name: str) -> None:
		"""
		Drop an existing column from a table.
		
		:param table_name: Name of the table
		:param column_name: Name of the column to drop
		"""
		try:
			table = Table(table_name, self.metadata, autoload_with=self.engine)
			with self.engine.connect() as conn:
				conn.execute(f'ALTER TABLE {table_name} DROP COLUMN {column_name}')
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{column_name}' dropped from table '{table_name}'.")
		except SQLAlchemyError as e:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Error dropping column: {e}")

	def modify_column(self, table_name: str, old_column_name: str, new_column: Column) -> None:
		"""
		Modify an existing column in a table.
		
		:param table_name: Name of the table
		:param old_column_name: Name of the column to modify
		:param new_column: New Column definition
		"""
		try:
			table = Table(table_name, self.metadata, autoload_with=self.engine)
			with self.engine.connect() as conn:
				conn.execute(f'ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO temp_{old_column_name}')
				conn.execute(f'ALTER TABLE {table_name} ADD COLUMN {new_column.compile(conn.dialect)}')
				conn.execute(f'UPDATE {table_name} SET {new_column.name} = temp_{old_column_name}')
				conn.execute(f'ALTER TABLE {table_name} DROP COLUMN temp_{old_column_name}')
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Column '{old_column_name}' modified to '{new_column.name}' in table '{table_name}'.")
		except SQLAlchemyError as e:
			print(f"{Fore.GREEN}[Migrator]{Style.RESET_ALL} Error modifying column: {e}")

