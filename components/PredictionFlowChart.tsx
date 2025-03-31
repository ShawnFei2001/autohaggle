"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export default function PredictionFlowChart() {
  const steps = [
    {
      title: "Step 1: Input Car Details",
      description: "User provides make, model, year, mileage, condition, and more.",
    },
    {
      title: "Step 2: Assign to Cluster",
      description: "We assign your car to a cluster of similar vehicles using feature-based grouping.",
    },
    {
      title: "Step 3: Use Best Model",
      description: "Each cluster has its own optimized prediction model trained on real-market data.",
    },
    {
      title: "Step 4: Predict Fair Price",
      description: "The model predicts the most accurate fair-market price for your car.",
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white rounded-xl shadow p-6 max-w-xl mx-auto text-center"
    >
      <h2 className="text-xl font-semibold text-blue-600 mb-4">🔍 How AutoHaggle Predicts Price</h2>

      <div className="flex flex-col gap-6">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            className="flex items-center gap-4"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.2 }}
          >
            <div className="flex flex-col items-start">
              <p className="font-semibold text-gray-800">{step.title}</p>
              <p className="text-sm text-gray-600">{step.description}</p>
            </div>
            {idx < steps.length - 1 && (
              <ArrowRight className="text-blue-500 shrink-0" />
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
