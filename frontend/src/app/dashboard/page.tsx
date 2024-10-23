'use client'

import React, { useState, memo, useLayoutEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/Components/ui/button"
import { Textarea } from "@/Components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/Components/ui/card"
import { Send } from 'lucide-react'
import ReactMarkdown from 'react-markdown';
import { } from 'ldrs';
import parse from 'html-react-parser';
import AgentStatus from '@/Components/AgentStatus'


interface FloatingCircleProps {
    size: string;
    initialPosition: { top?: string; left?: string; right?: string; bottom?: string };
    duration: number;
}

const FloatingCircle: React.FC<FloatingCircleProps> = ({ size, initialPosition, duration }) => (
    <motion.div
        className={`absolute rounded-full bg-CircleColor opacity-20 ${size}`}
        initial={initialPosition}
        animate={{
            x: [0, Math.random() * 100 - 50, 0],
            y: [0, Math.random() * 100 - 50, 0],
        }}
        transition={{
            repeat: Infinity,
            duration: duration,
            ease: "easeInOut",
        }}
    />
)

interface MyComponentProps {
    response: string; // Assuming response is a string containing HTML
}

const FormTable: React.FC<MyComponentProps> = ({ response }) => {
    const elRef = useRef<HTMLDivElement>(null);

    useLayoutEffect(() => {
        if (elRef.current) {
            // Access the table after it has been rendered
            const table = elRef.current.querySelector('table');

            if (table) {
                // Apply dynamic styles
                table.style.width = '100%'; // Make the table take full width
                table.style.borderCollapse = 'collapse'; // Collapse borders

                // Style table headers
                const headers = table.querySelectorAll('th');
                headers.forEach((header) => {
                    header.style.backgroundColor = '#f3f4f6'; // Light gray background
                    header.style.border = '2px solid #d1d5db'; // Gray border
                    header.style.padding = '8px'; // Padding for headers
                });

                // Style table cells
                const cells = table.querySelectorAll('td');
                cells.forEach((cell) => {
                    cell.style.border = '1px solid #d1d5db'; // Gray border
                    cell.style.padding = '8px'; // Padding for cells
                });

                // Optional: Style the table rows
                const rows = table.querySelectorAll('tr');
                rows.forEach((row) => {
                    row.style.transition = 'background-color 0.2s';
                    row.addEventListener('mouseenter', () => {
                        row.style.backgroundColor = '#f9fafb'; // Light hover effect
                    });
                    row.addEventListener('mouseleave', () => {
                        row.style.backgroundColor = ''; // Reset background
                    });
                });
            }
        }
    }, [response]); // Run effect when response changes

    return (
        <div className="prose overflow-x-auto" ref={elRef}>
            {parse(response)}
        </div>
    );
};


export default function DatabaseVisualizer() {
    const [query, setQuery] = useState('')
    const [response, setResponse] = useState('')
    const [isLoading, setLoading] = useState(false)

    const handleRunQuery = async () => {

        setLoading(true);

        try {
            const res = await fetch('http://localhost:8000/endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            })
            const data = await res.json()
            console.log(data.status)

            if (data.status == 'successful') {
                console.log('IT IS SUCCESSFUL');
                setResponse(data["agent_response"]);
            } else {
                console.log('NAHHH');
                setResponse(`Error: ${data.error}`);
            }

        } catch (error) {
            console.error('Error running query:', error)
            setResponse('Error: Something went wrong')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-ThemeBg p-8 flex flex-col items-center overflow-scroll relative">
            {/* Floating circles */}
            <FloatingCircle size="w-16 h-16" initialPosition={{ top: "10%", left: "10%" }} duration={7} />
            <FloatingCircle size="w-24 h-24" initialPosition={{ top: "20%", right: "15%" }} duration={9} />
            <FloatingCircle size="w-20 h-20" initialPosition={{ bottom: "15%", left: "20%" }} duration={8} />
            <FloatingCircle size="w-32 h-32" initialPosition={{ bottom: "10%", right: "10%" }} duration={10} />

            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-3xl font-bold text-white mb-2 relative z-10"
            >
                Databae.
            </motion.h1>
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-5xl relative z-0"
            >
                <Card className="shadow-lg min-h-[calc(100vh-30vh)] border-stone-800  bg-[#1B1B1B] max-h-[calc(100vh-45vh)] mb-2 overflow-y-scroll">
                    <CardContent className="p-6 h-full overflow-y-auto">
                        {isLoading ? (
                            <div className='w-full h-full flex flex-col gap-y-2 items-center justify-center'>
                                <l-spiral></l-spiral>
                                <AgentStatus />
                            </div>
                        ) : (
                            <div className="w-full h-full bg-[#1B1B1B] rounded-lg flex items-center justify-center text-gray-300 overflow-auto">
                                {response ? (
                                    // Check if response contains HTML tags
                                    response.includes('<') && response.includes('>') ? (
                                        // Display HTML safely
                                        <FormTable response={response} />
                                    ) : (
                                        // Display Markdown
                                        <ReactMarkdown className="bg-white prose">
                                            {response}
                                        </ReactMarkdown>
                                    )
                                ) : (
                                    'How can I help you?'
                                )}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="w-full max-w-3xl mt-4 mb-8 fixed bottom-0 transform rounded-lg "

            >
                <Card className="shadow-md overflow-hidden bg-[#1B1B1B]">
                    <CardContent className="flex flex-row p-4">
                        <Textarea
                            placeholder=" E.g. Explain this database"
                            className="w-full text-white bottom-0 min-h-[20px] max-h-10 mr-3 left-1/2 p-2 border-none bg-[#1B1B1B] rounded-md"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <Button
                                onClick={handleRunQuery}
                                className="bg-purple-600 hover:bg-purple-700 text-white px-4 rounded-md flex items-center"
                                disabled={isLoading}
                            >
                                <Send className="w-4 h-4 mr-2" />
                                Run Query
                            </Button>
                        </motion.div>
                    </CardContent>
                </Card>
            </motion.div>
        </div>
    )
}   