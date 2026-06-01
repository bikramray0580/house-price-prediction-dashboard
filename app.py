import customtkinter as ctk
import joblib
import os
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "house_model.pkl")
ACC_PATH = os.path.join(BASE_DIR, "models", "accuracy.pkl")

try:
    model = joblib.load(MODEL_PATH)
    accuracy = joblib.load(ACC_PATH) if os.path.exists(ACC_PATH) else 0.0
except Exception as e:
    messagebox.showerror("Model Error", f"Run train_model.py first\n\n{e}")
    raise SystemExit

history = []

def predict_price():
    try:
        living_area = float(area_entry.get())
        quality = float(quality_entry.get())
        bedrooms = float(bedroom_entry.get())
        bathrooms = float(bathroom_entry.get())
        garage = float(garage_entry.get())
        year = float(year_entry.get())

        pred = model.predict([[
            living_area,
            quality,
            bedrooms,
            bathrooms,
            garage,
            year
        ]])

        price = int(pred[0])

        result_label.configure(text=f"₹ {price:,}")

        record = f"₹ {price:,} | Area:{int(living_area)} | Q:{int(quality)}"
        history.append(record)

        history_box.configure(state="normal")
        history_box.insert("end", record + "\n")
        history_box.configure(state="disabled")

        status_label.configure(
            text=f"Last Prediction: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

    except Exception:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values."
        )

def reset_fields():
    for widget in [
        area_entry,
        quality_entry,
        bedroom_entry,
        bathroom_entry,
        garage_entry,
        year_entry
    ]:
        widget.delete(0, "end")

    result_label.configure(text="₹ 0")

root = ctk.CTk()
root.title("House Price Prediction Dashboard")
root.geometry("1300x780")

header = ctk.CTkFrame(root, height=80)
header.pack(fill="x", padx=20, pady=15)

ctk.CTkLabel(
    header,
    text="🏠 House Price Prediction Dashboard",
    font=("Segoe UI", 28, "bold")
).pack(anchor="w", padx=20, pady=(10,0))

ctk.CTkLabel(
    header,
    text="Kaggle House Prices Dataset + Random Forest",
    font=("Segoe UI", 14)
).pack(anchor="w", padx=22)

main = ctk.CTkFrame(root, fg_color="transparent")
main.pack(fill="both", expand=True, padx=20, pady=10)

left = ctk.CTkFrame(main)
left.pack(side="left", fill="both", expand=True, padx=(0,10))

right = ctk.CTkFrame(main)
right.pack(side="right", fill="both", expand=True)

ctk.CTkLabel(left,text="House Details",font=("Segoe UI",24,"bold")).pack(anchor="w",padx=20,pady=20)

def make_field(parent,label):
    ctk.CTkLabel(parent,text=label).pack(anchor="w",padx=20)
    e=ctk.CTkEntry(parent,width=350,height=40)
    e.pack(padx=20,pady=(5,15))
    return e

area_entry = make_field(left,"Living Area (GrLivArea)")
quality_entry = make_field(left,"Overall Quality (1-10)")
bedroom_entry = make_field(left,"Bedrooms")
bathroom_entry = make_field(left,"Bathrooms")
garage_entry = make_field(left,"Garage Cars")
year_entry = make_field(left,"Year Built")

ctk.CTkButton(left,text="Predict Price",height=45,command=predict_price).pack(padx=20,pady=10,fill="x")
ctk.CTkButton(left,text="Reset",height=45,command=reset_fields).pack(padx=20,pady=(0,20),fill="x")

price_card = ctk.CTkFrame(right)
price_card.pack(fill="x", padx=15, pady=15)

ctk.CTkLabel(
    price_card,
    text="Estimated House Price",
    font=("Segoe UI",22,"bold")
).pack(pady=(20,10))

result_label = ctk.CTkLabel(
    price_card,
    text="₹ 0",
    font=("Segoe UI",48,"bold"),
    text_color="green"
)
result_label.pack(pady=(10,20))

info_card = ctk.CTkFrame(right)
info_card.pack(fill="x", padx=15, pady=10)

ctk.CTkLabel(info_card,text="Model Information",font=("Segoe UI",20,"bold")).pack(anchor="w",padx=15,pady=15)

info = [
    ("Model","Random Forest Regressor"),
    ("Dataset","Kaggle House Prices"),
    ("Features","6"),
    ("Accuracy",f"{accuracy:.2%}")
]

for k,v in info:
    row = ctk.CTkFrame(info_card,fg_color="transparent")
    row.pack(fill="x",padx=15,pady=3)
    ctk.CTkLabel(row,text=k).pack(side="left")
    ctk.CTkLabel(row,text=v,font=("Segoe UI",12,"bold")).pack(side="right")

history_card = ctk.CTkFrame(right)
history_card.pack(fill="both", expand=True, padx=15, pady=10)

ctk.CTkLabel(history_card,text="Prediction History",font=("Segoe UI",18,"bold")).pack(anchor="w",padx=15,pady=10)

history_box = ctk.CTkTextbox(history_card)
history_box.pack(fill="both",expand=True,padx=15,pady=10)
history_box.configure(state="disabled")

status_bar = ctk.CTkFrame(root,height=40)
status_bar.pack(fill="x",padx=20,pady=(0,20))

status_label = ctk.CTkLabel(status_bar,text="Ready")
status_label.pack(side="left",padx=10,pady=8)

root.mainloop()
