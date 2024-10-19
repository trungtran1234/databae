import React from 'react';
import Background from '../../Components/Background'; // Import the component
import DatabaseConnection from "../../Components/DataConnection/DatabaseConnection";

const Page = () => {
    return (
        <div className="relative flex items-center justify-center min-h-screen">
            <div className="absolute inset-0 w-full h-full">
                <Background />
            </div>

            <div className="relative z-10">
                <DatabaseConnection />
            </div>
        </div>
    );
};

export default Page;
