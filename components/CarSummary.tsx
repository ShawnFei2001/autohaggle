"use client";

import { motion } from "framer-motion";
import Image from "next/image";

type CarSummaryProps = {
  data: {
    make: string;
    model: string;
    trim: string;
    year: string | number;
    state: string;
    color: string;
    interior: string;
    odometer: string | number;
    condition: string | number;
    mmr: string | number;
  };
  prediction: { cluster: number; predicted_price: number };
};

export default function CarSummary({ data, prediction }: CarSummaryProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mt-6 p-6 border border-gray-200 rounded-2xl shadow-xl bg-white max-w-3xl mx-auto"
    >
      <div className="flex flex-col md:flex-row gap-6">
        {/* Car Image */}
        <div className="flex-shrink-0">
          <Image
            src="/car_image.jpg"
            alt="Mystery Car"
            width={220}
            height={140}
            className="rounded-lg object-cover"
          />
        </div>

        {/* Info + Prediction */}
        <div className="flex-1">
          <h3 className="text-xl font-bold text-blue-700 mb-2">
            Prediction Result
          </h3>

          {/* Car Details */}
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-700 mb-4">
            {Object.entries(data).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="capitalize">{key}:</span>
                <span className="font-medium">{value}</span>
              </div>
            ))}
          </div>

          {/* Highlighted Prediction */}
          <div className="bg-blue-50 border border-blue-200 text-blue-900 rounded-md p-4 mb-4 text-sm font-semibold">
            Cluster: {prediction.cluster}
            <br />
            Predicted Price: ${prediction.predicted_price.toFixed(2)}  
          </div>

          {/* Save Button */}
          <button
            onClick={() => alert("Saved! (You can connect this to Supabase or DB logic)")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition"
          >
            Save Prediction
          </button>
        </div>
      </div>
    </motion.div>
  );
}
