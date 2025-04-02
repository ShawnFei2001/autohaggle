"use client";

import { useState, useEffect } from "react";
import { validCarMakes } from "@/lib/carMakes"; // adjust path accordingly

export default function CarMakeInput({
  value,
  onChange,
}: {
  value: string;
  onChange: (val: string) => void;
}) {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    onChange(inputValue);
    if (inputValue) {
      const filtered = validCarMakes.filter((make) =>
        make.toLowerCase().includes(inputValue.toLowerCase())
      );
      setSuggestions(filtered);
    } else {
      setSuggestions([]);
    }
  };

  return (
    <div className="relative">
      <input
        type="text"
        value={value}
        onChange={handleInputChange}
        placeholder="Enter car make"
        className="mt-1 p-2 border rounded w-full"
      />
      {suggestions.length > 0 && (
        <ul className="absolute z-10 bg-gray-800 border border-gray-700 w-full max-h-40 overflow-auto">
        {suggestions.map((make) => (
          <li
            key={make}
            onClick={() => {
              onChange(make);
              setSuggestions([]);
            }}
            className="cursor-pointer p-2 text-white hover:bg-gray-700"
          >
            {make}
          </li>
        ))}
      </ul>      
      )}
    </div>
  );
}
