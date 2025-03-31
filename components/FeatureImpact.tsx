"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Slider } from "@/components/ui/slider";

type Feature = {
  name: string;
  originalValue: number;
  importance: number;
  min: number;
  max: number;
  step: number;
  simulate: (value: number) => number; // function to generate predicted price
};

const dummyFeatures: Feature[] = [
  {
    name: "odometer",
    originalValue: 20000,
    importance: 35,
    min: 0,
    max: 100000,
    step: 5000,
    simulate: (val) => 27000 - (val / 1000) * 100, // decreasing
  },
  {
    name: "condition",
    originalValue: 6,
    importance: 25,
    min: 1,
    max: 10,
    step: 1,
    simulate: (val) => 20000 + val * 500, // increasing
  },
  {
    name: "mmr",
    originalValue: 20394,
    importance: 20,
    min: 15000,
    max: 25000,
    step: 500,
    simulate: (val) => val + 1000, // linear influence
  },
];

export default function FeatureImpact() {
  const [selectedFeature, setSelectedFeature] = useState<Feature>(dummyFeatures[0]);
  const [sliderValue, setSliderValue] = useState<number>(selectedFeature.originalValue);
  const [predictedPrice, setPredictedPrice] = useState<number>(selectedFeature.simulate(sliderValue));

  useEffect(() => {
    setSliderValue(selectedFeature.originalValue);
    setPredictedPrice(selectedFeature.simulate(selectedFeature.originalValue));
  }, [selectedFeature]);

  const handleSliderChange = (value: number[]) => {
    setSliderValue(value[0]);
    setPredictedPrice(selectedFeature.simulate(value[0]));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mt-8 p-6 bg-white rounded-2xl shadow-lg max-w-3xl w-full min-h-[400px] mx-auto transition-all duration-300"
    >
      <h3 className="text-xl font-bold mb-4 text-blue-700">📊 Feature Impact & What-If Analysis</h3>

      {/* Feature Importance List */}
      <div className="mb-6">
        <p className="text-sm text-gray-600 mb-2">Top contributing features:</p>
        <ul className="space-y-2">
          {dummyFeatures.map((f) => (
            <li
              key={f.name}
              onClick={() => setSelectedFeature(f)}
              className={`cursor-pointer p-2 rounded border transition ${
                selectedFeature.name === f.name
                  ? "bg-blue-50 border-blue-300"
                  : "hover:bg-gray-50"
              }`}
            >
              <div className="flex justify-between text-sm">
                <span className="capitalize w-[100px] truncate">{f.name}</span>
                <span className="text-gray-700 font-medium">{f.importance}% importance</span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Slider Interaction */}
      <div>
        <p className="text-sm mb-2 text-gray-700 font-medium">
          Adjust <span className="text-blue-600">{selectedFeature.name}</span> to simulate price:
        </p>
        <div className="mb-4">
          <Slider
            min={selectedFeature.min}
            max={selectedFeature.max}
            step={selectedFeature.step}
            defaultValue={[selectedFeature.originalValue]}
            value={[sliderValue]}
            onValueChange={handleSliderChange}
          />
          <div className="flex justify-between text-sm mt-1 text-gray-500">
            <span>{selectedFeature.min}</span>
            <span>{sliderValue}</span>
            <span>{selectedFeature.max}</span>
          </div>
        </div>

        <div className="p-4 bg-blue-50 border border-blue-200 rounded-md text-blue-800 text-center font-semibold text-lg">
          Predicted Price: ${predictedPrice.toFixed(0)}
        </div>
      </div>
    </motion.div>
  );
}
