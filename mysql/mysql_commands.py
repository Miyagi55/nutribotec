import argparse
import pymysql
from mysql.database_connector import connection


def update_and_delete_survey_id(survey_id):
    try:
        with connection.cursor() as cursor:
            # Update users table
            cursor.execute('UPDATE users SET survey_id = NULL WHERE survey_id = %s', (survey_id,))
            
            # Delete from answers table
            cursor.execute('DELETE FROM answers WHERE survey_id = %s', (survey_id,))
            
            # Commit the transaction
            connection.commit()
    
    except Exception as e:
        print(f"Error in update_and_delete_survey_id: {e}")
   


def delete_user_id_row(user_id):
    delete_query = "DELETE FROM users WHERE user_id = %s;"

    try:
        cursor = connection.cursor()
        cursor.execute(delete_query, (user_id,))
        connection.commit()  # Commit the transaction to apply the changes
        print(f"{user_id} deleted from users table")
        
    except Exception as e:
        print(f"Error in delete_user_id_row: {e}")
        connection.rollback()  # Rollback the transaction if an error occurs




def select_from_table(table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        cursor = connection.cursor()
        cursor.execute(query)
        
        result = cursor.fetchall()

        print(result)
        return result

    except Exception as e:
        print(f"Error in select_from_table: {e}")






def describe_table(table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        print(cursor.fetchall())
    except Exception as e:
        print(f"Error in describe_table: {e}")
    




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute specific functions.")
    parser.add_argument("action", choices=["update_delete", "select", "describe","delete"], help="Action to execute")
    parser.add_argument("--survey_id", type=int, help="Survey ID")
    parser.add_argument("--table_name", help="Table name")
    parser.add_argument("--user_id", help="User ID")
    args = parser.parse_args()


    if args.action == "update_delete" and args.survey_id is not None:
        update_and_delete_survey_id(args.survey_id)
    elif args.action == "delete" and args.user_id is not None:
        delete_user_id_row(args.user_id)
    elif args.action == "select" and args.table_name is not None:
        select_from_table(args.table_name)
    elif args.action == "describe" and args.table_name is not None:
        describe_table(args.table_name)
    else:
        print("Invalid arguments provided.")