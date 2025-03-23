import pandas as pd
import numpy as np

from faker import Faker

fake = Faker()


DATASET_SCHEMAS = {
    "healthcare": {
        "patient_id": lambda: fake.uuid4(),
        "age": lambda: np.random.randint(20, 80),
        "gender": lambda: np.random.choice(["Male", "Female"]),
        "diagnosis": lambda: np.random.choice(["Diabetes", "Hypertension", "Heart Disease", "None"]),
        "treatment": lambda: np.random.choice(["Medication", "Surgery", "Therapy", "None"]),
        "hospital": lambda: fake.company()
    },
    "finance": {
        "transaction_id": lambda: fake.uuid4(),
        "account_number": lambda: fake.iban(),
        "amount": lambda: round(np.random.uniform(10, 5000), 2),
        "currency": lambda: np.random.choice(["USD", "EUR", "GBP", "JPY"]),
        "transaction_type": lambda: np.random.choice(["Deposit", "Withdrawal", "Transfer", "Payment"]),
        "account_balance": lambda: round(np.random.uniform(1000, 50000), 2)
    },
    "retail": {
        "order_id": lambda: fake.uuid4(),
        "customer_name": lambda: fake.name(),
        "product": lambda: np.random.choice(["Laptop", "Smartphone", "Shoes", "Book", "Headphones"]),
        "quantity": lambda: np.random.randint(1, 10),
        "price": lambda: round(np.random.uniform(5, 500), 2)
    },
    "hr": {
        "employee_id": lambda: fake.uuid4(),
        "name": lambda: fake.name(),
        "department": lambda: np.random.choice(["HR", "Engineering", "Sales", "Marketing"]),
        "salary": lambda: round(np.random.uniform(40000, 120000), 2),
        "hire_date": lambda: fake.date_this_decade().isoformat()
    },
    "cybersecurity": {
        "log_id": lambda: fake.uuid4(),
        "timestamp": lambda: fake.date_time_this_year().isoformat(),
        "ip_address": lambda: fake.ipv4(),
        "event_type": lambda: np.random.choice(["Login", "Failed Login", "Data Breach", "Phishing Attempt"]),
        "status": lambda: np.random.choice(["Success", "Failure"])
    },
    "ecommerce": {
        "order_id": lambda: fake.uuid4(),
        "customer": lambda: fake.name(),
        "product": lambda: np.random.choice(["Laptop", "Phone", "TV", "Shoes", "Watch"]),
        "price": lambda: round(np.random.uniform(20, 1000), 2),
        "order_status": lambda: np.random.choice(["Shipped", "Pending", "Delivered", "Cancelled"])
    }
}

def generate_synthetic_data(dataset="healthcare", rows=10, missing_values=0.0, add_outliers=False):
    """Generate synthetic data dynamically based on predefined schemas."""
    dataset = dataset.lower()

    if dataset not in DATASET_SCHEMAS:
        raise ValueError(f"Invalid dataset '{dataset}'. Choose from: {', '.join(DATASET_SCHEMAS.keys())}")

    schema = DATASET_SCHEMAS[dataset]

    
    data = {column: [func() for _ in range(rows)] for column, func in schema.items()}

    
    df = pd.DataFrame(data)

    
    if dataset == "retail":
        df["total_amount"] = df["quantity"] * df["price"]

    return apply_data_modifications(df, missing_values, add_outliers)

def apply_data_modifications(df, missing_values, add_outliers):
    """Apply missing values and outliers to dataset."""
    if missing_values > 0:
        for col in df.columns:
            df.loc[df.sample(frac=missing_values).index, col] = None

    if add_outliers:
        num_outliers = max(1, int(0.05 * len(df)))  # At least 1 outlier
        outlier_indices = np.random.choice(df.index, num_outliers, replace=False)
        for col in df.select_dtypes(include=["float64", "int64"]).columns:
            df.loc[outlier_indices, col] *= np.random.randint(5, 10)

    return df
