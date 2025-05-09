"use client";

import { useState } from "react";
import CarSummary from "./CarSummary";
import FeatureImpact from "./FeatureImpact";
import PredictionFlowChart from "./PredictionFlowChart";

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
    mmr: "",
  });

  const [prediction, setPrediction] = useState<{
    cluster: number;
    predicted_price: number;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Array of US state 2-letter abbreviations
  const states = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga",
    "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md",
    "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj",
    "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc",
    "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"
  ];

  // Function to validate strings: only letters, spaces, and hyphens allowed
  const isValidString = (str: string) => /^[A-Za-z\s\-]+$/.test(str);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validate "model", "trim", "color", and "interior" fields using regex
    if (!isValidString(formData.model)) {
      setError("Please enter a valid car model (letters, spaces, and hyphens only).");
      return;
    }
    if (!isValidString(formData.trim)) {
      setError("Please enter a valid car trim (letters, spaces, and hyphens only).");
      return;
    }
    if (!isValidString(formData.color)) {
      setError("Please enter a valid car color (letters, spaces, and hyphens only).");
      return;
    }
    if (!isValidString(formData.interior)) {
      setError("Please enter a valid car interior (letters, spaces, and hyphens only).");
      return;
    }

    setLoading(true);
    setPrediction(null);
    try {
      const payload = {
        ...formData,
        year: Number(formData.year),
        odometer: Number(formData.odometer),
        condition: Number(formData.condition),
        mmr: Number(formData.mmr),
      };

      const response = await fetch("https://autohaggleapi.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Failed to fetch prediction");

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error("Error predicting price:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex gap-6 overflow-hidden">
      {/* Form Section */}
      <form
        onSubmit={handleSubmit}
        className="w-1/2 bg-white p-6 rounded-xl shadow-md overflow-auto flex flex-col gap-4"
      >
        <h2 className="text-lg font-semibold text-blue-700">Enter Car Details</h2>
        {error && <p className="text-red-600">{error}</p>}
        <div className="grid grid-cols-2 gap-4">
          {[
            { name: "make", label: "Make" },
            { name: "model", label: "Model" },
            { name: "trim", label: "Trim" },
            { name: "year", label: "Year", type: "number" },
            { name: "state", label: "State" },
            { name: "color", label: "Color" },
            { name: "interior", label: "Interior" },
            { name: "odometer", label: "Odometer", type: "number" },
            { name: "condition", label: "Condition", type: "number" },
            { name: "mmr", label: "MMR", type: "number" },
          ].map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-medium text-gray-700">{field.label}</label>
              {field.name === "state" ? (
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="mt-1 p-2 border rounded w-full"
                >
                  <option value="">Select State</option>
                  {states.map((state) => (
                    <option key={state} value={state}>
                      {state}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type || "text"}
                  name={field.name}
                  value={(formData as any)[field.name]}
                  onChange={handleChange}
                  placeholder={`Enter ${field.label}`}
                  className="mt-1 p-2 border rounded w-full"
                />
              )}
            </div>
          ))}
        </div>
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition"
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict Price"}
        </button>
      </form>

      {/* Result Section */}
      <div className="w-1/2 flex flex-col gap-4 overflow-auto pr-1">
        {!loading && prediction ? (
          <>
            <CarSummary data={formData} prediction={prediction} />
            <FeatureImpact />
          </>
        ) : (
          <PredictionFlowChart />
        )}
      </div>
    </div>
  );
}
