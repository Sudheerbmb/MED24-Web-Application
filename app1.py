import MySQLdb
import sys
from langchain_groq import ChatGroq

# MySQL connection settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sudheer@123'
MYSQL_DB = 'medicaldelivery103'

# Groq API settings
groq_api_key = "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"
model_name = "llama-3.1-8b-instant"

# Function to fetch ordered medicines from the database based on user_id
def get_ordered_medicines(user_id):
    # Establish connection to the MySQL database
    conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # Query to get ordered medicines for the given user
    cursor.execute("""
        SELECT medicines.name
        FROM orders
        JOIN medicines ON orders.medicine_id = medicines.id
        WHERE orders.user_id = %s
    """, (user_id,))

    # Fetch the ordered medicines
    ordered_medicines = [row['name'] for row in cursor.fetchall()]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return ordered_medicines

# Function to get similar medicines from the Groq API
def get_similar_medicines(ordered_medicines):
    # Initialize Groq LLM API call with the key and model
    llm = ChatGroq(api_key=groq_api_key, model=model_name)

    # Construct the prompt to ask Groq for similar medicines
    prompt = f"""
    Here is a list of medicines ordered by a patient: {', '.join(ordered_medicines)}.
    Based on these medicines, suggest other similar medicines that could be recommended for the patient.
    Provide a list of recommended medicines and brief reasoning.
    Medicines ordered: {', '.join(ordered_medicines)}
    """

    # Send the prompt to the LLM
    response = llm.invoke(prompt)

    # Check for a valid response and return it, otherwise return an error message
    if response:
        return response.content
    else:
        return "Error fetching recommended medicines."

# Main function to get similar medicines based on user orders
def recommend_similar_medicines(user_id):
    # Step 1: Fetch ordered medicines for the given user ID
    ordered_medicines = get_ordered_medicines(user_id)

    if not ordered_medicines:
        return "No previous orders found for this user."

    # Step 2: Get similar medicines using Groq API
    similar_medicines = get_similar_medicines(ordered_medicines)

    return similar_medicines

# Example usage
if len(sys.argv) > 1:
    try:
        user_id = int(sys.argv[1])  # Get user_id from command-line argument
        recommended_medicines = recommend_similar_medicines(user_id)
        print("Recommended medicines based on your order history:", recommended_medicines)
    except ValueError:
        print("Please enter a valid user ID (integer).")
else:
    print("Please provide a user ID as a command-line argument.")
