"use client"
import React from 'react';

interface InputFieldProps {
    label: string;
    placeholder: string;
    iconSrc: string;
}

const InputField: React.FC<InputFieldProps> = ({ label, placeholder, iconSrc }) => {
    return (
        <div className="mt-4">
            <label htmlFor={label.toLowerCase()} className="text-black">
                {label}
            </label>
            <div className="flex gap-6 pl-2 items-center self-center mt-1.5 text-base bg-neutral-200">
                <img loading="lazy" src={iconSrc} alt="" className="object-contain shrink-0 aspect-square w-[30px]" />
                <input
                    type="text"
                    id={label.toLowerCase()}
                    placeholder={placeholder}
                    className="flex-auto py-2 bg-transparent w-64"
                    aria-label={label}
                />
            </div>
        </div>
    );
};

export default InputField;