import requests
import time

AIRFLOW_URL = 'http://localhost:8080/api/v1' # Airflow's version 1 API.

# Airflow authentication
USERNAME = "admin"
PASSWORD = "aryan"

# Function to triggere a DAG run via Airflow REST API
def trigger_dag(dag_id):
    response = requests.post(
        f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns",
        auth=(USERNAME, PASSWORD),
        json={"conf": {}}   
    )
    if response.status_code == 200:          # If Airflow responds with 200, that means the DAG was successfully triggered.
        run_id =response.json()["dag_run_id"]
        print(f"Triggered DAG '{dag_id}' with run ID: {run_id}")
        return run_id
    else:
        print(f" Failed to trigger DAG '{dag_id}'.Response: {response.text}")
        return None

# Function to poll for DAG run status
def poll_dag_status(dag_id, run_id):
    while True:
        response = requests.get(
            f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns/{run_id}",
            auth=(USERNAME, PASSWORD)
        )
        if response.status_code == 200:
            state = response.json()["state"]
            print(f"DAG '{dag_id}' run '{run_id}' status: {state}")
            if state in ["success", "failed"]:
                return state
                
        else:
            print(f"Failed to get status for DAG '{dag_id}'. Response: {response.text}")
            return None
        time.sleep(10)  # Check again in 10 seconds

# Main function to trigger and poll DAG
if __name__ == "__main__":

    # Step 1: Trigger first DAG
    dag1_id = "amazon-product-pipeline"
    dag1_run_id = trigger_dag(dag1_id)

    # Step 2: Wait for DAG1 to finish
    if dag1_run_id:
        final_status = poll_dag_status(dag1_id, dag1_run_id)

        # Step 3: If DAG! is successful, trigger DAG2
        if final_status == "success":
            dag2_id = "transform-amazon-product-data"
            trigger_dag(dag2_id)
        else:
            print(" DAG1 failed, DAG2 will not be triggered.")