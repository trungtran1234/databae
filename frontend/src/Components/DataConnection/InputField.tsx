"use client"
import React from 'react';

interface InputFieldProps {
    label: string;
    placeholder: string;
    iconSrc: string;
    name: string; // Add name prop
    value: string; // Add value prop
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void; // Add onChange prop
}

const InputField: React.FC<InputFieldProps> = ({ label, placeholder, iconSrc, name, value, onChange }) => {
    return (
        <div className="mt-4">
            <label htmlFor={name} className="text-white">
                {label}
            </label>
            <div className="flex gap-6 pl-2 items-center self-center mt-1.5 text-base bg-gray">
                <img loading="lazy" src={iconSrc} alt="" className="object-contain shrink-0 aspect-square w-[30px]" />
                <input
                    type={name === "password" ? "password" : "text"} // Handle password type if applicable
                    id={name}
                    name={name} // Set the name for input identification
                    placeholder={placeholder}
                    value={value} // Set the controlled value
                    onChange={onChange} // Set the onChange handler
                    className="flex-auto py-2 bg-gray rounded-md w-64"
                    aria-label={label}
                />
            </div>
        </div>
    );
};

export default InputField;
