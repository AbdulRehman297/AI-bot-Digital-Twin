import time
import pandas as pd
import groq

GROQ_API_KEY = "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" 
client = groq.Client(api_key=GROQ_API_KEY)

data_path = "D:\\medical gpt\\didgital twin agent\\healthcare_iot_target_dataset.csv"
df = pd.read_csv(data_path)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.rename(columns={"temperature_(°c)": "temperature_c"}, inplace=True)
print("Column names:", df.columns)  

def analyze_health_data(data):
    input_text = (
        f"Systolic: {data['systolic_bp_(mmhg)']} mmHg, Diastolic: {data['diastolic_bp_(mmhg)']} mmHg, "
        f"Heart Rate: {data['heart_rate_(bpm)']} bpm, Temperature: {data['temperature_f']}°F. "
        "Assess the patient's health condition and respond with 'okay' or 'warning/critical'."
    )

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a medical assistant analyzing patient health."},
                {"role": "user", "content": input_text}
            ],
            max_tokens=50
        )

        generated_text = response.choices[0].message.content.lower()

        if "critical" in generated_text or "warning" in generated_text:
            return {"status": "warning"}
        else:
            return {"status": "okay"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Main loop for iterate through dataset
if __name__ == "__main__":
    print("\nHealthcare Digital Twin Monitor\n")

    for index, row in df.iterrows():
        health_data = {
            "systolic_bp_(mmhg)": row["systolic_bp_(mmhg)"],
            "diastolic_bp_(mmhg)": row["diastolic_bp_(mmhg)"],
            "heart_rate_(bpm)": row["heart_rate_(bpm)"],
            "temperature_f": row["temperature_c"] * 9/5 + 32 
        }

        status = analyze_health_data(health_data)

        print(f"\nPatient {index + 1} Health Data")
        print(health_data)

        print("\nHealth Status")
        print(status)

        time.sleep(5) 