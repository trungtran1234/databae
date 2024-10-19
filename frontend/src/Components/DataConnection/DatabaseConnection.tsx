"use client"
import React from 'react';
import InputField from './InputField';
import { motion } from 'framer-motion'


interface DatabaseConnectionProps { }

const DatabaseConnection: React.FC<DatabaseConnectionProps> = () => {
    const inputFields = [
        { label: 'Host', placeholder: 'eg. 127.0.0.1', iconSrc: 'https://cdn.builder.io/api/v1/image/assets/TEMP/14f27d632515d47537f723fecf57e49242be7f7ca33f5ddb396cb72e42c32874?placeholderIfAbsent=true&apiKey=c3d4e9746c434e5e98e26e5bfcd328c0' },
        { label: 'Port', placeholder: 'eg. 3306', iconSrc: 'https://cdn.builder.io/api/v1/image/assets/TEMP/6d39d4f05dd655accc53b6c4d4e9b287ef04cdb9f6c3379f273b2cf76448154d?placeholderIfAbsent=true&apiKey=c3d4e9746c434e5e98e26e5bfcd328c0' },
        { label: 'Username', placeholder: 'Database username', iconSrc: 'https://cdn.builder.io/api/v1/image/assets/TEMP/8144f9e844443fdc4027207b0542a3717b3259ed82cb81663bc9695c4b767f27?placeholderIfAbsent=true&apiKey=c3d4e9746c434e5e98e26e5bfcd328c0' },
        { label: 'Password', placeholder: 'Database password', iconSrc: 'https://cdn.builder.io/api/v1/image/assets/TEMP/2da3d092bd039bbce6365c7fd2b2baab0b9bfd3b33ebc903ecc9dfc00541410a?placeholderIfAbsent=true&apiKey=c3d4e9746c434e5e98e26e5bfcd328c0' },
        { label: 'Database Name', placeholder: 'Name of your database', iconSrc: 'https://cdn.builder.io/api/v1/image/assets/TEMP/4850789fafcc4111cdec9ced11b580ed3c51e5fd89fa0e8336c10e913b1902ef?placeholderIfAbsent=true&apiKey=c3d4e9746c434e5e98e26e5bfcd328c0' },
    ];

    return (
        <main className="flex flex-col text-sm text-gray-500 max-h-[600px] min-w-[440px] justify-center items-center">
            <motion.section
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{
                    type: "spring",
                    stiffness: 100,
                    damping: 35,
                }}
                className="flex flex-col items-center px-6 py-6 max-w-[500px] w-full min-h-fit bg-white rounded-[32px] shadow-[8px_8px_4px_rgba(0,0,0,0.25)]"
            >
                <h1 className="self-center text-2xl font-semibold text-indigo-600">
                    Database Connection
                </h1>
                <p className="mt-2.5 text-xs">
                    Enter your database connection details to get started
                </p>
                <form className="w-full h-full text-xs">
                    {inputFields.map((field, index) => (
                        <InputField key={index} {...field} />
                    ))}
                    <div className='flex justify-center'>
                        <button
                            type="submit"
                            className="self-center px-9 py-2 mt-7 w-full max-w-[200px] text-xl text-white whitespace-nowrap bg-indigo-600 rounded-2xl"
                        >
                            Connect
                        </button>
                    </div>
                </form>
            </motion.section>
        </main>
    );
};

export default DatabaseConnection;