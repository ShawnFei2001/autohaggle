"use client";

import { useState } from "react";

export default function CarForm() {
  const [formData, setFormData] = useState({
    make: "",
    model: "",
    trim: "",
    year: "",
    state: "",
    color: "",
    interior: "",
    odometer: "",
    condition: "",
    mmr: ""
  });
  const [prediction, setPrediction] = useState<{ cluster: number; predicted_price: number } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);
    try {
      // Ensure numeric fields are converted to numbers
      const payload = {
        ...formData,
        year: Number(formData.year),
        odometer: Number(formData.odometer),
        condition: Number(formData.condition),
        mmr: Number(formData.mmr)
      };

      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error("Error predicting price:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4">
        {[
          { name: "make", label: "Make", type: "text" },
          { name: "model", label: "Model", type: "text" },
          { name: "trim", label: "Trim", type: "text" },
          { name: "year", label: "Year", type: "number" },
          { name: "state", label: "State", type: "text" },
          { name: "color", label: "Color", type: "text" },
          { name: "interior", label: "Interior", type: "text" },
          { name: "odometer", label: "Odometer", type: "number" },
          { name: "condition", label: "Condition", type: "number" },
          { name: "mmr", label: "MMR", type: "number" }
        ].map((field) => (
          <div key={field.name}>
            <label className="block text-sm font-medium">{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              value={(formData as any)[field.name]}
              onChange={handleChange}
              placeholder={`Enter car ${field.label.toLowerCase()}`}
              className="mt-1 p-2 border rounded w-full"
            />
          </div>
        ))}
      </div>
      <button
        type="submit"
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Predicting..." : "Predict Price"}
      </button>
      {prediction && (
        <div className="mt-4 p-4 border rounded">
          <h3 className="font-bold">Predicted Price:</h3>
          <p>
            Cluster: {prediction.cluster} | Price: ${prediction.predicted_price}
          </p>
        </div>
      )}
    </form>
  );
}